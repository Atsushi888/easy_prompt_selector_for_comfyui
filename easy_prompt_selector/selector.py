class EasyPromptSelector:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bangs": ([
                    "short bangs",
                    "long bangs",
                    "blunt bangs",
                    "hime cut",
                    "curtained hair",
                ], {
                    "default": "blunt bangs"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "select"
    CATEGORY = "Easy Prompt Selector"

    def select(self, bangs):
        return (bangs,)
