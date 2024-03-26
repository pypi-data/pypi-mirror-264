from python_text_cleaning.character_mappings.latin_character_maps import (
    NORMALIZE_DASH,
    REMOVE_EVERYTHING,
    REPLACE_ALL_PUNCT_WITH_SPACE,
)
from python_text_cleaning.character_mappings.text_cleaning import (
    CharacterMapping,
    register_normalizer_plugin,
)

german_white_list = {"ä", "ü", "ö", "ß"}

german_mapping = {
    k: v
    for k, v in (
        REMOVE_EVERYTHING | REPLACE_ALL_PUNCT_WITH_SPACE | NORMALIZE_DASH
    ).items()
    if k not in german_white_list
}


@register_normalizer_plugin("de")
class GermanTextNormalizer(CharacterMapping):
    @property
    def mapping(self) -> dict[str, str]:
        return german_mapping


@register_normalizer_plugin("de_no_sz")
class GermanTextCleanerNoSz(CharacterMapping):
    @property
    def replace_mapping(self) -> dict[str, str]:
        return super().replace_mapping | {"ß": "ss"}

    @property
    def mapping(self) -> dict[str, str]:
        return german_mapping
