"""
Convert ComfyUI frontend workflow JSON -> API prompt graph and POST /prompt.

Usage:
  python workflow_submit.py <workflow_json_path> [--label name] [--validate-only]

Handles hidden widgets (ComfyUI auto-injects extras for some nodes):
  - KSampler / KSamplerAdvanced: 'control_after_generate' inserted after seed/noise_seed
  - LoadImage:                   'image' (upload-mode marker) inserted after image
  - PrimitiveNode etc not used here, skip.

Handles ComfyUI 0.19+ subgraph workflows:
  - Auto-unfolds subgraph instances (top-level nodes whose type is a subgraph
    definition GUID) into flat workflow before conversion.
  - Backward compatible: flat workflows pass through untouched.

Returns:
  prompt_id from /prompt response. Polls /history every 2s until done.
  --validate-only: stops after /prompt accepts (does not poll for completion).

History:
  2026-04-29 staged at D:\\tmp\\submit_smoke.py during Workflow #3 smoke testing.
  2026-04-29 promoted to D:\\Work\\system-setup\\tools\\workflow_submit.py
             (no logic changes, only docstring path/name; phase-1 promotion).
  2026-05-03 added unfold_subgraphs() for ComfyUI 0.19+ subgraph support
             (Wan 2.2 I2V Candidate B Comfy-Org official template uses subgraph).
"""
import copy
import json
import sys
import urllib.request
import time
import uuid
import argparse

HIDDEN_AFTER = {
    ("KSampler", "seed"),
    ("KSamplerAdvanced", "noise_seed"),
    ("LoadImage", "image"),
}

# Frontend-only node types that have no backend execution; skip during to_api conversion.
FRONTEND_ONLY_TYPES = {
    "Note",
    "MarkdownNote",
    "Reroute",
    "PrimitiveNode",
}


def unfold_subgraphs(frontend):
    """
    ComfyUI 0.19+ subgraph -> flat workflow.

    A subgraph instance is a top-level node whose `type` matches a subgraph
    definition id (GUID) in `definitions.subgraphs[]`. Each definition has
    `inputs`/`outputs` boundaries (virtual node ids -10 / -20 in internal
    `links`), `nodes` (inner), and `links` (dict format with id/origin_id/
    origin_slot/target_id/target_slot/type).

    Algorithm:
      1. For each instance:
         a. Walk subgraph inputs[]: rewire each boundary-input internal link
            (origin_id == -10) so its origin becomes the external source of
            the ext_link entering the instance at that slot. Remove ext_link.
         b. Walk subgraph outputs[]: for each boundary-output internal link
            (target_id == -20), find inner src node; rewire each ext_link
            leaving the instance at that slot to use inner src.
         c. Add all purely-inner internal links (no boundary endpoint) to
            top-level links (dict -> list format: [id, src, src_slot, dst,
            dst_slot, type]).
         d. Add all inner nodes to top-level (preserve ids).
         e. Remove the instance from top-level nodes.
      2. proxyWidgets override: NotImplementedError if instance widgets_values
         non-empty (no candidate exercising this path yet; can extend later).
      3. Backward compat: flat workflow (no `definitions.subgraphs`) passes
         through unmodified (returns input).

    Asserts no inner-id / inner-link-id collision with top-level. If a
    workflow ever needs id renumbering, raise NotImplementedError.
    """
    sg_defs_list = frontend.get('definitions', {}).get('subgraphs', []) or []
    if not sg_defs_list:
        return frontend
    sg_defs_by_id = {sg['id']: sg for sg in sg_defs_list}

    flat = copy.deepcopy(frontend)
    nodes = flat['nodes']
    links = flat['links']

    instances = [n for n in nodes if n['type'] in sg_defs_by_id]
    if not instances:
        return flat

    for inst in instances:
        sg_def = sg_defs_by_id[inst['type']]

        # Collision checks
        existing_node_ids = {n['id'] for n in nodes if n is not inst}
        for inner in sg_def['nodes']:
            if inner['id'] in existing_node_ids:
                raise NotImplementedError(
                    f"Inner node id {inner['id']} collides with top-level; "
                    f"id renumbering not implemented."
                )
        existing_link_ids = {L[0] for L in links}
        for il in sg_def['links']:
            if il['id'] in existing_link_ids:
                raise NotImplementedError(
                    f"Inner link id {il['id']} collides with top-level; "
                    f"id renumbering not implemented."
                )

        # proxyWidgets override (not implemented yet)
        proxy_widgets = inst.get('properties', {}).get('proxyWidgets', []) or []
        inst_wvals = inst.get('widgets_values', []) or []
        if inst_wvals and proxy_widgets:
            raise NotImplementedError(
                f"proxyWidgets override (instance widgets_values non-empty) "
                f"not implemented; instance id={inst['id']} "
                f"proxy={proxy_widgets} values={inst_wvals}"
            )

        inner_links_by_id = {il['id']: il for il in sg_def['links']}

        # 1a. Boundary inputs: rewire each input boundary internal link
        for slot_idx, sg_input in enumerate(sg_def['inputs']):
            ext_link = next(
                (L for L in links if L[3] == inst['id'] and L[4] == slot_idx),
                None,
            )
            if ext_link is None:
                # No external connection at this slot (widget-only input).
                continue
            ext_src_node, ext_src_slot = ext_link[1], ext_link[2]
            for ilid in sg_input.get('linkIds', []) or []:
                bl = inner_links_by_id.get(ilid)
                if bl is None or bl['origin_id'] != -10:
                    continue
                bl['origin_id'] = ext_src_node
                bl['origin_slot'] = ext_src_slot
            links.remove(ext_link)

        # 1b. Boundary outputs: rewire each ext_link leaving inst at this slot
        for slot_idx, sg_output in enumerate(sg_def['outputs']):
            ext_links_out = [
                L for L in links if L[1] == inst['id'] and L[2] == slot_idx
            ]
            inner_src = None
            for ilid in sg_output.get('linkIds', []) or []:
                bl = inner_links_by_id.get(ilid)
                if bl is None or bl['target_id'] != -20:
                    continue
                inner_src = (bl['origin_id'], bl['origin_slot'])
                break
            if inner_src is None:
                continue
            for ext_link in ext_links_out:
                ext_link[1] = inner_src[0]
                ext_link[2] = inner_src[1]

        # 1c. Add inner links to top-level. After 1a rewiring, boundary-input
        # links have origin_id != -10 (rewired) and behave like regular links.
        # Boundary-output links (target_id == -20) are consumed by 1b and dropped.
        # Boundary-input links not rewired (no ext_link at that slot) are dropped.
        for il in sg_def['links']:
            if il['origin_id'] == -10:
                continue  # boundary input not rewired (no ext source)
            if il['target_id'] == -20:
                continue  # boundary output, consumed by 1b
            links.append([
                il['id'],
                il['origin_id'],
                il['origin_slot'],
                il['target_id'],
                il['target_slot'],
                il['type'],
            ])

        # 1d. Add inner nodes
        nodes.extend(copy.deepcopy(sg_def['nodes']))

        # 1e. Remove instance
        nodes.remove(inst)

    return flat


