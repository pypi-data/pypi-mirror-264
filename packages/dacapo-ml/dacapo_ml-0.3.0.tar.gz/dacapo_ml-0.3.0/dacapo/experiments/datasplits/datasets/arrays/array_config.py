import attr

from typing import Tuple


@attr.s
class ArrayConfig:
    """Base class for array configurations. Each subclass of an
    `Array` should have a corresponding config class derived from
    `ArrayConfig`.
    """

    name: str = attr.ib(
        metadata={
            "help_text": "A unique name for this array. This will be saved so you "
            "and others can find and reuse this array. Keep it short "
            "and avoid special characters."
        }
    )

    def verify(self) -> Tuple[bool, str]:
        """
        Check whether this is a valid Array
        """
        return True, "No validation for this Array"
