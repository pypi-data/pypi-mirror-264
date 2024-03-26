 ```python
import re

from unicode_tr import unicode_tr

from ml4audio.text_processing.character_mappings.latin_character_maps import (
    REMOVE_EVERYTHING,
    REPLACE_ALL_PUNCT_WITH_SPACE,
)
from ml4audio.text_processing.character_mappings.not_str_translatable_maps import (
    SAME_SAME_BUT_DIFFERENT,
)
from ml4audio.text_processing.character_mappings.text_normalization import (
    register_normalizer_plugin,
    TextCleaner,
)


@register_normalizer_plugin("tr")
class TurkishTextCleaner(TextCleaner):
    @property
    def mapping(self) -> dict[str, str]:
        turkish_white_list = ["ç", "ö", "ü", "ğ", "ı", "ş"]

        return {
            k: v for k, v in REMOVE_EVERYTHING.items() if k not in turkish_white_list
        } | REPLACE_ALL_PUNCT_WITH_SPACE

    def __init__(self) -> None:

        # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        self.table = str.maketrans(self.mapping)

    def __call__(self, text: str) -> str:
        text = text.translate(self.table)
        for k, v in SAME_SAME_BUT_DIFFERENT.items():
            text = text.replace(k, v)
        text = re.sub(r"\s+", " ", text)
        instance_of_subclass_of_str_overring_upper_lower_methods = unicode_tr(text)
        return instance_of_subclass_of_str_overring_upper_lower_methods

```