_object_info_cache = None


def get_object_info():
    """Fetch and cache ComfyUI /object_info (backend INPUT_TYPES schema)."""
    global _object_info_cache
    if _object_info_cache is None:
        with urllib.request.urlopen(
            "http://127.0.0.1:8188/object_info", timeout=30
        ) as r:
            _object_info_cache = json.loads(r.read())
    return _object_info_cache


def _is_widget_type(type_value):
    """A schema input type is widget-bound if it's a list (legacy COMBO with
    inline options), or a primitive/COMBO type string. Connection types are
    uppercase node-data types like MODEL/CLIP/CONDITIONING/LATENT/IMAGE/etc.

    ComfyUI 0.19+ may return type as a string 'COMBO' with options stored in
    the type_def[1] dict (`'options': [...]`) rather than as an inline list.
    """
    if isinstance(type_value, (list, tuple)):
        return True
    if type_value in ("STRING", "INT", "FLOAT", "BOOLEAN", "COMBO"):
        return True
    return False


def to_api(frontend):
    """Convert flat ComfyUI frontend workflow -> backend prompt graph.

    Walks each class's INPUT_TYPES schema (from /object_info) in order,
    pulling values from node link connections (when input is connected) or
    from widgets_values (when widget input). Handles ComfyUI 0.19+ structure
    where widgets are NOT all listed in node.inputs[] (some widgets only exist
    in widgets_values, e.g., KSamplerAdvanced steps/cfg/sampler_name).
    """
    info = get_object_info()
    links_by_id = {L[0]: L for L in frontend.get("links", []) or []}
    api = {}
    for n in frontend["nodes"]:
        cls = n["type"]
        if cls in FRONTEND_ONLY_TYPES:
            continue
        nid = str(n["id"])
        wvals = n.get("widgets_values", []) or []
        result = {"class_type": cls, "inputs": {}}

        cls_info = info.get(cls)
        if cls_info is None:
            print(f"WARN: class_type '{cls}' not in /object_info; node id={nid} skipped", file=sys.stderr)
            continue

        input_schema = cls_info.get("input", {})
        schema_pairs = []
        for k, v in input_schema.get("required", {}).items():
            schema_pairs.append((k, v))
        for k, v in input_schema.get("optional", {}).items():
            schema_pairs.append((k, v))

        front_inputs_by_name = {inp["name"]: inp for inp in n.get("inputs", []) or []}

        widget_idx = 0
        for name, type_def in schema_pairs:
            type_value = (
                type_def[0]
                if isinstance(type_def, (list, tuple)) and len(type_def) > 0
                else type_def
            )
            is_widget = _is_widget_type(type_value)

            front_inp = front_inputs_by_name.get(name)
            link_id = front_inp.get("link") if front_inp else None

            if link_id is not None:
                L = links_by_id.get(link_id)
                if L is not None:
                    result["inputs"][name] = [str(L[1]), L[2]]
                    if is_widget:
                        widget_idx += 1
                        if (cls, name) in HIDDEN_AFTER:
                            widget_idx += 1
                    continue
                # link dangling (boundary not rewired); fall through to widget

            if is_widget:
                if widget_idx < len(wvals):
                    result["inputs"][name] = wvals[widget_idx]
                widget_idx += 1
                if (cls, name) in HIDDEN_AFTER:
                    widget_idx += 1
            # else: connection input without link; skip (optional)

        api[nid] = result
    return api


