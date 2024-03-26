# they need to be imported otherwise they don't get "registred"
from beartype.claw import beartype_this_package

from python_text_cleaning.character_mappings import (  # noqa: F401
    german_text_cleaners,  # noqa: F401
    misc_language_text_cleaners,
)

beartype_this_package()
