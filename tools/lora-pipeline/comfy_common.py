#!/usr/bin/env python
"""Shared plumbing for the ComfyUI-driven LoRA pipeline scripts.

Design: each generation route stays its OWN script (sdxl_bootstrap.py,
flux_kontext.py, ...) because the routes are fundamentally different pipelines
(IPAdapter bootstrap vs Kontext in-context edit, different graphs/conditioning).
They only SHARE this transport layer, so the boilerplate (submit / poll / stage)
is written once and a bug here is fixed once.

Stdlib only (json, urllib, shutil) -> runs on any Python 3.8+, no installs.
"""
import json
import os
import shutil
import time
import urllib.request


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def stage_reference(ref, input_dir):
    """Copy an absolute reference path into ComfyUI/input and return the basename
    (ComfyUI LoadImage only sees files inside its input dir). If `ref` is already a
    bare filename, return it unchanged."""
    input_dir = (input_dir or "").strip()
    if os.path.isabs(ref) and os.path.exists(ref) and input_dir:
        base = os.path.basename(ref)
        dst = os.path.join(input_dir, base)
        if os.path.abspath(ref) != os.path.abspath(dst):
            shutil.copyfile(ref, dst)
        return base
    return ref


def stage_references(refs, input_dir):
    """Stage one or many references. Accepts a str OR a list of str; returns a LIST of
    staged basenames (ComfyUI input filenames). Backward compatible: a single string
    yields a one-element list."""
    if isinstance(refs, str):
        refs = [refs]
    out = []
    for r in (refs or []):
        if isinstance(r, str) and r.strip():
            out.append(stage_reference(r.strip(), input_dir))
    return out


def submit(url, graph, client_id="lora-pipeline"):
    """POST a prompt graph to ComfyUI; return the parsed response (has prompt_id)."""
    body = json.dumps({"prompt": graph, "client_id": client_id}).encode("utf-8")
    req = urllib.request.Request(url.rstrip("/") + "/prompt", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def queue_empty(url):
    with urllib.request.urlopen(url.rstrip("/") + "/queue", timeout=10) as r:
        q = json.loads(r.read().decode("utf-8"))
    return not q.get("queue_running") and not q.get("queue_pending")


def wait_for_drain(url, max_polls=300, interval=4):
    """Block until the ComfyUI queue is empty. Returns True on drain, False on timeout."""
    for _ in range(max_polls):
        try:
            if queue_empty(url):
                return True
        except Exception:  # noqa: BLE001
            pass
        time.sleep(interval)
    return False
