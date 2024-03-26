"""."""

import re


def get_file_name(txt: str) -> str:
    """."""
    return re.sub(r'\W+', '-', txt).lower()

