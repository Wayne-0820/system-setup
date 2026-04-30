"""
One-shot script to generate Wan 2.2 A14B T2V/I2V 合一 workflow JSON.
Outputs:
  D:\\Work\\system-setup\\comfyui-workflows\\Wan2.2_A14B_T2V-I2V合一_720P_81幀.json (frontend format)
  /tmp/wan22_prompt_t2v.json (prompt API format, T2V smoke)
  /tmp/wan22_prompt_i2v.json (prompt API format, I2V smoke)
"""
import json
import os

# Node specs: id -> (class_type, widgets_values, inputs_dict, outputs_types, pos, size)
# inputs_dict: name -> ("link", src_node_id, src_slot) or ("widget", index)

OUT_DIR = r"D:\Work\system-setup\comfyui-workflows"
OUT_FILE = "Wan2.2_A14B_T2V-I2V合一_720P_81幀_4步.json"

WIDTH, HEIGHT, NUM_FRAMES = 1280, 720, 81
TOTAL_STEPS = 4  # Lightx2v 4-step distilled schedule
HIGH_END_STEP = 2  # HIGH samples step 0..2, LOW samples step 2..end
CFG = 1.0  # distilled models use cfg=1.0 (no classifier-free guidance)

# LoRA filenames (with wan22-lightning\ subfolder prefix as ComfyUI lists them)
T2V_LORA_HIGH = r"wan22-lightning\Wan22_A14B_T2V_HIGH_Lightning_4steps_lora_250928_rank128_fp16.safetensors"
T2V_LORA_LOW = r"wan22-lightning\Wan22_A14B_T2V_LOW_Lightning_4steps_lora_250928_rank64_fp16.safetensors"
I2V_LORA_HIGH = r"wan22-lightning\Wan2.2-Lightning_I2V-A14B-4steps-lora_HIGH_fp16.safetensors"
I2V_LORA_LOW = r"wan22-lightning\Wan2.2-Lightning_I2V-A14B-4steps-lora_LOW_fp16.safetensors"

