
import sys
import subprocess
import random
import string

import math
from time import thread_time
from tokenize import Double

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import socket
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

import time , datetime

from typing import List, Dict, Any

from dataclasses import dataclass, field
from typing import types, Optional, Union, Any, List, Tuple, Dict  # type: ignore[attr-defined]

from parser.nodes import BlockNode, ItemizedExpressionNode
from interpreter.base import Environment

from parser.nodes import UseNode


######################
### COLORS LIBRARY ###
######################

class Colors:
    # ANSI escape codes for colors
    reset = "\033[0m"
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    magenta = "\033[35m"
    cyan = "\033[36m"
    white = "\033[37m"
    bright_black = "\033[90m"
    bright_red = "\033[91m"
    bright_green = "\033[92m"
    bright_yellow = "\033[93m"
    bright_blue = "\033[94m"
    bright_magenta = "\033[95m"
    bright_cyan = "\033[96m"
    bright_white = "\033[97m"

######################
### OBJECT LIBRARY ###
######################

class FarrObject:
    
    def type(self):
        return type(self.value)

    ### TO... COMMANDS ###
    
    def to_string(self):
        return str(self.value)
    
    def toString(self):
        return str(self.value)
    
    def to_int(self):
        return int(self.value)
    
    def toInt(self):
        return int(self.value)
    
    def to_float(self):
        return float(self.value)
    
    def toFloat(self):
        return float(self.value)
    
    def to_list(self):
        return list(self.value)
    
    def toList(self):
        return list(self.value)
    


class ExpressionObject(FarrObject):
    pass


class PassObject(ExpressionObject):
    def __str__(self) -> str:
        """Returns a text as object equivalent."""
        return 'ellipsis'

    def __bool__(self) -> bool:
        """Returns the boolean equivalent of the pass."""
        return False

    def __hash__(self) -> int:
        """Returns zero as the object hash."""
        return 0


class NullObject(ExpressionObject):
    def __str__(self) -> str:
        """Returns `null`."""
        return 'null'

    def __bool__(self) -> bool:
        """Returns the essence of `NullObject`."""
        return False

    def __hash__(self) -> int:
        """Returns zero as the object hash."""
        return 0

    def __eq__(self, other: FarrObject) -> 'BooleanObject':  # type: ignore[override]
        """Compares the equality of nothing with another object."""
        return BooleanObject(value=False == other)  # noqa: E712

    def __ne__(self, other: FarrObject) -> 'BooleanObject':  # type: ignore[override]
        """Compares the inequality of nothing with another object."""
        return BooleanObject(value=False != other)  # noqa: E712

class MathObject(ExpressionObject):
    def __str__(self,num) -> str:
        """Returns `null`."""
        return num

    def __bool__(self,num) -> bool:
        """Returns the essence of `NullObject`."""
        return num

    def __hash__(self,num) -> int:
        """Returns zero as the object hash."""
        return num

    def __eq__(self, other: FarrObject,num) -> 'BooleanObject':  # type: ignore[override]
        """Compares the equality of nothing with another object."""
        return BooleanObject(value=num == other)  # noqa: E712

    def __ne__(self, other: FarrObject,num) -> 'BooleanObject':  # type: ignore[override]
        """Compares the inequality of nothing with another object."""
        return BooleanObject(value=num != other)  # noqa: E712


@dataclass
class HeterogeneousLiteralObject(ExpressionObject):
    value: Any = field(kw_only=True)

    def __str__(self) -> str:
        """Returns the value as a `str`."""
        return str(self.value)

    def __bool__(self) -> bool:
        """Returns the value status as `bool`."""
        return bool(self.value)

    def __hash__(self) -> int:
        """Calculates the hash of the object."""
        return hash(self.value)

    def __eq__(self, other: FarrObject) -> 'BooleanObject':  # type: ignore[override]
        """Checks whether the two values are equal or not."""
        return BooleanObject(value=self.value == other)

    def __ne__(self, other: FarrObject) -> 'BooleanObject':  # type: ignore[override]
        """Checks if the two values are not equal."""
        return BooleanObject(value=self.value != other)

    def __lt__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'BooleanObject':
        """Checks if it is a smaller value or not."""
        if not isinstance(self, (IntegerObject, FloatObject)) or not isinstance(
            other, (IntegerObject, FloatObject)
        ):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `<` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return BooleanObject(value=self.value < other.value)

    def __gt__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'BooleanObject':
        """Checks if the value is greater than or not."""
        if not isinstance(self, (IntegerObject, FloatObject)) or not isinstance(
            other, (IntegerObject, FloatObject)
        ):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `>` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return BooleanObject(value=self.value > other.value)

    def __le__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'BooleanObject':
        """Checks if the value is less than or equal to or not."""
        if not isinstance(self, (IntegerObject, FloatObject)) or not isinstance(
            other, (IntegerObject, FloatObject)
        ):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `<=` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return BooleanObject(value=self.value <= other.value)

    def __ge__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'BooleanObject':
        """Checks if the value is greater than or equal to or not."""
        if not isinstance(self, (IntegerObject, FloatObject)) or not isinstance(
            other, (IntegerObject, FloatObject)
        ):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `>=` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return BooleanObject(value=self.value >= other.value)

    def isin(self, list_: 'ListObject') -> 'BooleanObject':
        """Checks the existence of the object value in the list."""
        return BooleanObject(value=self.value in list_)


class BooleanObject(HeterogeneousLiteralObject):
    def __str__(self) -> str:
        """Converts the value to lowercase letters."""
        return str(self.value).lower()


