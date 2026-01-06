from __future__ import annotations

from pathlib import Path
import re

import yaml


# =========================================
# Config
# =========================================

HERE = Path(__file__).resolve().parent
YAML_PATH = HERE / "ill_hair.yml"

# 「起動時に自動で先頭が選択されるカテゴリ」
# ※ ill_hair.yml のトップレベルキー名と一致させること
DEFAULT_AUTO_SELECT_CATEGORIES = [
    "前髪",
    "髪色（単色）",
    # "髪の長さ",
]


# =========================================
# YAML load (once at import)
# =========================================

def _load_yaml() -> dict:
    if not YAML_PATH.exists():
        raise FileNotFoundError(f"Missing YAML file: {YAML_PATH}")

    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError("ill_hair.yml: root must be a mapping (dict).")

    # 各カテゴリも dict であることを期待。違ったら空dictにする（落とさない）
    for k, v in list(data.items()):
        if not isinstance(v, dict):
            data[k] = {}

    return data


DATA = _load_yaml()


# =========================================
# Field name mapping (category -> safe key)
# =========================================

def _safe_field_name(category: str) -> str:
    """
    Convert category label to a safe ASCII-ish field key for ComfyUI INPUT_TYPES.
    Japanese category names are fine as display, but dict keys are safer in ASCII.
    """
    s = category.strip()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^0-9A-Za-z_]", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "category"


# category name -> field key (avoid collisions)
CAT_TO_FIELD: dict[str, str] = {}
used = set()
for cat in DATA.keys():
    cat = str(cat)
    base = _safe_field_name(cat)
    name = base
    i = 2
    while name in used:
        name = f"{base}_{i}"
        i += 1
    used.add(name)
    CAT_TO_FIELD[cat] = name

FIELD_TO_CAT = {field: cat for cat, field in CAT_TO_FIELD.items()}


# =========================================
# Node: "All-in-one" selector
# =========================================

def _build_inputs():
    """
    Build ComfyUI inputs dynamically from YAML.
    - For auto-select categories: dropdown has no "" option, default is labels[0]
    - For optional categories: dropdown includes "" (means 'not selected')
    """
    req = {
        "delimiter": ("STRING", {"default": ", "}),
        "trim_spaces": ("BOOLEAN", {"default": True}),
    }

    for cat, field in CAT_TO_FIELD.items():
        items = DATA.get(cat, {})
        labels = list(items.keys())

        if cat in DEFAULT_AUTO_SELECT_CATEGORIES and labels:
            req[field] = (labels, {"default": labels[0]})
        else:
            req[field] = ([""] + labels, {"default": ""})

    return {"required": req}


class EasyPromptSelectorAllHairFromYAML:
    @classmethod
    def INPUT_TYPES(cls):
        return _build_inputs()

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build"
    CATEGORY = "Easy Prompt Selector"

    def build(self, delimiter=", ", trim_spaces=True, **kwargs):
        parts = []

        # kwargs: field_key -> selected_label
        for field, selected_label in kwargs.items():
            if not selected_label:
                continue

            cat = FIELD_TO_CAT.get(field)
            if not cat:
                continue

            prompt = DATA.get(cat, {}).get(selected_label, "")
            if prompt:
                parts.append(prompt)

        sep = delimiter
        if trim_spaces:
            sep = sep.strip()
            # " , " みたいな事故を避けて、区切り後ろを1スペースに寄せる
            if sep and not sep.endswith(" "):
                sep = sep + " "

        return (sep.join(parts),)


NODE_CLASS_MAPPINGS = {
    "EasyPromptSelectorAllHairFromYAML": EasyPromptSelectorAllHairFromYAML,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyPromptSelectorAllHairFromYAML": "Easy Prompt Selector (All Hair from YAML)",
}