# === node defs ===
# format: dict per node — id, type, widgets_values, link_inputs (name -> (src_node_id, src_slot, type)), output_types, pos, size, mode
nodes_def = [
    # Node 1: HIGH model loader (sageattn, no BlockSwap, no compile, +HIGH Lightx2v LoRA)
    {
        "id": 1, "type": "WanVideoModelLoader",
        "widgets": ["Wan2_2-T2V-A14B_HIGH_fp8_e4m3fn_scaled_KJ.safetensors", "fp16", "fp8_e4m3fn_scaled", "offload_device", "sageattn"],
        "outputs": [("model", "WANVIDEOMODEL")],
        "link_inputs": {"lora": (16, 0, "WANVIDLORA")},
        "pos": [50, 50], "size": [400, 200], "mode": 0,
    },
    # Node 2: LOW model loader (sageattn, no BlockSwap, no compile, +LOW Lightx2v LoRA)
    {
        "id": 2, "type": "WanVideoModelLoader",
        "widgets": ["Wan2_2-T2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors", "fp16", "fp8_e4m3fn_scaled", "offload_device", "sageattn"],
        "outputs": [("model", "WANVIDEOMODEL")],
        "link_inputs": {"lora": (17, 0, "WANVIDLORA")},
        "pos": [50, 280], "size": [400, 200], "mode": 0,
    },
    # Node 3: T5 text encoder
    {
        "id": 3, "type": "LoadWanVideoT5TextEncoder",
        "widgets": ["umt5-xxl-enc-fp8_e4m3fn.safetensors", "bf16", "offload_device", "fp8_e4m3fn"],
        "outputs": [("wan_t5_model", "WANTEXTENCODER")],
        "link_inputs": {},
        "pos": [50, 510], "size": [400, 150], "mode": 0,
    },
    # Node 4: VAE loader
    {
        "id": 4, "type": "WanVideoVAELoader",
        "widgets": ["Wan2_1_VAE_bf16.safetensors", "bf16"],
        "outputs": [("vae", "WANVAE")],
        "link_inputs": {},
        "pos": [50, 690], "size": [400, 100], "mode": 0,
    },
    # Node 5: WanVideoTextEncode
    {
        "id": 5, "type": "WanVideoTextEncode",
        "widgets": [
            "A red panda balancing on a bamboo stem in a forest, cinematic, high quality nature footage",
            "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量",
            True, False, "gpu"
        ],
        "outputs": [("text_embeds", "WANVIDEOTEXTEMBEDS")],
        "link_inputs": {"t5": (3, 0, "WANTEXTENCODER")},
        "pos": [500, 510], "size": [450, 280], "mode": 0,
    },
    # Node 6: WanVideoEmptyEmbeds (T2V branch, ENABLED by default)
    {
        "id": 6, "type": "WanVideoEmptyEmbeds",
        "widgets": [WIDTH, HEIGHT, NUM_FRAMES],
        "outputs": [("image_embeds", "WANVIDIMAGE_EMBEDS")],
        "link_inputs": {},
        "pos": [500, 50], "size": [350, 130], "mode": 0,
    },
    # Node 7: LoadImage (I2V branch, BYPASSED by default for T2V)
    {
        "id": 7, "type": "LoadImage",
        "widgets": ["example.png", "image"],
        "outputs": [("IMAGE", "IMAGE"), ("MASK", "MASK")],
        "link_inputs": {},
        "pos": [500, 220], "size": [320, 280], "mode": 4,  # bypass
    },
    # Node 8: ImageResizeKJv2 (I2V branch, BYPASSED)
    {
        "id": 8, "type": "ImageResizeKJv2",
        "widgets": [WIDTH, HEIGHT, "lanczos", "crop", "0, 0, 0", "center", 16],
        "outputs": [("IMAGE", "IMAGE"), ("width", "INT"), ("height", "INT"), ("mask", "MASK")],
        "link_inputs": {"image": (7, 0, "IMAGE")},
        "pos": [870, 220], "size": [280, 280], "mode": 4,
    },
    # Node 9: WanVideoImageToVideoEncode (I2V branch, BYPASSED)
    {
        "id": 9, "type": "WanVideoImageToVideoEncode",
        "widgets": [WIDTH, HEIGHT, NUM_FRAMES, 0.0, 1.0, 1.0, True],
        "outputs": [("image_embeds", "WANVIDIMAGE_EMBEDS")],
        "link_inputs": {
            "vae": (4, 0, "WANVAE"),
            "start_image": (8, 0, "IMAGE"),
        },
        "pos": [1170, 220], "size": [350, 280], "mode": 4,
    },
    # Node 10: Any Switch (rgthree) — image_embeds muxer
    {
        "id": 10, "type": "Any Switch (rgthree)",
        "widgets": [],
        "outputs": [("*", "*")],
        "link_inputs": {
            "any_t2v": (6, 0, "*"),
            "any_i2v": (9, 0, "*"),
        },
        "pos": [1550, 50], "size": [220, 120], "mode": 0,
    },
    # Node 11: WanVideoSampler HIGH
    {
        "id": 11, "type": "WanVideoSampler",
        # widget order: steps, cfg, shift, seed, control_after_generate(hidden), force_offload, scheduler, riflex_freq_index, denoise_strength, batched_cfg, rope_function, start_step, end_step, add_noise_to_samples
        "widgets": [TOTAL_STEPS, CFG, 5.0, 42, "fixed", True, "unipc", 0, 1.0, False, "comfy", 0, HIGH_END_STEP, False],
        "outputs": [("samples", "LATENT"), ("denoised_samples", "LATENT")],
        "link_inputs": {
            "model": (1, 0, "WANVIDEOMODEL"),
            "image_embeds": (10, 0, "WANVIDIMAGE_EMBEDS"),
            "text_embeds": (5, 0, "WANVIDEOTEXTEMBEDS"),
        },
        "pos": [1820, 50], "size": [350, 600], "mode": 0,
    },
    # Node 12: WanVideoSampler LOW
    {
        "id": 12, "type": "WanVideoSampler",
        "widgets": [TOTAL_STEPS, CFG, 5.0, 42, "fixed", True, "unipc", 0, 1.0, False, "comfy", HIGH_END_STEP, -1, False],
        "outputs": [("samples", "LATENT"), ("denoised_samples", "LATENT")],
        "link_inputs": {
            "model": (2, 0, "WANVIDEOMODEL"),
            "image_embeds": (10, 0, "WANVIDIMAGE_EMBEDS"),
            "text_embeds": (5, 0, "WANVIDEOTEXTEMBEDS"),
            "samples": (11, 0, "LATENT"),
        },
        "pos": [2200, 50], "size": [350, 600], "mode": 0,
    },
    # Node 13: WanVideoDecode
    {
        "id": 13, "type": "WanVideoDecode",
        "widgets": [False, 272, 272, 144, 128],
        "outputs": [("images", "IMAGE")],
        "link_inputs": {
            "vae": (4, 0, "WANVAE"),
            "samples": (12, 0, "LATENT"),
        },
        "pos": [2580, 50], "size": [320, 250], "mode": 0,
    },
    # Node 14: SaveAnimatedWEBP
    {
        "id": 14, "type": "SaveAnimatedWEBP",
        "widgets": ["Wan2.2_A14B_T2V-I2V_4step", 16.0, False, 80, "default"],
        "outputs": [],
        "link_inputs": {"images": (13, 0, "IMAGE")},
        "pos": [2580, 330], "size": [400, 250], "mode": 0,
    },
    # Node 16: HIGH LoRA (T2V default; switched to I2V LoRA in i2v API mode)
    {
        "id": 16, "type": "WanVideoLoraSelect",
        "widgets": [T2V_LORA_HIGH, 1.0],
        "outputs": [("lora", "WANVIDLORA")],
        "link_inputs": {},
        "pos": [50, 800], "size": [400, 130], "mode": 0,
    },
    # Node 17: LOW LoRA (T2V default; switched to I2V LoRA in i2v API mode)
    {
        "id": 17, "type": "WanVideoLoraSelect",
        "widgets": [T2V_LORA_LOW, 1.0],
        "outputs": [("lora", "WANVIDLORA")],
        "link_inputs": {},
        "pos": [50, 950], "size": [400, 130], "mode": 0,
    },
]