class IntegerObject(HeterogeneousLiteralObject):
    def __lshift__(self, other: 'IntegerObject') -> 'IntegerObject':
        """Performs bitwise left shift."""
        if not isinstance(other, IntegerObject):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `<<` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return IntegerObject(value=self.value << other.value)

    def __rshift__(self, other: 'IntegerObject') -> 'IntegerObject':
        """Performs bitwise right shift."""
        if not isinstance(other, IntegerObject):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `>>` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return IntegerObject(value=self.value >> other.value)

    def __add__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> Union['IntegerObject', 'FloatObject']:
        """Adds the two values together."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `+` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return other.__class__(value=self.value + other.value)

    def __sub__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> Union['IntegerObject', 'FloatObject']:
        """Subtracts two existing values."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `-` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return other.__class__(value=self.value - other.value)

    def __mul__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> Union['IntegerObject', 'FloatObject']:
        """Multiplies two existing values together."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `*` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return other.__class__(value=self.value * other.value)

    def __truediv__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Divides the existing values."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `/` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return FloatObject(value=self.value / other.value)

    def __mod__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> Union['IntegerObject', 'FloatObject']:
        """Calculates the remainder of the division."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `%` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return other.__class__(value=self.value % other.value)

    def __pow__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> Union['IntegerObject', 'FloatObject']:
        """Calculates the exponentiation."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `^` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return other.__class__(value=self.value**other.value)

    def tostring(self) -> 'StringObject':
        """Converts the value of the object to a string."""
        return StringObject(value=str(self))

class FloatObject(HeterogeneousLiteralObject):
    def __add__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Adds the two values together."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `+` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return FloatObject(value=self.value + other.value)

    def __sub__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Subtracts two existing values."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `-` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return FloatObject(value=self.value - other.value)

    def __mul__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Multiplies two existing values together."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `*` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return FloatObject(value=self.value * other.value)

    def __truediv__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Divides the existing values."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `/` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return FloatObject(value=self.value / other.value)

    def __mod__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Calculates the remainder of the division."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `%` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return FloatObject(value=self.value % other.value)

    def __pow__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Calculates the exponentiation."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            print(f"{Colors.bright_red}   TypeError{Colors.red}",
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `^` with type `{other.__class__.__name__}`!{Colors.reset}'
            )
        return FloatObject(value=self.value**other.value)

    def toint(self) -> IntegerObject:
        """Removes the decimal part and returns an integer."""
        return IntegerObject(value=int(self.value))

    def tostring(self) -> 'StringObject':
        """Converts the value of the object to a string."""
        return StringObject(value=str(self))


class StringObject(HeterogeneousLiteralObject):
    def __getitem__(self, key: 'RangeObject') -> 'StringObject':
        """Returns the characters in the string based on range."""
        if key.from_.value <= 0 or key.by is not None and key.by.value <= 0:  # type: ignore[union-attr]
            raise IndexError('Non-positive indexes are not allowed!{Colors.reset}')
        return (
            StringObject(value=self.value[key.from_.value - 1])  # type: ignore[union-attr]
            if key.to is None and key.by is None
            else StringObject(
                value=self.value[
                    key.from_.value  # type: ignore[union-attr]
                    - 1 : key.to.value if key.to is not None else None : (
                        key.by.value if key.by is not None else None
                    )
                ]
            )
        )

    def __iter__(self) -> 'StringObject':
        """Iterates over the characters of the string."""
        self._index = 0
        return self

    def __next__(self) -> 'StringObject':
        """Returns the next character."""
        if self._index >= len(self.value):
            raise StopIteration
        char = self.value[self._index]
        self._index += 1
        return char

    def toint(self) -> IntegerObject:
        """Converts the value to an integer."""
        return IntegerObject(value=int(self.value))

    def tofloat(self) -> FloatObject:
        """Converts the value to a decimal number."""
        return FloatObject(value=float(self.value))

    def tolower(self) -> 'StringObject':
        """Converts the value to lowercase letters."""
        return StringObject(value=self.value.lower())

    def toupper(self) -> 'StringObject':
        """Converts the value to uppercase."""
        return StringObject(value=self.value.upper())

    def concat(self, object_: FarrObject) -> 'StringObject':
        """Merges the string with another object."""
        return StringObject(value=self.value + str(object_))

    def split(self, separator: Optional['StringObject'] = None) -> 'ListObject':
        """Separates the string based on the separator."""
        return ListObject(
            elements=list(
                map(
                    lambda x: StringObject(value=x),
                    (
                        filter(lambda x: x, self.value.split(separator.value))
                        if separator is not None
                        else self.value
                    ),
                )
            )
        )

    def removeprefix(self, prefix: 'StringObject') -> 'StringObject':
        """Removes a prefix from the string if it exists."""
        return StringObject(value=self.value.removeprefix(prefix.value))

    def removesuffix(self, suffix: 'StringObject') -> 'StringObject':
        """Removes a suffix from the string if it exists."""
        return StringObject(value=self.value.removesuffix(suffix.value))

    def count_q(self, subset: 'StringObject') -> IntegerObject:
        """Returns the number of matches by subset."""
        return IntegerObject(value=self.value.count(subset.value))

    def nearest_q(self, subset: 'StringObject') -> IntegerObject:
        """Returns the index of the first matched item."""
        return IntegerObject(
            value=(
                result + 1
                if (result := self.value.find(subset.value)) != -1
                else -1
            )
        )

    def contains_q(self, subset: 'StringObject') -> BooleanObject:
        """Returns whether the given subset exists in the string."""
        return BooleanObject(value=subset.value in self.value)

    def startswith_q(self, prefix: 'StringObject') -> BooleanObject:
        """Returns true if the beginning of the string is the same as the input value."""
        return BooleanObject(value=self.value.startswith(prefix.value))

    def endswith_q(self, suffix: 'StringObject') -> BooleanObject:
        """Returns true if the end of the string is the same as the input value."""
        return BooleanObject(value=self.value.endswith(suffix.value))


@dataclass
class RangeObject(ExpressionObject):
    from_: Optional[IntegerObject] = field(kw_only=True)
    to: Optional[IntegerObject] = field(default=None, kw_only=True)
    by: Optional[IntegerObject] = field(default=None, kw_only=True)

    def __str__(self) -> str:
        """Returns the object as a string."""
        return (
            f'[{self.from_}, {self.by if self.by is not None else 1}'
            f'..{self.to if self.to is not None else "undefined"}]'
        )

    def __hash__(self) -> int:
        """Calculates the hash of the object."""
        return hash((self.from_, self.to, self.by))

    def __iter__(self) -> 'RangeObject':
        """Iterates over the range defined by the object."""
        self._number = self.from_
        return self

    def __next__(self) -> int:
        """Returns the next integer in the range."""
        if self.to is not None and self._number > self.to:  # type: ignore[operator]
            raise StopIteration
        result = self._number
        self._number += (  # type: ignore[operator, assignment]
            self.by if self.by is not None else IntegerObject(value=1)
        )
        return result  # type: ignore[return-value]


class DataStructureObject(ExpressionObject):
    pass


@dataclass
class ListObject(DataStructureObject):
    elements: List[Optional[FarrObject]] = field(kw_only=True)

    def __str__(self) -> str:
        """Returns elements separated by a semicolon."""
        return '; '.join(map(str, self.elements))

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

    def __getitem__(
        self,
        key: 'RangeObject',
    ) -> FarrObject:
        """Extracts a range of elements."""
        if key.from_.value <= 0 or key.by is not None and key.by.value <= 0:  # type: ignore[union-attr]
            raise IndexError('Non-positive indexes are not allowed!{Colors.reset}')
        return (
            self.elements[key.from_.value - 1]  # type: ignore[return-value, union-attr]
            if key.to is None and key.by is None
            else ListObject(
                elements=self.elements[
                    key.from_.value  # type: ignore[union-attr]
                    - 1 : key.to.value if key.to is not None else None : (
                        key.by.value if key.by is not None else None
                    )
                ]
            )
        )

    def __setitem__(
        self,
        key: 'RangeObject',
        value: FarrObject,
    ) -> None:
        """Updates the elements based on the given range."""
        if key.from_.value <= 0 or key.by is not None and key.by.value <= 0:  # type: ignore[union-attr]
            raise IndexError('Non-positive indexes are not allowed!{Colors.reset}')
        elif key.to is None and key.by is None:
            self.elements[key.from_.value - 1] = value  # type: ignore[union-attr]
            return None
        self.elements[  # type: ignore[call-overload]
            key.from_.value  # type: ignore[union-attr]
            - 1 : key.to.value if key.to is not None else None : (
                key.by.value if key.by is not None else None
            )
        ] = value

    def __iter__(self) -> 'ListObject':
        """Iterates the elements in the list."""
        self._index = 0
        return self

    def __next__(self) -> FarrObject:
        """Returns the next element of the list."""
        if self._index >= len(self.elements):
            raise StopIteration
        element = self.elements[self._index]
        self._index += 1
        return element  # type: ignore[return-value]

    @property
    def first(self) -> FarrObject:
        """Returns the first element if the list is not empty."""
        if not self.elements:
            raise IndexError('The list is empty!{Colors.reset}')
        return self.elements[0]  # type: ignore[return-value]

    @property
    def last(self) -> FarrObject:
        """Returns the last element if the list is not empty."""
        if not self.elements:
            raise IndexError('The list is empty!{Colors.reset}')
        return self.elements[-1]  # type: ignore[return-value]

    @property
    def length(self) -> IntegerObject:
        """Returns the number of elements in the list."""
        return IntegerObject(value=len(self.elements))

    def isempty_q(self) -> BooleanObject:
        """Returns the status of the list being empty or not."""
        return BooleanObject(value=not bool(self.elements))

    def clear_e(self) -> NullObject:
        """Removes all elements from the list."""
        self.elements = []
        return NullObject()

    def nearest_q(self, element: FarrObject) -> IntegerObject:
        """Returns the index of the closest element found in the list."""
        return IntegerObject(
            value=(
                self.elements.index(element) + 1
                if element in self.elements
                else -1
            )
        )

    def iprepend_e(self, element: FarrObject) -> NullObject:
        """Adds an element to the beginning of the list."""
        self.elements.insert(0, element)
        return NullObject()

    def append_e(self, element: FarrObject) -> NullObject:
        """Adds an element to the end of the list"""
        self.elements.append(element)
        return NullObject()

    def pop_e(self, index: IntegerObject) -> FarrObject:
        """Deletes an element based on the index."""
        if index.value <= 0:
            raise IndexError(
                'Using an index smaller than or equal to zero is not allowed!{Colors.reset}'
            )
        return self.elements.pop(index.value - 1)  # type: ignore[return-value]

    def popitem_e(self, value: FarrObject) -> FarrObject:
        """Discards an element based on the given value."""
        return self.elements.pop(self.elements.index(value))  # type: ignore[return-value]

    def reverse(self) -> 'ListObject':
        """Returns the reversed list."""
        return ListObject(elements=list(reversed(self.elements)))  # type: ignore[type-var]

    def ireverse_e(self) -> 'ListObject':
        """Reverses the list and returns the new state."""
        self.elements = list(reversed(self.elements))  # type: ignore[type-var]
        return self

    def sort(self) -> 'ListObject':
        """Returns the sorted list."""
        return ListObject(elements=sorted(self.elements))  # type: ignore[type-var]

    def isort_e(self) -> 'ListObject':
        """Sorts the list in its own place."""
        self.elements = sorted(self.elements)  # type: ignore[type-var]
        return self

    def shuffle(self) -> 'ListObject':
        """Returns a shuffled list."""
        return ListObject(
            elements=sorted(self.elements, key=lambda _: random.random())
        )

    def ishuffle_e(self) -> 'ListObject':
        """Assigns the shuffled list to the object and then returns it."""
        self.elements = sorted(self.elements, key=lambda _: random.random())
        return self

    def join(self, separator: Optional[StringObject] = None) -> StringObject:
        """Merges elements together."""
        return StringObject(
            value=(separator.value if separator is not None else '').join(
                map(str, self.elements)
            )
        )


@dataclass
class HashMapObject(DataStructureObject):
    pairs: Optional[List['PairObject']] = field(kw_only=True)

    def __post_init__(self) -> None:
        """Tries to ignore duplicate pairs."""
        self._drop_duplicates()

    def __str__(self) -> str:
        """Returns existing pairs separated by a semicolon."""
        return '; '.join(map(str, self.pairs))  # type: ignore[arg-type]

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

    def __getitem__(
        self,
        key: 'RangeObject',
    ) -> FarrObject:
        """Extracts a range of pairs."""
        if key.from_.value <= 0 or key.by is not None and key.by.value <= 0:  # type: ignore[union-attr]
            raise IndexError('Non-positive indexes are not allowed!{Colors.reset}')
        return (
            self.pairs[key.from_.value - 1]  # type: ignore[index, union-attr]
            if key.to is None and key.by is None
            else HashMapObject(
                pairs=self.pairs[  # type: ignore[index]
                    key.from_.value  # type: ignore[union-attr]
                    - 1 : key.to.value if key.to is not None else None : (
                        key.by.value if key.by is not None else None
                    )
                ]
            )
        )

    def __iter__(self) -> 'HashMapObject':
        """iterates over the pairs in the hash map."""
        self._index = 0
        return self

    def __next__(self) -> Tuple[FarrObject, FarrObject]:
        """Returns the next pair."""
        if self.pairs is not None and self._index >= len(self.pairs):
            raise StopIteration
        pair = self.pairs[self._index]  # type: ignore[index]
        self._index += 1
        return pair.key, pair.value

    def _drop_duplicates(self) -> None:
        """Removes duplicate pairs."""
        self.pairs = list({pair.key: pair for pair in self.pairs}.values())  # type: ignore[union-attr]

    @property
    def first(self) -> 'PairObject':
        """Returns the first existing pair."""
        if not self.pairs:
            raise IndexError('No pair found!{Colors.reset}')
        return self.pairs[0]

    @property
    def last(self) -> 'PairObject':
        """Returns the last existing pair."""
        if not self.pairs:
            raise IndexError('No pair found!{Colors.reset}')
        return self.pairs[-1]

    @property
    def length(self) -> IntegerObject:
        """Returns the number of existing pairs."""
        return IntegerObject(value=len(self.pairs))  # type: ignore[arg-type]

    @property
    def keys(self) -> ListObject:
        """Returns all available keys."""
        return ListObject(elements=list(map(lambda x: x.key, self.pairs)))  # type: ignore[arg-type]

    @property
    def values(self) -> ListObject:
        """Returns all values."""
        return ListObject(elements=list(map(lambda x: x.value, self.pairs)))  # type: ignore[arg-type]

    def isempty_q(self) -> BooleanObject:
        """Returns whether there is a pair or not."""
        return BooleanObject(value=not bool(self.pairs))

    def clear_e(self) -> NullObject:
        """Makes the object empty of pairs."""
        self.pairs = []
        return NullObject()

    def get(
        self,
        key: FarrObject,
        orelse: Optional[FarrObject] = None,
    ) -> FarrObject:
        """Returns a value based on the key or something else."""
        return {pair.key: pair.value for pair in self.pairs}.get(  # type: ignore[union-attr]
            key, orelse if orelse is not None else NullObject()
        )

    def iupdate_e(self, hash_map: 'HashMapObject') -> 'HashMapObject':
        """Updates the current pairs based on the new values."""
        self.pairs.extend(hash_map.pairs)  # type: ignore[union-attr, arg-type]
        self._drop_duplicates()
        return self

    def pop_e(self, index: IntegerObject) -> 'PairObject':
        """Discards a pair based on its index."""
        if index.value <= 0:
            raise IndexError('Non-positive indexes are not allowed!{Colors.reset}')
        return self.pairs.pop(index.value - 1)  # type: ignore[union-attr]

    def popitem_e(self, key: FarrObject) -> 'PairObject':
        """Deletes a pair based on the key."""
        return self.pairs.pop(self.pairs.index(key))  # type: ignore[union-attr, arg-type]


@dataclass
class PairObject(DataStructureObject):
    key: FarrObject = field(kw_only=True)
    value: FarrObject = field(kw_only=True)

    def __str__(self) -> str:
        """Returns the key and value along with an arrow."""
        return f'{self.key}->{self.value}'

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Compares the key with another object for equality."""
        return BooleanObject(value=self.key == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Compares the key with another object for inequality."""
        return BooleanObject(value=self.key != other)

    def __hash__(self) -> int:
        """Calculates the hash of the object."""
        return hash((self.key, self.value))


class PythonNativeObject(ExpressionObject):
    pass


@dataclass
class PythonNativeClassMethodObject(PythonNativeObject):
    method: types.MethodType = field(kw_only=True)

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks the sameness of two methods."""
        return BooleanObject(value=self.method.__func__.__qualname__ == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks to see the difference between the two methods."""
        return BooleanObject(value=self.method.__func__.__qualname__ != other)

    def __call__(
        self,
        *args: Tuple[FarrObject, ...],
        **kwargs: Dict[str, FarrObject],
    ) -> FarrObject:
        """Calls the method."""
        return self.method(*args, **kwargs)


class PythonNativePrintObject(PythonNativeObject):
    def __call__(
        self,
        *args: Tuple[FarrObject, ...],
    ) -> NullObject:
        """Prints and stays on the same line."""
        print(*args, end='')
        return NullObject()


class PythonNativePrintLineObject(PythonNativeObject):
    def __call__(
        self,
        *args: Tuple[FarrObject, ...],
    ) -> NullObject:
        """Prints and goes to the next line."""
        print(*args)
        return NullObject()

class SystemConsole(PythonNativeObject): 
    def writeline(
            self,
            *args: Tuple[FarrObject, ...],
             ) -> NullObject:
            """Prints and goes to the next line."""
            print(f"{Colors.bright_white}",*args,f"{Colors.reset}")
            return NullObject()

    def write(
        self,
        *args: Tuple[FarrObject, ...],
    ) -> NullObject:
        """Prints and stays on the same line."""
        print(f"{Colors.bright_white}",*args,f"{Colors.reset}", end='')
        return NullObject()

    

class SystemMath(PythonNativeObject):
    def __call__(self, arg:FarrObject):
            return type(arg)
    def random(self, *args: Tuple[FarrObject, IntegerObject]) -> 'ListObject':
        if len(args) != 2:
            print(f"{Colors.bright_red}   ValueError{Colors.red}","Two arguments are required")

        chars = str(args[0]).replace(";", "").split(",")
        chars = [char.strip() for char in chars]
        num_choices = int(args[1])
        items = [random.choice(chars) for _ in range(num_choices)]
        return ListObject(items)

    def ave(self, arg: FarrObject):
        w = list(arg)
        x = len(w)
        y = 0
        
        for _ in w:
            y = y + float(str(_))
            
        z = y / x
        return (z)
            

    def acos(self, arg: FarrObject) -> float:
        return math.acos(arg.to_float())

    def acosh(self, arg: FarrObject) -> float:
        return math.acosh(arg.to_float())

    def asin(self, arg: FarrObject) -> float:
        return math.asin(arg.to_float())

    def asinh(self, arg: FarrObject) -> float:
        return math.asinh(arg.to_float())

    def atan(self, arg: FarrObject) -> float:
        return math.atan(arg.to_float())

    def atan2(self, y: FarrObject, x: FarrObject) -> float:
        return math.atan2(y.to_float(), x.to_float())

    def atanh(self, arg: FarrObject) -> float:
        return math.atanh(arg.to_float())

    def ceil(self, arg: FarrObject) -> int:
        return math.ceil(arg.to_float())

    def comb(self, n: IntegerObject, k: IntegerObject) -> int:
        return math.comb(n.to_int(), k.to_int())

    def copysign(self, x: FarrObject, y: FarrObject) -> float:
        return math.copysign(x.to_float(), y.to_float())

    def cos(self, arg: FarrObject) -> float:
        return math.cos(arg.to_float())

    def cosh(self, arg: FarrObject) -> float:
        return math.cosh(arg.to_float())

    def degrees(self, arg: FarrObject) -> float:
        return math.degrees(arg.to_float())

    def dist(self, p: FarrObject, q: FarrObject) -> float:
        return math.dist(p.to_float(), q.to_float())

    def erf(self, arg: FarrObject) -> float:
        return math.erf(arg.to_float())

    def erfc(self, arg: FarrObject) -> float:
        return math.erfc(arg.to_float())

    def exp(self, arg: FarrObject) -> float:
        return math.exp(arg.to_float())

    def expm1(self, arg: FarrObject) -> float:
        return math.expm1(arg.to_float())

    def fabs(self, arg: FarrObject) -> float:
        return math.fabs(arg.to_float())

    def factorial(self, arg: IntegerObject) -> int:
        return math.factorial(arg.to_int())

    def floor(self, arg: FarrObject) -> int:
        return math.floor(arg.to_float())

    def fmod(self, x: FarrObject, y: FarrObject) -> float:
        return math.fmod(x.to_float(), y.to_float())

    def frexp(self, arg: FarrObject) -> Tuple[float, int]:
        return math.frexp(arg.to_float())

    def fsum(self, iterable: ListObject) -> float:
        return math.fsum([float(item) for item in iterable.items])

    def gamma(self, arg: FarrObject) -> float:
        return math.gamma(arg.to_float())

    def gcd(self, a: IntegerObject, b: IntegerObject) -> int:
        return math.gcd(a.to_int(), b.to_int())

    def hypot(self, *args: FarrObject) -> float:
        return math.hypot(*(arg.to_float() for arg in args))

    def isclose(self, a: FarrObject, b: FarrObject, rel_tol: float = 1e-09, abs_tol: float = 0.0) -> bool:
        return math.isclose(a.to_float(), b.to_float(), rel_tol=rel_tol, abs_tol=abs_tol)

    def isfinite(self, arg: FarrObject) -> bool:
        return math.isfinite(arg.to_float())

    def isinf(self, arg: FarrObject) -> bool:
        return math.isinf(arg.to_float())

    def isnan(self, arg: FarrObject) -> bool:
        return math.isnan(arg.to_float())

    def isqrt(self, arg: IntegerObject) -> int:
        return math.isqrt(arg.to_int())

    def ldexp(self, x: FarrObject, i: IntegerObject) -> float:
        return math.ldexp(x.to_float(), i.to_int())

    def lgamma(self, arg: FarrObject) -> float:
        return math.lgamma(arg.to_float())

    def log(self, arg: FarrObject, base: FarrObject = None) -> float:
        if base is not None:
            return math.log(arg.to_float(), base.to_float())
        else:
            return math.log(arg.to_float())

    def log10(self, arg: FarrObject) -> float:
        return math.log10(arg.to_float())

    def log1p(self, arg: FarrObject) -> float:
        return math.log1p(arg.to_float())

    def log2(self, arg: FarrObject) -> float:
        return math.log2(arg.to_float())

    def perm(self, n: IntegerObject, k: IntegerObject = None) -> int:
        return math.perm(n.to_int(), k.to_int() if k else None)

    def pow(self, x: FarrObject, y: FarrObject) -> float:
        return math.pow(x.to_float(), y.to_float())

    def prod(self, iterable: ListObject) -> float:
        return math.prod([float(item) for item in iterable.items])

    def radians(self, arg: FarrObject) -> float:
        return math.radians(arg.to_float())

    def remainder(self, x: FarrObject, y: FarrObject) -> float:
        return math.remainder(x.to_float(), y.to_float())

    def sin(self, arg: FarrObject) -> float:
        return math.sin(arg.to_float())

    def sinh(self, arg: FarrObject) -> float:
        return math.sinh(arg.to_float())

    def sqrt(self, arg: FarrObject) -> float:
        return math.sqrt(arg.to_float())

    def tan(self, arg: FarrObject) -> float:
        return math.tan(arg.to_float())

    def tanh(self, arg: FarrObject) -> float:
        return math.tanh(arg.to_float())

    def trunc(self, arg: FarrObject) -> int:
        return math.trunc(arg.to_float())

class SystemChars(PythonNativeObject): 
    def __call__(self, arg:FarrObject):
            return type(arg)
    def allchars(self,):
        allchars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','U','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0','!','@','#','$','%','^','&','*','?','/','\\','|','<','>',',','.','~','`','(',')','-','=','_','+',':',';','"','"']
        
        #print(allchars)
        return allchars
    def digits(self,):
        allchars = ['1','2','3','4','5','6','7','8','9','0']
        
        #print(allchars)
        return allchars
    def a_to_z_lower(self,):
        allchars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        
        #print(allchars)
        return allchars
    def a_to_z_upper(self,):
        allchars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','U','R','S','T','U','V','W','X','Y','Z']
        
        #print(allchars)
        return allchars
    def esymbols(self,):
        allchars = ['!','@','#','$','%','^','&','*','?','/','\\','|','<','>',',','.','~','`','(',')','-','=','_','+',':',';','"','"']
        
        #print(allchars)
        return allchars
    
class SystemRaise(PythonNativeObject): 
    def __call__(self, arg:FarrObject):
            return type(arg)
    def success(
            self,
            *args: Tuple[FarrObject, ...],
             ) -> NullObject:
            """Prints and goes to the next line."""
            print(f"{Colors.bright_green}",*args,f"{Colors.reset}")
            return NullObject()

    def successln(
            self,
            *args: Tuple[FarrObject, ...],
        ) -> NullObject:
            """Prints and stays on the same line."""
            print(f"\n{Colors.bright_green}",*args,f"{Colors.reset}", end='')
            return NullObject()

    def error(
            self,
            *args: Tuple[FarrObject, ...],
             ) -> NullObject:
            """Prints and goes to the next line."""
            print(f"{Colors.bright_red}",*args,f"{Colors.reset}")
            return NullObject()

    def errorln(
            self,
            *args: Tuple[FarrObject, ...],
        ) -> NullObject:
            """Prints and stays on the same line."""
            print(f"\n{Colors.bright_red}",*args,f"{Colors.reset}", end='')
            return NullObject()

    def warning(
            self,
            *args: Tuple[FarrObject, ...],
             ) -> NullObject:
            """Prints and goes to the next line."""
            print(f"{Colors.yellow}",*args,f"{Colors.reset}")
            return NullObject()

    def warningln(
            self,
            *args: Tuple[FarrObject, ...],
        ) -> NullObject:
            """Prints and stays on the same line."""
            print(f"\n{Colors.yellow}",*args,f"{Colors.reset}", end='')
            return NullObject()

    def output(
            self,
            *args: Tuple[FarrObject, ...],
             ) -> NullObject:
            """Prints and goes to the next line."""
            print(f"{Colors.bright_magenta}",*args,f"{Colors.reset}")
            return NullObject()

    def outputln(
            self,
            *args: Tuple[FarrObject, ...],
        ) -> NullObject:
            """Prints and stays on the same line."""
            print(f"\n{Colors.bright_magenta}",*args,f"{Colors.reset}", end='')
            return NullObject()

    def info(
            self,
            *args: Tuple[FarrObject, ...],
             ) -> NullObject:
            """Prints and goes to the next line."""
            print(f"{Colors.bright_blue}",*args,f"{Colors.reset}")
            return NullObject()

    def infoln(
            self,
            *args: Tuple[FarrObject, ...],
        ) -> NullObject:
            """Prints and stays on the same line."""
            print(f"\n{Colors.bright_blue}",*args,f"{Colors.reset}", end='')
            return NullObject()



class PythonNativeReadLineObject(PythonNativeObject):
    def __call__(self, prompt: Optional[StringObject] = None) -> StringObject:
        """Takes an input from the user."""
        return StringObject(value=input(prompt if prompt is not None else ''))


class PythonNativePanicObject(PythonNativeObject):
    def __call__(
        self,
        exception: Optional[BaseException] = None,
    ) -> None:
        """Throws an error."""
        raise exception if exception is not None else BaseException  # type: ignore[misc]


class PythonNativeAssertObject(PythonNativeObject):
    def __call__(
        self,
        condition: FarrObject,
        message: Optional[StringObject] = None,
    ) -> None:
        """Panics if the condition is not correct."""
        assert condition, message if message is not None else ''


class PythonNativeExitObject(PythonNativeObject):
    def __call__(self, code: Optional[IntegerObject] = None) -> None:
        """Comes out based on the given exit code."""
        sys.exit(code)  # type: ignore[arg-type]


class PythonNativeTypeOfObject(PythonNativeObject):
    def __call__(self, object_: FarrObject) -> StringObject:
        """Returns the object type."""
        return StringObject(value=object_.__class__.__name__)


class PythonNativeSimilarTypesObject(PythonNativeObject):
    def __call__(
        self,
        object_: FarrObject,
        target: FarrObject,
    ) -> BooleanObject:
        """Checks whether there are similar types or not."""
        return BooleanObject(value=object_.__class__ == target.__class__)


class PythonNativeShellExecutionObject(PythonNativeObject):
    def __call__(self, cmd: StringObject) -> StringObject:
        """Executes the command in the shell and returns the result."""
        return StringObject(value=subprocess.getoutput(cmd.value))


class PythonNativeBaseErrorObject(BaseException, PythonNativeObject):
    pass


class PythonNativeKeyboardInterruptErrorObject(
    KeyboardInterrupt,
    PythonNativeObject,
):
    pass


class PythonNativeSystemExitErrorObject(SystemExit, PythonNativeObject):
    pass


class PythonNativeArithmeticErrorObject(ArithmeticError, PythonNativeObject):
    pass


class PythonNativeAssertionErrorObject(AssertionError, PythonNativeObject):
    pass


class PythonNativeAttributeErrorObject(AttributeError, PythonNativeObject):
    pass


class PythonNativeImportErrorObject(ImportError, PythonNativeObject):
    pass


class PythonNativeLookupErrorObject(LookupError, PythonNativeObject):
    pass


class PythonNativeNameErrorObject(NameError, PythonNativeObject):
    pass


class PythonNativeOSErrorObject(OSError, PythonNativeObject):
    pass


class PythonNativeRuntimeErrorObject(RuntimeError, PythonNativeObject):
    pass


class PythonNativeNotImplementedErrorObject(
    NotImplementedError,
    PythonNativeObject,
):
    pass


class PythonNativeTypeErrorObject(TypeError, PythonNativeObject):
    pass


class PythonNativeValueErrorObject(ValueError, PythonNativeObject):
    pass


class PythonNativeDeprecatedErrorObject(DeprecationWarning, PythonNativeObject):
    pass


@dataclass
class StructInstanceObject(ExpressionObject):
    environment: Environment = field(repr=False, kw_only=True)

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are similar."""
        return BooleanObject(value=self.__dict__ == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are different or not."""
        return BooleanObject(value=self.__dict__ != other)

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

    def __getattr__(self, name: str) -> FarrObject:
        """Finds the value from the environment."""
        return self.environment.locate(name)
    
@dataclass
class ExtensionInstanceObject(ExpressionObject):
    environment: Environment = field(repr=False, kw_only=True)

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are similar."""
        return BooleanObject(value=self.__dict__ == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are different or not."""
        return BooleanObject(value=self.__dict__ != other)

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

    def __getattr__(self, name: str) -> FarrObject:
        """Finds the value from the environment."""
        return self.environment.locate(name)


class StatementObject(FarrObject):
    pass


@dataclass
class ImportSystemObject(StatementObject):
    environment: Environment = field(repr=False, kw_only=True)

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

    def __getattr__(self, name: str) -> FarrObject:
        """Makes the modules available."""
        return self.environment.locate(name)


class ModuleObject(ImportSystemObject):
    pass


class LibraryObject(ImportSystemObject):
    pass


@dataclass
class NonPythonNativeObject(StatementObject):
    environment: Optional[Environment] = field(
        default=None, repr=False, kw_only=True
    )
    body: BlockNode = field(repr=False, kw_only=True)


@dataclass
class FunctionDefinitionObject(NonPythonNativeObject):
    params: ItemizedExpressionNode = field(repr=False, kw_only=True)

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are similar."""
        return BooleanObject(value=self.__dict__ == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are different or not."""
        return BooleanObject(value=self.__dict__ != other)

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

@dataclass
class VoidFunctionDefinitionObject(NonPythonNativeObject):
    params: ItemizedExpressionNode = field(repr=False, kw_only=True)

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are similar."""
        return BooleanObject(value=self.__dict__ == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are different or not."""
        return BooleanObject(value=self.__dict__ != other)

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)
    
    def loop(self,numtimes:FarrObject) -> int:
        for __ in int(numtimes):
            self.__call__()



@dataclass
class StructDefinitionObject(NonPythonNativeObject):
    attributes: ItemizedExpressionNode = field(repr=False, kw_only=True)

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are similar."""
        return BooleanObject(value=self.__dict__ == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are different or not."""
        return BooleanObject(value=self.__dict__ != other)

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

@dataclass
class ExtensionDefinitionObject(NonPythonNativeObject):
    attributes: ItemizedExpressionNode = field(repr=False, kw_only=True)

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are similar."""
        return BooleanObject(value=self.__dict__ == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are different or not."""
        return BooleanObject(value=self.__dict__ != other)

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

    # def __sametype__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
    #     """Checks whether the attributes are similar."""
    #     return BooleanObject(value=type(self.__dict__ ) == type(other))

    # def __notsametype__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
    #     """Checks whether the attributes are similar."""
    #     return BooleanObject(value=type(self.__dict__ ) != type(other))

    # def __sametypeandsamevalue__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
    #     """Checks whether the attributes are similar."""
    #     return BooleanObject(value=type(self.__dict__ ) == type(other))

    # def __notsametypeandsamevalue__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
    #     """Checks whether the attributes are similar."""
    #     return BooleanObject(value=type(self.__dict__ ) != type(other))



#####################
### BASIC SCIENCE ###
#####################

class SystemBasicScience(PythonNativeObject):
    def __call__(self, arg:FarrObject):
            return type(arg)
     # Mechanics
    def velocity(self, displacement: float, time: float) -> float:
        return displacement / time

    def acceleration(self, initial_velocity: float, final_velocity: float, time: float) -> float:
        return (final_velocity - initial_velocity) / time

    def force(self, mass: float, acceleration: float) -> float:
        return mass * acceleration

    def momentum(self, mass: float, velocity: float) -> float:
        return mass * velocity

    def kinetic_energy(self, mass: float, velocity: float) -> float:
        return 0.5 * mass * velocity**2

    def gravitational_potential_energy(self, mass: float, height: float, g: float = 9.81) -> float:
        return mass * g * height

    # Circular Motion
    def angular_velocity(self, angle: float, time: float) -> float:
        return angle / time

    def centripetal_acceleration(self, velocity: float, radius: float) -> float:
        return velocity**2 / radius

    # Thermodynamics
    def heat(self, mass: float, specific_heat_capacity: float, temperature_change: float) -> float:
        return mass * specific_heat_capacity * temperature_change

    def work(self, force: float, displacement: float, angle: float = 0) -> float:
        return force * displacement * math.cos(math.radians(angle))

    def power(self, work_done: float, time: float) -> float:
        return work_done / time

    def efficiency(self, useful_work: float, total_work: float) -> float:
        return (useful_work / total_work) * 100

    # Optics
    def focal_length(self, object_distance: float, image_distance: float) -> float:
        return (1 / object_distance) + (1 / image_distance)

    def magnification(self, image_height: float, object_height: float) -> float:
        return image_height / object_height

    def lens_formula(self, focal_length: float, object_distance: float, image_distance: float) -> float:
        return (1 / focal_length) - (1 / object_distance) + (1 / image_distance)

    def index_of_refraction(self, speed_of_light_vacuum: float, speed_of_light_medium: float) -> float:
        return speed_of_light_vacuum / speed_of_light_medium

    # Electricity
    def voltage(self, current: float, resistance: float) -> float:
        return current * resistance

    def current(self, voltage: float, resistance: float) -> float:
        return voltage / resistance

    def resistance(self, voltage: float, current: float) -> float:
        return voltage / current

    def power_dissipated(self, current: float, resistance: float) -> float:
        return current**2 * resistance

    def electrical_energy(self, voltage: float, time: float) -> float:
        return voltage * time

    # Waves
    def wave_speed(self, frequency: float, wavelength: float) -> float:
        return frequency * wavelength

    def frequency(self, wave_speed: float, wavelength: float) -> float:
        return wave_speed / wavelength

    def wavelength(self, wave_speed: float, frequency: float) -> float:
        return wave_speed / frequency

    # Modern Physics
    def energy_photon(self, frequency: float) -> float:
        return 6.62607015e-34 * frequency  # Planck's constant * frequency

    def de_broglie_wavelength(self, momentum: float, mass: float) -> float:
        return 6.62607015e-34 / momentum  # Planck's constant / momentum

import json

class JSONInterpreter(PythonNativeObject):
    def __call__(self, arg:FarrObject):
            return type(arg)
    def loads(self, json_string: FarrObject) -> string:
        """
        Loads JSON data from a string.

        Args:
            json_string (str): JSON string to be loaded.

        Returns:
            Parsed JSON data.
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"{Colors.bright_red}   ValueError{Colors.red}","Invalid JSON format")

    def dumps(self, data: FarrObject) -> string:
        """
        Dumps data to a JSON string.

        Args:
            data: Data to be converted to JSON.

        Returns:
            JSON string.
        """
        return json.dumps(data)

    def pretty_dumps(self, data: FarrObject) -> string:
        """
        Dumps data to a formatted (pretty-printed) JSON string.

        Args:
            data: Data to be converted to JSON.

        Returns:
            Formatted JSON string.
        """
        return json.dumps(data, indent=4)

    def validate(self, json_string: FarrObject) -> string:
        """
        Validates if a string is a valid JSON.

        Args:
            json_string (str): JSON string to be validated.

        Returns:
            True if the string is valid JSON, False otherwise.
        """
        try:
            json.loads(json_string)
            return True
        except ValueError:
            return False

    def get(self, data, key):
        """
        Gets the value associated with the given key in a JSON object.

        Args:
            data: JSON data.
            key: Key to search for.

        Returns:
            The value associated with the key, or None if the key is not found.
        """
        if isinstance(data, dict):
            return data.get(key)
        return None

    def set(self, data, key, value):
        """
        Sets the value associated with the given key in a JSON object.

        Args:
            data: JSON data.
            key: Key to set.
            value: Value to associate with the key.
        """
        if isinstance(data, dict):
            data[key] = value

    def rmkey(self, data, key):
        """
        Removes the given key from a JSON object.

        Args:
            data: JSON data.
            key: Key to remove.
        """
        if isinstance(data, dict) and key in data:
            del data[key]

    def merge(self, json1, json2):
        """
        Merges two JSON objects.

        Args:
            json1: First JSON object.
            json2: Second JSON object.

        Returns:
            Merged JSON object.
        """
        if isinstance(json1, dict) and isinstance(json2, dict):
            return {**json1, **json2}
        return None

    def filter(self, data, keys_to_keep):
        """
        Filters a JSON object to keep only specified keys.

        Args:
            data: JSON data.
            keys_to_keep: List of keys to keep.

        Returns:
            Filtered JSON object.
        """
        if isinstance(data, dict):
            return {key: data[key] for key in keys_to_keep if key in data}
        return None

    def sort(self, data, key=None, reverse=False):
        """
        Sorts a JSON object by keys or values.

        Args:
            data: JSON data.
            key: Key function to sort by (optional).
            reverse: Whether to sort in reverse order (optional).

        Returns:
            Sorted JSON object.
        """
        if isinstance(data, dict):
            return dict(sorted(data.items(), key=key, reverse=reverse))
        return None

    def flatten(self, data, parent_key='', sep='_'):
        """
        Flattens a nested JSON object into a single level.

        Args:
            data: JSON data.
            parent_key: Parent key (optional).
            sep: Separator for nested keys (optional).

        Returns:
            Flattened JSON object.
        """
        flattened = {}
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f'{parent_key}{sep}{k}' if parent_key else k
                if isinstance(v, dict):
                    flattened.update(self.flatten_json(v, new_key, sep=sep))
                else:
                    flattened[new_key] = v
        return flattened

    def unflatten(self, data):
        """
        Unflattens a flattened JSON object into a nested structure.

        Args:
            data: Flattened JSON data.

        Returns:
            Unflattened JSON object.
        """
        unflattened = {}
        for key, value in data.items():
            parts = key.split('_')
            current = unflattened
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = value
        return unflattened
    
class FSONInterpreter(PythonNativeObject):
    def __call__(self, arg:FarrObject):
            return type(arg)
    
    def loadsde(self, sson_string:FarrObject) -> string:
        sson_data = {}
        for line in str(sson_string).split('\n'):
            if not line or line.startswith('#'):
                continue
            
            datas = line.split(';')
            
            for dat in datas:
                parts = dat.split(":")
                if len(parts) == 2:
                    key = parts[0]
                    valueof = parts[1]
                    sson_data[str(key)] = str(valueof)
                # else:
                #     print(f"Ignoring invalid line: {line}")
        return sson_data

    def loads(self, sson_string:FarrObject) -> string:
        sson_data = {}
        for line in str(sson_string).split('\n'):
            if not line or line.startswith('#'):
                continue
            
            datas = line.split(';')
            
            for dat in datas:  
                if not dat or dat.startswith('#'):
                    continue
            
                if len(dat.split(":")) == 2:
                    parts = dat.split(":")
                    if "[" in dat:
                        pass
                    else:
                        key = parts[0]
                        valueof = parts[1]
                        sson_data[str(key)] = str(valueof)
                else:
                    parts = dat.split(":")
                    if "[" in parts[1]:
                        if "[" in parts[1]:
                            heading = str(parts[0])
                            str_parts = str(parts)
                            valueof =str_parts.split(",")

                        F = str(valueof).replace("{","").replace("}","").replace("[","").replace("]","").replace("'","")

                        #print(f"F: {F}")
                    
                        x = 0

                        #print(f"{key} : {resdata} ")

                        valueof[0] = ""

                        dattoresend = ""                      

                        for _ in valueof:
                            if _ == "":
                                pass
                            else:
                                x += 0.5
                                resval = _.replace("{","").replace("}","").replace("[","").replace("]","").replace("'","").replace("#.#",f" @@num")
                                #print(f"*** >>>",resval)
                                dattoresend += resval
                            #print(x)

                        realdat = dattoresend.split(" ")
                    
                        abc = 0
                        charlovck = False

                        jmbldat = ""

                        for __ in realdat:
                            if charlovck:
                                resval2 = __.replace("@@num",f" {str(int(abc))}:")
                            else:
                                resval2 = __.replace("@@num",f",{str(int(abc))}:")
                            #print(resval2)
                            abc += 0.5
                            jmbldat += resval2
                            charlovck = True
                        
                    
                        anadat = jmbldat.split(" ")
                    
                        pakadat = ""
                    
                        for ___ in anadat:
                            if ___ == "":
                                pass
                            else:
                                fusdat = f"{___};"
                                pakadat += fusdat
                                #print(fusdat)

                        #print(pakadat)
                        valdat = self.loads(pakadat)
                        #print(heading)
                        sson_data[str(heading)] = valdat

                    
                    
                # else:
                #     print(f"Ignoring invalid line: {line}")
        return sson_data

    def dumps(self, data):
        """
        Dumps data to SSON format.

        Args:
            self
            data: Data to be converted to SSON.

        Returns:
            SSON string.
        """
        return '\n'.join([f"{key}: {value}" for key, value in data.items()])

    def validate(self, sson_string):
        """
        Validates if a string is a valid SSON.

        Args:
            self
            sson_string (str): SSON string to be validated.

        Returns:
            True if the string is valid SSON, False otherwise.
        """
        try:
            self.load(sson_string)
            return True
        except Exception:
            return False

    def get(self, data, key, default=None):
        """
        Gets the value associated with the given key in SSON data.

        Args:
            self
            data: SSON data.
            key: Key to search for.
            default: Default value to return if key is not found (optional).

        Returns:
            The value associated with the key, or default if the key is not found.
        """
        return data.get(key, default)

    def set(self, data, key, value):
        """
        Sets the value associated with the given key in SSON data.
        Args:
            self
            data: SSON data.
            key: Key to set.
            value: Value to associate with the key.
        """
        data[key] = value

    def rmkey(self, data, key):
        """
        Removes the given key from SSON data.

        Args:
            self
            data: SSON data.
            key: Key to remove.
        """
        data.pop(key, None)

    def merge(self, sson1, sson2):
        """
        Merges two SSON objects.

        Args:
            self
            sson1: First SSON object.
            sson2: Second SSON object.

        Returns:
            Merged SSON object.
        """
        return {**sson1, **sson2}

    def filterf(self, data, keys_to_keep):
        """
        Filters SSON data to keep only specified keys.

        Args:
            self
            data: SSON data.
            keys_to_keep: List of keys to keep.

        Returns:
            Filtered SSON data.
        """
        return {key: data[key] for key in keys_to_keep if key in data}

    def sort(self, data, key=None, reverse=False):
        """
        Sorts SSON data by keys or values.

        Args:
            self
            data: SSON data.
            key: Key function to sort by (optional).
            reverse: Whether to sort in reverse order (optional).

        Returns:
            Sorted SSON data.
        """
        return dict(sorted(data.items(), key=key, reverse=reverse))

    def flatten(self, data):
        """
        Flattens a nested SSON object into a single level.

        Args:
            self
            data: SSON data.

        Returns:
            Flattened SSON data.
        """
        flattened = {}
        for key, value in data.items():
            if isinstance(value, dict):
                sub_data = self.flatten(value)
                for sub_key, sub_value in sub_data.items():
                    flattened[f"{key}_{sub_key}"] = sub_value
            else:
                flattened[key] = value
        return flattened

    def unflatten(self, data):
        """
        Unflattens a flattened SSON object into a nested structure.

        Args:
            self
            data: Flattened SSON data.

        Returns:
            Unflattened SSON data.
        """
        unflattened = {}
        for key, value in data.items():
            parts = key.split('_')
            current = unflattened
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = value
        return unflattened ### NEEDS FIX ###




class TimeObjLib(PythonNativeObject):
    def __call__(self, arg:FarrObject):
            return type(arg)
    def sleep(self, arg: FarrObject) -> int:
        time.sleep(arg.to_float())
        return 0
    
    def get_clock_info(self, arg: FarrObject) -> str:
        return time.get_clock_info(arg.to_float())
    
    def local_time(self) -> str:
        return str(time.localtime())
    
    def perf_counter(self) -> str:
        return str(time.perf_counter())
    
    def perf_counter_ns(self) -> str:
        return str(time.perf_counter_ns())
    
    def monotonic(self) -> str:
        return str(time.monotonic())
    
    def monotonic_ns(self) -> str:
        return str(time.monotonic_ns())
    
    def process_time(self) -> str:
        return str(time.process_time())
    
    def process_time_ns(self) -> str:
        return str(time.process_time_ns())
    
    def strf(self, format: FarrObject, t: Union[time.struct_time, None] = None) -> str:
        return time.strftime(format.to_float(), t if t else time.localtime())
    
    def strp(self, string: FarrObject, format: FarrObject) -> str:
        return str(time.strptime(string.to_float(), format.to_float()))
    
    def thread_time(self) -> str:
        return str(time.thread_time())
    
    def thread_time_ns(self) -> str:
        return str(time.thread_time_ns())
    
    def time(self) -> str:
        return str(time.time())
    
    def time_ns(self) -> str:
        return str(time.time_ns())
    
    def timezone(self) -> str:
        return str(time.timezone)
    
    def altzone(self) -> str:
        return str(time.altzone)
    
    def ctime(self, seconds: Union[float, None] = None) -> str:
        return time.ctime(seconds)
    
    def gmtime(self, seconds: Union[float, None] = None) -> str:
        return str(time.gmtime(seconds))
    
    def daylight(self) -> str:
        return str(time.daylight)
    
    def tzname(self) -> str:
        return str(time.tzname)

class DateTimeObjLib(PythonNativeObject):
    def __call__(self, arg:FarrObject):
            return type(arg)
    def now(self) -> str:
        return str(datetime.datetime.now())
    
    def utcnow(self) -> str:
        return str(datetime.datetime.utcnow())
    
    def today(self) -> str:
        return str(datetime.date.today())
    
    def date(self, year: FarrObject, month: FarrObject, day: FarrObject) -> str:
        return str(datetime.date(year.to_int(), month.to_int(), day.to_int()))
    
    def time(self, hour: FarrObject, minute: FarrObject, second: FarrObject, microsecond: FarrObject = FarrObject()) -> str:
        return str(datetime.time(hour.to_int(), minute.to_int(), second.to_int(), microsecond.to_int()))
    
    def datetime(self, year: FarrObject, month: FarrObject, day: FarrObject, hour: FarrObject = FarrObject(), minute: FarrObject = FarrObject(), second: FarrObject = FarrObject(), microsecond: FarrObject = FarrObject()) -> str:
        return str(datetime.datetime(year.to_int(), month.to_int(), day.to_int(), hour.to_int(), minute.to_int(), second.to_int(), microsecond.to_int()))
    
    def timedelta(self, days: FarrObject = FarrObject(), seconds: FarrObject = FarrObject(), microseconds: FarrObject = FarrObject(), milliseconds: FarrObject = FarrObject(), minutes: FarrObject = FarrObject(), hours: FarrObject = FarrObject(), weeks: FarrObject = FarrObject()) -> str:
        return str(datetime.timedelta(days=days.to_int(), seconds=seconds.to_int(), microseconds=microseconds.to_int(), milliseconds=milliseconds.to_int(), minutes=minutes.to_int(), hours=hours.to_int(), weeks=weeks.to_int()))
    
    def strftime(self, dt: FarrObject, format: FarrObject) -> str:
        return datetime.datetime.strptime(dt.to_str(), format.to_str()).strftime(format.to_str())
    
    def strptime(self, date_string: FarrObject, format: FarrObject) -> str:
        return str(datetime.datetime.strptime(date_string.to_str(), format.to_str()))
    
    def fromtimestamp(self, timestamp: FarrObject) -> str:
        return str(datetime.datetime.fromtimestamp(timestamp.to_int()))
    
    def utcfromtimestamp(self, timestamp: FarrObject) -> str:
        return str(datetime.datetime.utcfromtimestamp(timestamp.to_int()))
    
    def combine(self, date: FarrObject, time: FarrObject) -> str:
        date_obj = datetime.datetime.strptime(date.to_str(), "%Y-%m-%d").date()
        time_obj = datetime.datetime.strptime(time.to_str(), "%H:%M:%S").time()
        return str(datetime.datetime.combine(date_obj, time_obj))
    
    def isoformat(self, dt: FarrObject) -> str:
        return datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S").isoformat()
    
    def fromisoformat(self, date_string: FarrObject) -> str:
        return str(datetime.datetime.fromisoformat(date_string.to_str()))
    
    def timestamp(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S")
        return str(dt_obj.timestamp())
    
    def toordinal(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d")
        return str(dt_obj.toordinal())
    
    def weekday(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d")
        return str(dt_obj.weekday())
    
    def isoweekday(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d")
        return str(dt_obj.isoweekday())
    
    def isocalendar(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d")
        return str(dt_obj.isocalendar())
    
    def astimezone(self, dt: FarrObject, tz: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S")
        tz_obj = datetime.timezone(datetime.timedelta(hours=tz.to_int()))
        return str(dt_obj.astimezone(tz_obj))
    
    def replace(self, dt: FarrObject, year: Optional[FarrObject] = None, month: Optional[FarrObject] = None, day: Optional[FarrObject] = None, hour: Optional[FarrObject] = None, minute: Optional[FarrObject] = None, second: Optional[FarrObject] = None, microsecond: Optional[FarrObject] = None, tzinfo: Optional[FarrObject] = None) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S")
        kwargs = {}
        if year is not None:
            kwargs['year'] = year.to_int()
        if month is not None:
            kwargs['month'] = month.to_int()
        if day is not None:
            kwargs['day'] = day.to_int()
        if hour is not None:
            kwargs['hour'] = hour.to_int()
        if minute is not None:
            kwargs['minute'] = minute.to_int()
        if second is not None:
            kwargs['second'] = second.to_int()
        if microsecond is not None:
            kwargs['microsecond'] = microsecond.to_int()
        if tzinfo is not None:
            kwargs['tzinfo'] = datetime.timezone(datetime.timedelta(hours=tzinfo.to_int()))
        return str(dt_obj.replace(**kwargs))
    
    def total_seconds(self, td: FarrObject) -> str:
        td_obj = datetime.timedelta(seconds=td.to_int())
        return str(td_obj.total_seconds())
    
    def tzname(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S")
        return str(dt_obj.tzname())
    
    def utcoffset(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S")
        return str(dt_obj.utcoffset())
    
    def dst(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S")
        return str(dt_obj.dst())
    
    def max(self) -> str:
        return str(datetime.datetime.max)
    
    def min(self) -> str:
        return str(datetime.datetime.min)
    
    def resolution(self) -> str:
        return str(datetime.datetime.resolution)
    
    def combine_date_time(self, date: FarrObject, time: FarrObject) -> str:
        date_obj = datetime.date(date.to_int())
        time_obj = datetime.time(time.to_int())
        return str(datetime.datetime.combine(date_obj, time_obj))
    
    def timetz(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S")
        return str(dt_obj.timetz())
    
    def isoformat_date(self, date: FarrObject) -> str:
        date_obj = datetime.datetime.strptime(date.to_str(), "%Y-%m-%d").date()
        return date_obj.isoformat()
    
    def isoformat_time(self, time: FarrObject) -> str:
        time_obj = datetime.datetime.strptime(time.to_str(), "%H:%M:%S").time()
        return time_obj.isoformat()
    
    def date_isoformat(self, year: FarrObject, month: FarrObject, day: FarrObject) -> str:
        date_obj = datetime.date(year.to_int(), month.to_int(), day.to_int())
        return date_obj.isoformat()
    
    def time_isoformat(self, hour: FarrObject, minute: FarrObject, second: FarrObject, microsecond: FarrObject = FarrObject()) -> str:
        time_obj = datetime.time(hour.to_int(), minute.to_int(), second.to_int(), microsecond.to_int())
        return time_obj.isoformat()
    
    def fromisoformat_date(self, date_string: FarrObject) -> str:
        return str(datetime.date.fromisoformat(date_string.to_str()))
    
    def fromisoformat_time(self, time_string: FarrObject) -> str:
        return str(datetime.time.fromisoformat(time_string.to_str()))
    
    def week(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d")
        return str(dt_obj.isocalendar()[1])
    
    def year(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d")
        return str(dt_obj.year)
    
    def month(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d")
        return str(dt_obj.month)
    
    def day(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d")
        return str(dt_obj.day)

    def hour(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S")
        return str(dt_obj.hour)

    def minute(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S")
        return str(dt_obj.minute)

    def second(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S")
        return str(dt_obj.second)

    def microsecond(self, dt: FarrObject) -> str:
        dt_obj = datetime.datetime.strptime(dt.to_str(), "%Y-%m-%d %H:%M:%S")
        return str(dt_obj.microsecond)

    def maxyear(self) -> str:
        return str(datetime.MAXYEAR)

    def minyear(self) -> str:
        return str(datetime.MINYEAR)





    
class SocketLIB(PythonNativeObject):
    def __call__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _send_request(self, host, port, path, method='GET', headers=None, data=None):
        if headers is None:
            headers = {}
        if data is not None:
            headers['Content-Length'] = str(len(data))
        request_headers = '\r\n'.join([f"{key}: {value}" for key, value in headers.items()])
        request = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\n{request_headers}\r\n\r\n"
        if data is not None:
            request += data
        self._socket.sendall(request.encode())

    def _receive_response(self):
        response = b""
        while True:
            chunk = self._socket.recv(1024)
            if not chunk:
                break
            response += chunk
        return response

    def _parse_url(self, url):
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port if parsed_url.port else 80
        path = parsed_url.path if parsed_url.path else '/'
        return host, port, path

    def get(self, url, headers):
        host, port, path = self._parse_url(url)
        self._socket.connect((host, port))
        self._send_request(host, port, path, method='GET', headers=headers)
        response = self._receive_response()
        self._socket.close()
        return response

    def post(self, url, data, headers):
        host, port, path = self._parse_url(url)
        self._socket.connect((host, port))
        if data:
            headers['Content-Length'] = str(len(data))
        self._send_request(host, port, path, method='POST', headers=headers, data=data)
        response = self._receive_response()
        self._socket.close()
        return response

    def put(self, url, data, headers):
        host, port, path = self._parse_url(url)
        self._socket.connect((host, port))
        if data:
            headers['Content-Length'] = str(len(data))
        self._send_request(host, port, path, method='PUT', headers=headers, data=data)
        response = self._receive_response()
        self._socket.close()
        return response

    def delete(self, url, headers=None):
        host, port, path = self._parse_url(url)
        self._socket.connect((host, port))
        self._send_request(host, port, path, method='DELETE', headers=headers)
        response = self._receive_response()
        self._socket.close()
        return response

    def download_file(self, url, filename):
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

    def parse_html(self, html):
        return BeautifulSoup(html, 'html.parser')

    def find_element_by_tag(self, soup, tag):
        return soup.find(tag)

    def find_all_elements_by_tag(self, soup, tag):
        return soup.find_all(tag)

import hashlib
from cryptography.fernet import Fernet

class cryptohh(PythonNativeObject):
        def __call__(self, arg:FarrObject):
            return type(arg)

        def md5(self, data):
            return hashlib.md5(str(data).encode()).hexdigest()

        def sha1(self, data):
            return hashlib.sha1(str(data).encode()).hexdigest()

        def sha256(self, data):
            return hashlib.sha256(str(data).encode()).hexdigest()

        def sha512(self, data):
            return hashlib.sha512(str(data).encode()).hexdigest()
        
class cryptofernet(PythonNativeObject):
        def __call__(self, key=None):
            if key:
                self.key = key.encode()
            else:
                self.key = Fernet.generate_key()
            self.cipher = Fernet(self.key)

        def encrypt(self, data):
            return self.cipher.encrypt(str(data).encode()).decode()

        def decrypt(self, data):
            return self.cipher.decrypt(str(data).encode()).decode()

        def get_key(self):
            return self.key.decode()

class UseModLib(PythonNativeObject):
    def require(self,arg: FarrObject) -> string:
        # print(UseNode(
        #     path=arg
        # ))
        return UseNode(
            path=arg
        )

##################################
### SINGLE LINE BASIC COMMANDS ###
##################################

class LenghtLIB(PythonNativeObject):
    def __call__(self, arg:FarrObject) -> list:
        return len(list(arg))

class TypeLIB(PythonNativeObject):
    def __call__(self, arg:FarrObject):
        return type(arg)

    def to_string(self, arg:FarrObject):
        return str(arg)
    
    def to_float(self, arg:FarrObject):
        return float(str(arg))
    
    def to_int(self, arg:FarrObject):
        return int(str(arg))
    
    def to_list(self, arg:FarrObject):
        return list(arg)
    


    def toString(self, arg:FarrObject):
        return str(arg)
    
    def toFloat(self, arg:FarrObject):
        return float(str(arg))
    
    def toInt(self, arg:FarrObject):
        return int(str(arg))
    
    def toList(self, arg:FarrObject):
        return list(arg)

###################################
### INTERMEDIATE LEVEL COMMANDS ###
###################################

class PyTorchLIB(PythonNativeObject):
    def tensor(self, data: List[List[float]]) -> List[List[float]]:
        return data

    def zeros(self, shape: List[int]) -> List[List[float]]:
        return [[0] * shape[1] for _ in range(shape[0])]

    def ones(self, shape: List[int]) -> List[List[float]]:
        return [[1] * shape[1] for _ in range(shape[0])]

    def randn(self, shape: List[int]) -> List[List[float]]:
        import random
        return [[random.random() for _ in range(shape[1])] for _ in range(shape[0])]

    def randint(self, low: int, high: int, shape: List[int]) -> List[List[int]]:
        import random
        return [[random.randint(low, high) for _ in range(shape[1])] for _ in range(shape[0])]

    def eye(self, n: int) -> List[List[float]]:
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def arange(self, start: int, stop: int, step: int = 1) -> List[int]:
        return list(range(start, stop, step))

    def add(self, a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
        return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

    def mul(self, a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
        return [[a[i][j] * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

    def matmul(self, a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
        return [[sum(a[i][k] * b[k][j] for k in range(len(a[0]))) for j in range(len(b[0]))] for i in range(len(a))]

class NumPyLIB(PythonNativeObject):
    def array(self, *args: List[float]) -> List[float]:
        return list(args)

    def mean(self, arg: List[float]) -> float:
        return sum(arg) / len(arg)

    def sum(self, arg: List[float]) -> float:
        return sum(arg)

    def min(self, arg: List[float]) -> float:
        return min(arg)

    def max(self, arg: List[float]) -> float:
        return max(arg)

    def reshape(self, arg: List[float], shape: List[int]) -> List[float]:
        return [arg[i:i + shape[1]] for i in range(0, len(arg), shape[1])]

    def concatenate(self, arrays: List[List[float]]) -> List[float]:
        return [item for sublist in arrays for item in sublist]

    def dot(self, a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
        return [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*b)] for row_a in a]

    def arange(self, start: int, stop: int, step: int = 1) -> List[int]:
        return list(range(start, stop, step))

    def zeros(self, shape: List[int]) -> List[float]:
        return [0] * shape[0] * shape[1]

    def ones(self, shape: List[int]) -> List[float]:
        return [1] * shape[0] * shape[1]

    def identity(self, n: int) -> List[List[float]]:
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def linspace(self, start: float, stop: float, num: int) -> List[float]:
        step = (stop - start) / (num - 1)
        return [start + i * step for i in range(num)]

    def random(self, shape: List[int]) -> List[float]:
        import random
        return [random.random() for _ in range(shape[0] * shape[1])]

class PandasLIB(PythonNativeObject):
    def DataFrame(self, data: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        return data

    def head(self, df: Dict[str, List[Any]], n=5) -> Dict[str, List[Any]]:
        return {key: value[:n] for key, value in df.items()}

    def describe(self, df: Dict[str, List[Any]]) -> Dict[str, Dict[str, Any]]:
        description = {}
        for key, value in df.items():
            description[key] = {
                'mean': sum(value) / len(value),
                'count': len(value),
                'min': min(value),
                'max': max(value)
            }
        return description

    def merge(self, df1: Dict[str, List[Any]], df2: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        return {**df1, **df2}

    def concat(self, dfs: List[Dict[str, List[Any]]]) -> Dict[str, List[Any]]:
        result = {}
        for df in dfs:
            for key, value in df.items():
                if key not in result:
                    result[key] = []
                result[key].extend(value)
        return result

    def filter(self, df: Dict[str, List[Any]], condition: bool) -> Dict[str, List[Any]]:
        return {key: value for key, value in df.items() if condition}

    def groupby(self, df: Dict[str, List[Any]], by: str) -> Dict[str, Dict[Any, List[Any]]]:
        groups = {}
        for i, key in enumerate(df[by]):
            if key not in groups:
                groups[key] = {}
            for col, val in df.items():
                if col != by:
                    if i not in groups[key]:
                        groups[key][i] = []
                    groups[key][i].append(val[i])
        return groups

    def dropna(self, df: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        return {key: [v for v in value if v is not None] for key, value in df.items()}

    def fillna(self, df: Dict[str, List[Any]], value: Any) -> Dict[str, List[Any]]:
        return {key: [v if v is not None else value for v in value] for key, value in df.items()}

    def sort_values(self, df: Dict[str, List[Any]], by: str, ascending: bool = True) -> Dict[str, List[Any]]:
        index = sorted(range(len(df[by])), key=lambda i: df[by][i], reverse=not ascending)
        return {key: [value[i] for i in index] for key, value in df.items()}

    def drop_duplicates(self, df: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        seen = set()
        result = {key: [] for key in df.keys()}
        for i, row in enumerate(zip(*df.values())):
            if row not in seen:
                seen.add(row)
                for j, value in enumerate(row):
                    result[list(df.keys())[j]].append(value)
        return result

    def to_csv(self, df: Dict[str, List[Any]], filename: str) -> None:
        with open(filename, 'w') as f:
            for i in range(len(df[list(df.keys())[0]])):
                f.write(','.join([str(df[key][i]) for key in df.keys()]) + '\n')

class MatplotlibLIB(PythonNativeObject):
    def plot(self, x: List[float], y: List[float]) -> List[tuple]:
        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Plot')
        plt.grid(True)
        plt.show()
        return list(zip(x, y))

    def scatter(self, x: List[float], y: List[float]) -> List[tuple]:
        plt.scatter(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Scatter Plot')
        plt.grid(True)
        plt.show()
        return list(zip(x, y))

    def hist(self, data: List[float]) -> List[float]:
        plt.hist(data)
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title('Histogram')
        plt.grid(True)
        plt.show()
        return data

    def bar(self, x: List[str], height: List[float]) -> List[tuple]:
        plt.bar(x, height)
        plt.xlabel('Category')
        plt.ylabel('Value')
        plt.title('Bar Chart')
        plt.grid(True)
        plt.show()
        return list(zip(x, height))

    def pie(self, data: Dict[str, float]) -> List[tuple]:
        labels = list(data.keys())
        sizes = list(data.values())
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('Pie Chart')
        plt.show()
        return list(data.items())

    def boxplot(self, data: List[List[float]]) -> List[tuple]:
        plt.boxplot(data)
        plt.xlabel('Category')
        plt.ylabel('Value')
        plt.title('Box Plot')
        plt.grid(True)
        plt.show()
        return [tuple(sublist) for sublist in data]

    def violinplot(self, data: List[List[float]]) -> List[tuple]:
        plt.violinplot(data)
        plt.xlabel('Category')
        plt.ylabel('Value')
        plt.title('Violin Plot')
        plt.grid(True)
        plt.show()
        return [tuple(sublist) for sublist in data]

###################################
### INTERMEDIATE LEVEL COMMANDS ###
###################################

# Placeholder classes for representing data and models
class Model:
    pass

class NeuralNetworkModel:
    pass

class LearnForgeLIB(PythonNativeObject):
    def __init__(self):
        self.model = None

    def train(self, X_train: List[List[float]], y_train: List[float]) -> str:
        # Placeholder method for training a machine learning model
        self.model = Model()  # Dummy model for illustration
        return "Model trained successfully"

    def predict(self, X_test: List[List[float]]) -> List[float]:
        # Placeholder method for making predictions using a trained model
        if self.model is None:
            raise RuntimeError("Model is not trained")
        return [0.5] * len(X_test)  # Dummy predictions for illustration

    def load_model(self, path: str) -> str:
        # Placeholder method for loading a trained model from a file
        self.model = Model()  # Dummy model for illustration
        return "Model loaded successfully"

    def save_model(self, path: str) -> str:
        # Placeholder method for saving a trained model to a file
        if self.model is None:
            raise RuntimeError("Model is not trained")
        return "Model saved successfully"

    def evaluate(self, X_test: List[List[float]], y_test: List[float]) -> Dict[str, float]:
        # Placeholder method for evaluating a trained model
        if self.model is None:
            raise RuntimeError("Model is not trained")
        return {"accuracy": 0.75, "loss": 0.2}  # Dummy evaluation metrics for illustration

    def get_params(self) -> Dict[str, Any]:
        # Placeholder method for getting parameters of the trained model
        if self.model is None:
            raise RuntimeError("Model is not trained")
        return {"param1": 1, "param2": "abc"}  # Dummy parameters for illustration

    def set_params(self, **params: Any) -> None:
        # Placeholder method for setting parameters of the trained model
        if self.model is None:
            raise RuntimeError("Model is not trained")
        pass  # Dummy implementation for illustration

    # Implement additional commands...

class TensorForgeLIB(PythonNativeObject):
    def __init__(self):
        self.model = None

    def build_model(self, input_shape: List[int]) -> str:
        # Placeholder method for building a neural network model
        self.model = NeuralNetworkModel()  # Dummy model for illustration
        return "Neural network model built successfully"

    def compile_model(self, optimizer: str, loss: str, metrics: List[str]) -> str:
        # Placeholder method for compiling a neural network model
        if self.model is None:
            raise RuntimeError("Model is not built")
        return "Neural network model compiled successfully"

    def train_model(self, X_train: List[List[float]], y_train: List[float], epochs: int, batch_size: int) -> str:
        # Placeholder method for training a neural network model
        if self.model is None:
            raise RuntimeError("Model is not compiled")
        return "Neural network model trained successfully"

    def evaluate_model(self, X_test: List[List[float]], y_test: List[float]) -> Dict[str, float]:
        # Placeholder method for evaluating a neural network model
        if self.model is None:
            raise RuntimeError("Model is not trained")
        return {"accuracy": 0.75, "loss": 0.2}  # Dummy evaluation metrics for illustration

    def save_model(self, path: str) -> str:
        # Placeholder method for saving a trained model to a file
        if self.model is None:
            raise RuntimeError("Model is not trained")
        return "Model saved successfully"

    def load_model(self, path: str) -> str:
        # Placeholder method for loading a trained model from a file
        self.model = NeuralNetworkModel()  # Dummy model for illustration
        return "Model loaded successfully"

    def get_weights(self) -> List[List[float]]:
        # Placeholder method for getting weights of the trained model
        if self.model is None:
            raise RuntimeError("Model is not trained")
        return [[0.1, 0.2], [0.3, 0.4]]  # Dummy weights for illustration

    def set_weights(self, weights: List[List[float]]) -> None:
        # Placeholder method for setting weights of the trained model
        if self.model is None:
            raise RuntimeError("Model is not trained")
        pass  # Dummy implementation for illustration
    
# from sklearn.linear_model import LinearRegression
# import numpy as np

# class LinePredictorLIB:
#     def __call__(self):
#         self.model = LinearRegression()

#     def __init__(self):
#         self.model = LinearRegression()

#     def train(self, X_train, y_train):
#         """Train the regression model."""
#         X_train = np.array(X_train).reshape(-1, 1)  # Reshape X_train if needed
#         y_train = np.array(y_train)
#         self.model.fit(X_train, y_train)

#     def predict(self, X_test):
#         """Predict future lines based on X_test."""
#         X_test = np.array(X_test).reshape(-1, 1)  # Reshape X_test if needed
#         return self.model.predict(X_test)

import os

class Shell(PythonNativeObject):
    def __call__(self, arg:FarrObject) -> list:
        os.system(str(arg))

class PowerShell(PythonNativeObject):
    def __call__(self, arg:FarrObject) -> list:
        os.system(f"powershell && {str(arg)}")

