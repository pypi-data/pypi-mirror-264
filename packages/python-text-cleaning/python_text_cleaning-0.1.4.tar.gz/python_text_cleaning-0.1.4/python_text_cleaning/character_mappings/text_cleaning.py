import abc
import logging
import re
import string
from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

from beartype.vale import Is

from python_text_cleaning.character_mappings.not_str_translatable_maps import (
    SAME_SAME_BUT_DIFFERENT,
)

logger = logging.getLogger(
    __name__.replace("_", "."),
)  # "The name is potentially a period-separated hierarchical", see: https://docs.python.org/3.10/library/logging.html

NeStr = Annotated[str, Is[lambda s: len(s) > 0]]


class PluginNameConflictError(BaseException):
    """more than 1 plugin of same name"""


def register_normalizer_plugin(name: str) -> Callable:
    """
    TODO: why not simple single-ton instead?
    all these "plugins" get instantiated during import-time! is this really what I want?
    """
    if name in CHARACTER_MAPPINGS:
        msg = f"you have more than one TextNormalizer of name {name}"
        raise PluginNameConflictError(
            msg,
        )

    def register_wrapper(
        clazz: type[CharacterMapping],
    ) -> (
        Callable
    ):  # TODO: why does beartype whant another callable? isn't this already the decorator?
        plugin = clazz()
        CHARACTER_MAPPINGS[name] = plugin
        logger.info(f"registered {plugin.name}")
        return clazz

    return register_wrapper


@dataclass  # being a dataclass enable (de)-serialization
class TextCleaner(abc.ABC):
    @property
    def name(self) -> NeStr:
        return self.__class__.__name__

    @abc.abstractmethod
    def __call__(self, text: str) -> str:
        pass


@dataclass  # being a dataclass enable (de)-serialization
class CharacterMapping(TextCleaner):
    @property
    @abc.abstractmethod
    def mapping(self) -> dict[str, str]:
        pass

    def __init__(self) -> None:
        # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        self.table = str.maketrans(self.mapping)

    @property
    def replace_mapping(self) -> dict[str, str]:
        return SAME_SAME_BUT_DIFFERENT

    def __call__(self, text: str) -> str:
        for k, v in self.replace_mapping.items():
            text = text.replace(k, v)
        text = text.translate(self.table)
        return re.sub(r"\s+", " ", text)


CHARACTER_MAPPINGS: dict[str, CharacterMapping] = {}
TEXT_CLEANERS: dict[str, TextCleaner] = CHARACTER_MAPPINGS  # TODO: use this in future?


@register_normalizer_plugin("none")  # noqa: NEW100 -> false positive!
class NoCharacterMappingAtAll(CharacterMapping):
    @property
    def mapping(self) -> dict[str, str]:
        return {}


@register_normalizer_plugin("none_lower_veryfirst")  # noqa: NEW100 -> false positive!
class NoCharacterMappingAtAllLowerVeryFirst(CharacterMapping):
    @property
    def mapping(self) -> dict[str, str]:
        return {}

    def __call__(self, text: str) -> str:
        if len(text) > 0:
            text = text[0].lower() + text[1:]
        return super().__call__(text)


@register_normalizer_plugin("no_punct")  # noqa: NEW100 -> false positive!
class NoPunctuation(CharacterMapping):
    @property
    def mapping(self) -> dict[str, str]:
        PUNCTUATION = string.punctuation + "„“’”'-—…"  # noqa: RUF001
        return {key: " " for key in PUNCTUATION}
