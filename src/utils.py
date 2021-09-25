# Python imports
from enum import Enum
from typing import Tuple, TypeVar


class Op(Enum):
    """Enum representing the two types of update operations in dynamic SSE schemes: add and delete."""
    ADD = 1
    DEL = 2

    def __eq__(
            self,
            other: Enum,
    ) -> bool:
        """Comparison method.

        :param other: the operation to compare this operation to
        :type other: Enum (Op)
        :returns: whether the other operation is equal to this operation
        :rtype: bool
        """
        return self.value == other.value


"""Generics for Add and Search tokens."""
AddToken = TypeVar('AddToken')
SrchToken = TypeVar('SrchToken')


"""Type declaration for Libertas updates, (t, op, ind, w) tuples."""
Update = Tuple[int, Op, int, str]
