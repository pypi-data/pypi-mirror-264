from python_text_cleaning.character_mappings.cyrillic_character_maps import (
    NO_JO,
    RECOVER_CYRILLIC,
)
from python_text_cleaning.character_mappings.latin_character_maps import (
    NORMALIZE_APOSTROPHES,
    NORMALIZE_DASH,
    REMOVE_EVERYTHING,
    REPLACE_ALL_PUNCT_WITH_SPACE,
)
from python_text_cleaning.character_mappings.not_str_translatable_maps import (
    SAME_SAME_BUT_DIFFERENT,
)
from python_text_cleaning.character_mappings.text_cleaning import (
    CharacterMapping,
    register_normalizer_plugin,
)


@register_normalizer_plugin("ru")
class RussianTextNormalizer(CharacterMapping):
    @property
    def replace_mapping(self) -> dict[str, str]:
        multiletter = {
            "ch": "ч",
            "sh": "ш",  # cannot map multi-letter here
            # "sh": "щ",
            "you": "ю",
            "ja": "я",
            "th": "д",
        }
        return SAME_SAME_BUT_DIFFERENT | multiletter

    @property
    def mapping(self) -> dict[str, str]:
        white_list = {}
        return {
            k: v
            for k, v in (
                REMOVE_EVERYTHING
                | REPLACE_ALL_PUNCT_WITH_SPACE
                | RECOVER_CYRILLIC
                | NO_JO
            ).items()
            if k not in white_list
        }


@register_normalizer_plugin("es")
class SpanishTextNormalizer(CharacterMapping):
    @property
    def mapping(self) -> dict[str, str]:
        SPANISH_WHITE_LIST = {"ñ", "ü", "ö", "á", "é", "í", "ó", "ú"}
        SPANISH_CHARACTER_MAPPING = {
            k: v for k, v in REMOVE_EVERYTHING.items() if k not in SPANISH_WHITE_LIST
        }
        return {**SPANISH_CHARACTER_MAPPING, **REPLACE_ALL_PUNCT_WITH_SPACE}


@register_normalizer_plugin("en")
class EnglishTextNormalizer(CharacterMapping):
    @property
    def mapping(self) -> dict[str, str]:
        english_white_list = ["-", "'"]
        return {
            k: v
            for k, v in (
                REMOVE_EVERYTHING
                | REPLACE_ALL_PUNCT_WITH_SPACE
                | NORMALIZE_APOSTROPHES
                | NORMALIZE_DASH
            ).items()
            if k not in english_white_list
        }
