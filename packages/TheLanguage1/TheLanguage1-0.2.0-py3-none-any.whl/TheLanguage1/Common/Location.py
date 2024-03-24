# ----------------------------------------------------------------------
# |
# |  Location.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-02-11 14:03:11
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Location object"""

from dataclasses import dataclass
from functools import cached_property


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Location:
    """Location within a source file"""

    # ----------------------------------------------------------------------
    line: int
    column: int

    # ----------------------------------------------------------------------
    def __post_init__(self):
        if self.line < 1:
            raise ValueError("Invalid line")
        if self.column < 1:
            raise ValueError("Invalid column")

    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        return self._string

    # ----------------------------------------------------------------------
    @staticmethod
    def Compare(
        this: "Location",
        that: "Location",
    ) -> int:
        result = this.line - that.line
        if result != 0:
            return result

        result = this.column - that.column
        if result != 0:
            return result

        return 0

    # ----------------------------------------------------------------------
    def __eq__(self, other) -> bool:
        return isinstance(other, Location) and self.__class__.Compare(self, other) == 0

    def __ne__(self, other) -> bool:
        return not isinstance(other, Location) or self.__class__.Compare(self, other) != 0

    def __lt__(self, other) -> bool:
        return isinstance(other, Location) and self.__class__.Compare(self, other) < 0

    def __le__(self, other) -> bool:
        return isinstance(other, Location) and self.__class__.Compare(self, other) <= 0

    def __gt__(self, other) -> bool:
        return isinstance(other, Location) and self.__class__.Compare(self, other) > 0

    def __ge__(self, other) -> bool:
        return isinstance(other, Location) and self.__class__.Compare(self, other) >= 0

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @cached_property
    def _string(self) -> str:
        return "line {}, column {}".format(self.line, self.column)
