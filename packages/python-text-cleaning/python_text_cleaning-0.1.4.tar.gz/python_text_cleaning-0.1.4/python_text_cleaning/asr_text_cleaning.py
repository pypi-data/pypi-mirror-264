import re
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto

from typing_extensions import Self

from python_text_cleaning.character_mappings.text_cleaning import (
    TEXT_CLEANERS,
    NeStr,
    TextCleaner,
)


class Casing(str, Enum):
    lower = auto()
    upper = auto()
    original = auto()

    def _to_dict(self, skip_keys: list[str] | None = None) -> dict:
        obj = self
        module = obj.__class__.__module__
        _target_ = f"{module}.{obj.__class__.__name__}"
        # TODO: WTF? why _target_ and _id_ stuff here?
        d = {"_target_": _target_, "value": self.value, "_id_": str(id(self))}
        skip_keys = skip_keys if skip_keys is not None else []
        return {k: v for k, v in d.items() if k not in skip_keys}

    def apply(self, text: str) -> str:
        if self in CASING_FUNS.keys():
            fun = CASING_FUNS[self](text)
        else:  # noqa: RET505
            msg = "unknown Casing"
            raise AssertionError(msg)
        return fun

    @staticmethod
    def create(value: str | int) -> Self:
        """
        # TODO: this is only necessary if someone else mis-interprets "1" as an integer! pythons json lib does it correctly -> somewhere in jina??
        """
        return Casing(str(value))


CASING_FUNS: dict[Casing, Callable] = {
    Casing.upper: lambda s: s.upper(),
    Casing.lower: lambda s: s.lower(),
    Casing.original: lambda s: s,
}


Letters = str


def upper_lower_text(text: str, casing: Casing = Casing.original) -> str:
    # first upper than check if in vocab actually makes sense for ß, cause "ß".upper()==SS
    return casing.apply(text)


#
# def casing_vocab_filtering(
#     text: str, vocab_letters: list[str], casing: Casing = Casing.original
# ) -> str:
#     return filter_by_lettervocab(casing.apply(text), vocab_letters)


@dataclass
class VocabCasingAwareTextCleaner(TextCleaner):
    casing: str | dict | Casing
    text_cleaner_name: str
    letter_vocab: Letters

    @property
    def name(self) -> NeStr:
        return f"{self.casing.value.name}-{self.text_cleaner_name}"

    def __post_init__(self) -> None:
        if isinstance(self.casing, str):
            self.casing = Casing(self.casing)
        elif isinstance(
            self.casing,
            dict,
        ):  # TODO: somehow Casing gets not deserialized properly!
            self.casing = Casing.create(int(self.casing["value"]))

    def __call__(self, text: str) -> str:
        text = clean_and_filter_text(
            text,
            self.letter_vocab,
            TEXT_CLEANERS[self.text_cleaner_name],
            self.casing,
        )
        assert "  " not in text, f"{text=}"
        return text


def clean_and_filter_text(
    text: str,
    vocab_letters: str,
    text_cleaner: str | TextCleaner,
    casing: Casing,
) -> str:
    if isinstance(text_cleaner, str):
        text_cleaner = TEXT_CLEANERS[text_cleaner]
    text = clean_upper_lower_text(text, text_cleaner, casing)
    text = filter_by_lettervocab(text, list(vocab_letters))
    return re.sub(
        r"\s\s+",
        " ",
        text,
    )  # \s\s+ -> see jiwer RemoveMultipleSpaces transform


def filter_by_lettervocab(text: str, vocab_letters: list[str]) -> str:
    return "".join([c for c in text if c in vocab_letters or c == " "]).strip(" ")


def clean_upper_lower_text(
    text: str,
    text_cleaner: TextCleaner,
    casing: Casing = Casing.original,
) -> str:
    text = text_cleaner(text).strip(" ")
    return casing.apply(text)


def determine_casing(letter_vocab: Letters) -> Casing:
    more_than_half_is_upper = (
        sum([1 if c.upper() == c else 0 for c in letter_vocab]) > len(letter_vocab) / 2
    )
    return Casing.upper if more_than_half_is_upper else Casing.lower
