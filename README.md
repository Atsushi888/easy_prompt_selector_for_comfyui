# Easy Prompt Selector For ComfyUI

A simple custom node for ComfyUI that loads `ill_hair.yml` and provides
an all-in-one dropdown selector to build a prompt string.

## Install (RunPod / local ComfyUI)

1. Go to your ComfyUI `custom_nodes` directory:
   - Example: `/workspace/ComfyUI/custom_nodes`

2. Clone this repo:
   ```bash
   git clone https://github.com/<YOUR_GITHUB>/Easy_Prompt_Selector_For_ComfyUI.git

3.	Ensure dependency is installed:
   ```bash
    pip install pyyaml```
4.	Restart ComfyUI.

Auto-select defaults

Edit DEFAULT_AUTO_SELECT_CATEGORIES inside easy_prompt_selector/__init__.py.
Categories listed there will:
	•	not include empty option “”
	•	default to the first item of that category in YAML

Notes
	•	ill_hair.yml is loaded once at import (ComfyUI startup).
	•	If you edit ill_hair.yml, restart ComfyUI to reload.