def post_prompt(prompt_dict):
    client_id = str(uuid.uuid4())
    body = json.dumps({"prompt": prompt_dict, "client_id": client_id}).encode("utf-8")
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read())
    return resp


def get_history():
    with urllib.request.urlopen("http://127.0.0.1:8188/history", timeout=10) as r:
        return json.loads(r.read())


def get_queue():
    with urllib.request.urlopen("http://127.0.0.1:8188/queue", timeout=10) as r:
        return json.loads(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--label", default="")
    ap.add_argument("--validate-only", action="store_true",
                    help="Stop after /prompt accepts (no polling for completion)")
    args = ap.parse_args()

    with open(args.path, "r", encoding="utf-8") as f:
        wf = json.load(f)

    # Unfold ComfyUI 0.19+ subgraphs into flat workflow (no-op for flat).
    flat_wf = unfold_subgraphs(wf)
    if flat_wf is not wf:
        print(f"[{args.label}] subgraph unfolded: "
              f"{len(wf['nodes'])} top nodes -> {len(flat_wf['nodes'])} flat nodes, "
              f"{len(wf.get('links', []))} top links -> {len(flat_wf['links'])} flat links")

    api_graph = to_api(flat_wf)
    print(f"[{args.label}] converted: {len(api_graph)} nodes")
    # quick dump first 3 nodes for inspection
    for nid in list(api_graph.keys())[:3]:
        print(f"  {nid} -> {api_graph[nid]}")

    t0 = time.time()
    resp = post_prompt(api_graph)
    print(f"[{args.label}] /prompt response: {resp}")
    pid = resp.get("prompt_id")
    if not pid:
        print(f"[{args.label}] no prompt_id, error?")
        sys.exit(2)
    if args.validate_only:
        print(f"[{args.label}] --validate-only: prompt_id={pid} accepted; exit")
        return
    print(f"[{args.label}] prompt_id={pid}, polling /history every 2s...")

    while True:
        time.sleep(2)
        # Check queue first (running or pending)
        q = get_queue()
        running_pids = [item[1] for item in q.get("queue_running", [])]
        pending_pids = [item[1] for item in q.get("queue_pending", [])]
        if pid not in running_pids and pid not in pending_pids:
            # Done (or never started). Check history.
            hist = get_history()
            if pid in hist:
                entry = hist[pid]
                status = entry.get("status", {})
                outputs = entry.get("outputs", {})
                out_files = []
                for nid_o, info in outputs.items():
                    for img in info.get("images", []):
                        out_files.append(img.get("filename"))
                elapsed = time.time() - t0
                print(f"[{args.label}] DONE in {elapsed:.2f}s")
                print(f"  status={status}")
                print(f"  outputs={out_files}")
                return
            else:
                print(f"[{args.label}] prompt {pid} not in queue or history -- error")
                sys.exit(3)
        else:
            elapsed = time.time() - t0
            where = "running" if pid in running_pids else "pending"
            print(f"  [{elapsed:5.1f}s] {where}, queue running={len(running_pids)} pending={len(pending_pids)}")


if __name__ == "__main__":
    main()
