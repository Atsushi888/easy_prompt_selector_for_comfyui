# Easy Prompt Selector for ComfyUI
# Final unified version (CLIP passthrough + selector text output only)
#
# Folder layout (required):
#   easy_prompt_selector_for_comfyui/
#     ├─ __init__.py
#     └─ ill_hair.yml
#
# Dependencies:
#   pip install pyyaml

from pathlib import Path
from typing import Dict, Any, List, Tuple

try:
    import yaml
except Exception as e:
    raise RuntimeError(
        "[EasyPromptSelector] Missing dependency: pyyaml (pip install pyyaml)"
    ) from e


# -----------------------------
# Load YAML once
# -----------------------------
YAML_PATH = Path(__file__).with_name("ill_hair.yml")

if not YAML_PATH.exists():
    raise FileNotFoundError(f"[EasyPromptSelector] ill_hair.yml not found: {YAML_PATH}")

with YAML_PATH.open("r", encoding="utf-8") as f:
    DB = yaml.safe_load(f) or {}

if not isinstance(DB, dict):
    raise ValueError("[EasyPromptSelector] ill_hair.yml must be a mapping (dict).")

CATEGORIES: List[str] = list(DB.keys())


def _dropdown(cat: str) -> Tuple[List[str], Dict[str, str]]:
    """
    Returns:
      options: list of labels for the UI dropdown
      mapping: label -> prompt string
    """
    entries = DB.get(cat, {}) or {}
    if not isinstance(entries, dict):
        entries = {}

    skip = "— (skip)"
    options = [skip] + list(entries.keys())

    mapping = {skip: ""}
    for k, v in entries.items():
        mapping[str(k)] = "" if v is None else str(v)

    return options, mapping


def _join(parts: List[str]) -> str:
    return ", ".join(p.strip() for p in parts if isinstance(p, str) and p.strip())


# -----------------------------
# Main Node (CLIP passthrough)
# -----------------------------
class EasyPromptSelector:
    @classmethod
    def INPUT_TYPES(cls):
        required: Dict[str, Any] = {
            # CLIP passthrough (required)
            "clip": ("CLIP",),
        }

        # Build dropdowns from YAML categories
        cls._maps: Dict[str, Dict[str, str]] = {}
        for cat in CATEGORIES:
            opts, m = _dropdown(cat)
            required[cat] = (opts, {"default": opts[0]})
            cls._maps[cat] = m

        return {"required": required}

    # Return clip unchanged + generated selector text
    RETURN_TYPES = ("CLIP", "STRING")
    RETURN_NAMES = ("clip", "text")
    FUNCTION = "run"
    CATEGORY = "EasyPromptSelector"

    def run(self, clip, **kwargs):
        parts: List[str] = []

        for cat in CATEGORIES:
            label = kwargs.get(cat, "— (skip)")
            prompt = self._maps.get(cat, {}).get(label, "")
            if prompt:
                parts.append(prompt)

        final_text = _join(parts)
        return (clip, final_text)


# -----------------------------
# ComfyUI registry
# -----------------------------
NODE_CLASS_MAPPINGS = {
    "EasyPromptSelector": EasyPromptSelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyPromptSelector": "Easy Prompt Selector (CLIP passthrough)",
}
