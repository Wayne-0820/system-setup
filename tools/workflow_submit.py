"""
Convert ComfyUI frontend workflow JSON -> API prompt graph and POST /prompt.

Usage:
  python workflow_submit.py <workflow_json_path> [--label name]

Handles hidden widgets (ComfyUI auto-injects extras for some nodes):
  - KSampler / KSamplerAdvanced: 'control_after_generate' inserted after seed/noise_seed
  - LoadImage:                   'image' (upload-mode marker) inserted after image
  - PrimitiveNode etc not used here, skip.

Returns:
  prompt_id from /prompt response. Polls /history every 2s until done.

History:
  2026-04-29 staged at D:\\tmp\\submit_smoke.py during Workflow #3 smoke testing.
  2026-04-29 promoted to D:\\Work\\system-setup\\tools\\workflow_submit.py
             (no logic changes, only docstring path/name; phase-1 promotion).
"""
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

def to_api(frontend):
    links_by_id = {L[0]: L for L in frontend.get("links", []) or []}
    api = {}
    for n in frontend["nodes"]:
        nid = str(n["id"])
        cls = n["type"]
        wvals = n.get("widgets_values", []) or []
        result = {"class_type": cls, "inputs": {}}

        widget_idx = 0
        for inp in n.get("inputs", []) or []:
            name = inp["name"]
            if "widget" in inp:
                if widget_idx < len(wvals):
                    result["inputs"][name] = wvals[widget_idx]
                widget_idx += 1
                if (cls, name) in HIDDEN_AFTER:
                    widget_idx += 1
            else:
                lid = inp.get("link")
                if lid is None:
                    continue
                L = links_by_id.get(lid)
                if L:
                    result["inputs"][name] = [str(L[1]), L[2]]
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
    args = ap.parse_args()

    with open(args.path, "r", encoding="utf-8") as f:
        wf = json.load(f)

    api_graph = to_api(wf)
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
