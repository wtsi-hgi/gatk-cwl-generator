import string


TESTED_VERSIONS = [
    "3.5-0",
    "3.8-0",
    "4.0.0.0",
    "4.0.6.0",
    "4.0.7.0",
]


ALLOWED_INITIAL_CHARACTERS = string.ascii_letters
ALLOWED_CHARACTERS = ALLOWED_INITIAL_CHARACTERS + string.digits + "_"


def escape_for_mark(s: str, initial_char: str = None) -> str:
    """Escape a string to be used as a pytest mark name.

    Pytest uses eval() at various points to process marks, so they must
    be valid Python identifiers; usually, this would be enforced by the
    Python interpreter itself (since marks are created by referring to
    an attribute of `pytest.mark`), but if using getattr() to create
    marks dynamically, this restriction is not in place.
    """
    if not s:
        raise ValueError("Mark names cannot be empty")
    if initial_char is None:
        initial_char, s = s[0], s[1:]
    if initial_char not in ALLOWED_INITIAL_CHARACTERS:
        raise ValueError(f"Initial character {initial_char!r} not permitted in mark names")
    return initial_char + "".join(
        c if c in ALLOWED_CHARACTERS else "_" for c in s
    )
