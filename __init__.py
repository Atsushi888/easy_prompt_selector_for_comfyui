# Easy Prompt Selector for ComfyUI
# - Loads ill_hair.yml once at import
# - Provides:
#   1) Standalone selector (no input)
#   2) Selector with base_prompt input (recommended)

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Tuple, List

try:
    import yaml
except Exception as e:
    raise RuntimeError(
        "[EasyPromptSelector] Missing dependency: pyyaml. Install it with: pip install pyyaml"
    ) from e


# -----------------------------
# YAML loader (loaded once)
# -----------------------------
YAML_PATH = Path(__file__).with_name("ill_hair.yml")

if not YAML_PATH.exists():
    raise FileNotFoundError(f"[EasyPromptSelector] ill_hair.yml not found: {YAML_PATH}")

with YAML_PATH.open("r", encoding="utf-8") as f:
    RAW_DB: Dict[str, Dict[str, str]] = yaml.safe_load(f) or {}

# Expect: { category: { label: prompt_str, ... }, ... }
if not isinstance(RAW_DB, dict):
    raise ValueError("[EasyPromptSelector] ill_hair.yml must be a mapping (dict).")

# Normalize categories order (keep YAML order as loaded)
CATEGORIES: List[str] = list(RAW_DB.keys())


def _build_dropdown_options_for_category(cat: str) -> Tuple[List[str], Dict[str, str]]:
    """
    Returns:
      - options: list of labels displayed in UI
      - label_to_prompt: mapping label -> prompt string
    """
    entries = RAW_DB.get(cat, {})
    if not isinstance(entries, dict):
        entries = {}

    # Special option to skip this category
    SKIP_LABEL = "— (skip)"
    options = [SKIP_LABEL] + list(entries.keys())

    label_to_prompt = {SKIP_LABEL: ""}
    for label, prompt in entries.items():
        label_to_prompt[str(label)] = "" if prompt is None else str(prompt)

    return options, label_to_prompt


def _join_prompts(parts: List[str], sep: str = ", ") -> str:
    cleaned = [p.strip() for p in parts if isinstance(p, str) and p.strip()]
    return sep.join(cleaned)


# -----------------------------
# Node: Standalone (no input)
# -----------------------------
class EasyPromptSelectorStandalone:
    @classmethod
    def INPUT_TYPES(cls):
        required: Dict[str, Any] = {}
        cls._maps: Dict[str, Dict[str, str]] = {}

        for cat in CATEGORIES:
            opts, m = _build_dropdown_options_for_category(cat)
            required[cat] = (opts, {"default": opts[0]})
            cls._maps[cat] = m

        return {"required": required}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "run"
    CATEGORY = "EasyPromptSelector"

    def run(self, **kwargs):
        parts = []
        for cat in CATEGORIES:
            label = kwargs.get(cat, "— (skip)")
            prompt = self._maps.get(cat, {}).get(label, "")
            if prompt:
                parts.append(prompt)

        final_text = _join_prompts(parts, sep=", ")
        return (final_text,)


# -----------------------------
# Node: With base_prompt input
# -----------------------------
class EasyPromptSelectorWithBasePrompt:
    @classmethod
    def INPUT_TYPES(cls):
        required: Dict[str, Any] = {
            "base_prompt": ("STRING", {"default": "", "multiline": True}),
        }
        cls._maps: Dict[str, Dict[str, str]] = {}

        for cat in CATEGORIES:
            opts, m = _build_dropdown_options_for_category(cat)
            required[cat] = (opts, {"default": opts[0]})
            cls._maps[cat] = m

        return {"required": required}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "run"
    CATEGORY = "EasyPromptSelector"

    def run(self, base_prompt: str = "", **kwargs):
        base = (base_prompt or "").strip()

        parts = []
        if base:
            parts.append(base)

        for cat in CATEGORIES:
            label = kwargs.get(cat, "— (skip)")
            prompt = self._maps.get(cat, {}).get(label, "")
            if prompt:
                parts.append(prompt)

        final_text = _join_prompts(parts, sep=", ")
        return (final_text,)


# -----------------------------
# ComfyUI registry
# -----------------------------
NODE_CLASS_MAPPINGS = {
    "EasyPromptSelectorStandalone": EasyPromptSelectorStandalone,
    "EasyPromptSelectorWithBasePrompt": EasyPromptSelectorWithBasePrompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyPromptSelectorStandalone": "Easy Prompt Selector (Standalone)",
    "EasyPromptSelectorWithBasePrompt": "Easy Prompt Selector (with base_prompt)",
}