# === build frontend format ===
def build_frontend(nodes_def):
    nodes = []
    links = []
    link_id_counter = 1
    # output_links: (src_node, src_slot) -> [link_ids]
    output_links_map = {}

    # Build links first to know each output's link IDs
    for node in nodes_def:
        for inp_name, (src_node, src_slot, t) in node["link_inputs"].items():
            link_id = link_id_counter
            link_id_counter += 1
            links.append([link_id, src_node, src_slot, node["id"], len(node["link_inputs"]), t])
            key = (src_node, src_slot)
            output_links_map.setdefault(key, []).append(link_id)

    # Now rebuild links with correct dst_slot index per node
    links = []
    link_id_counter = 1
    output_links_map = {}
    # Need to first calc dst_slot from inputs_array order. But inputs_array also includes widget inputs (with widget marker).
    # Simplification: only link inputs go in dst_slot order based on enumeration.

    for node in nodes_def:
        # build inputs array: only link inputs (no widget markers, like example format)
        inputs_arr = []
        for slot_idx, (inp_name, (src_node, src_slot, t)) in enumerate(node["link_inputs"].items()):
            link_id = link_id_counter
            link_id_counter += 1
            links.append([link_id, src_node, src_slot, node["id"], slot_idx, t])
            output_links_map.setdefault((src_node, src_slot), []).append(link_id)
            inputs_arr.append({"name": inp_name, "type": t, "link": link_id})
        node["_inputs_arr"] = inputs_arr

    # Build outputs array with link references
    for node in nodes_def:
        outputs_arr = []
        for slot_idx, (out_name, t) in enumerate(node["outputs"]):
            lks = output_links_map.get((node["id"], slot_idx), [])
            outputs_arr.append({
                "name": out_name, "type": t,
                "links": lks if lks else None,
            })
        node["_outputs_arr"] = outputs_arr

    # Assemble nodes
    for n in nodes_def:
        nodes.append({
            "id": n["id"],
            "type": n["type"],
            "pos": n["pos"],
            "size": n["size"],
            "flags": {},
            "order": n["id"] - 1,
            "mode": n["mode"],
            "inputs": n["_inputs_arr"],
            "outputs": n["_outputs_arr"],
            "properties": {"Node name for S&R": n["type"]},
            "widgets_values": n["widgets"],
        })

    return {
        "id": "wan22-a14b-t2v-i2v-mux",
        "revision": 0,
        "last_node_id": max(n["id"] for n in nodes_def),
        "last_link_id": link_id_counter - 1,
        "nodes": nodes,
        "links": links,
        "groups": [
            {"id": 1, "title": "T2V branch (default ON; bypass for I2V)", "bounding": [490, 0, 380, 200], "color": "#3f789e", "font_size": 18, "flags": {}},
            {"id": 2, "title": "I2V branch (default BYPASSED; enable for I2V; remember switch model widgets to I2V-A14B HIGH/LOW)", "bounding": [490, 200, 1050, 320], "color": "#a1309b", "font_size": 18, "flags": {}},
            {"id": 3, "title": "HIGH/LOW two-stage samplers", "bounding": [1810, 0, 760, 680], "color": "#b58b2a", "font_size": 18, "flags": {}},
        ],
        "config": {},
        "extra": {
            "ds": {"scale": 0.6, "offset": [0, 0]},
            "frontendVersion": "1.42.11",
            "node_versions": {
                "ComfyUI-WanVideoWrapper": "HEAD",
                "comfy-core": "0.19.3",
                "ComfyUI-KJNodes": "HEAD",
                "rgthree-comfy": "v1.0.260407001",
            },
        },
        "version": 0.4,
    }


# === build prompt API format ===
def build_prompt_api(nodes_def, mode="t2v"):
    """mode='t2v' bypasses I2V branch (nodes 7/8/9), 'i2v' bypasses T2V branch (node 6) and switches model loaders."""
    # widget order maps for class -> [widget names]
    # control_after_generate is hidden, skip in API
    widget_names_map = {
        "WanVideoModelLoader": ["model", "base_precision", "quantization", "load_device", "attention_mode"],
        "LoadWanVideoT5TextEncoder": ["model_name", "precision", "load_device", "quantization"],
        "WanVideoVAELoader": ["model_name", "precision"],
        "WanVideoTextEncode": ["positive_prompt", "negative_prompt", "force_offload", "use_disk_cache", "device"],
        "WanVideoEmptyEmbeds": ["width", "height", "num_frames"],
        "LoadImage": ["image"],  # second 'image' is hidden upload marker
        "ImageResizeKJv2": ["width", "height", "upscale_method", "keep_proportion", "pad_color", "crop_position", "divisible_by"],
        "WanVideoImageToVideoEncode": ["width", "height", "num_frames", "noise_aug_strength", "start_latent_strength", "end_latent_strength", "force_offload"],
        "WanVideoSampler": ["steps", "cfg", "shift", "seed", "force_offload", "scheduler", "riflex_freq_index", "denoise_strength", "batched_cfg", "rope_function", "start_step", "end_step", "add_noise_to_samples"],
        "WanVideoDecode": ["enable_vae_tiling", "tile_x", "tile_y", "tile_stride_x", "tile_stride_y"],
        "SaveAnimatedWEBP": ["filename_prefix", "fps", "lossless", "quality", "method"],
        "Any Switch (rgthree)": [],
        "WanVideoLoraSelect": ["lora", "strength"],
    }
    # widget index slots that are hidden (not in API): name in widgets_values but skip
    hidden_widget_idx_map = {
        "WanVideoSampler": [4],  # control_after_generate after seed
        "LoadImage": [1],         # second 'image' (upload marker)
    }

    # Determine which nodes to skip per mode (bypass equivalence)
    if mode == "t2v":
        skip_nodes = {7, 8, 9}  # I2V branch
        # model widgets stay as T2V (default)
        model_overrides = {}
    elif mode == "i2v":
        skip_nodes = {6}  # T2V branch
        model_overrides = {
            1: ("model", "Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors"),
            2: ("model", "Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors"),
            16: ("lora", I2V_LORA_HIGH),
            17: ("lora", I2V_LORA_LOW),
        }
    else:
        raise ValueError(mode)

    api = {}
    for node in nodes_def:
        if node["id"] in skip_nodes:
            continue
        cls = node["type"]
        nid = str(node["id"])
        wnames = widget_names_map.get(cls, [])
        wvals = node["widgets"]
        hidden = hidden_widget_idx_map.get(cls, [])

        inputs = {}
        # widgets: skip hidden ones
        wname_iter = iter(wnames)
        for i, v in enumerate(wvals):
            if i in hidden:
                continue
            try:
                k = next(wname_iter)
            except StopIteration:
                break
            inputs[k] = v

        # apply mode-specific overrides
        if node["id"] in model_overrides:
            k, v = model_overrides[node["id"]]
            inputs[k] = v

        # link inputs
        for inp_name, (src_node, src_slot, t) in node["link_inputs"].items():
            if src_node in skip_nodes:
                continue  # broken link, skip
            inputs[inp_name] = [str(src_node), src_slot]

        api[nid] = {"class_type": cls, "inputs": inputs}

    return api


# === main ===
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    fe = build_frontend([dict(n) for n in nodes_def])  # copy to avoid in-place mutation
    out_path = os.path.join(OUT_DIR, OUT_FILE)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fe, f, ensure_ascii=False, indent=2)
    print(f"Frontend JSON -> {out_path} ({os.path.getsize(out_path)} bytes)")

    api_t2v = build_prompt_api(nodes_def, "t2v")
    with open("/tmp/wan22_prompt_t2v.json", "w", encoding="utf-8") as f:
        json.dump(api_t2v, f, ensure_ascii=False, indent=2)
    print(f"T2V prompt API -> /tmp/wan22_prompt_t2v.json ({len(api_t2v)} nodes)")

    api_i2v = build_prompt_api(nodes_def, "i2v")
    with open("/tmp/wan22_prompt_i2v.json", "w", encoding="utf-8") as f:
        json.dump(api_i2v, f, ensure_ascii=False, indent=2)
    print(f"I2V prompt API -> /tmp/wan22_prompt_i2v.json ({len(api_i2v)} nodes)")


if __name__ == "__main__":
    main()
