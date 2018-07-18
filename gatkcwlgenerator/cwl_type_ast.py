"""
Classes to make an AST for CWL types
"""
import abc
from abc import abstractmethod
import copy
from typing import *

class CWLType:
    __metaclass__ = abc.ABCMeta

    def __eq__(self, other: 'CWLType'):
        if self.is_leaf() and other.is_leaf():
            if type(self) is type(other):
                raise NotImplementedError(f"Leaf comparison not implemented for {type(self)} (__eq__ should be overloaded)")
            else:
                return False
        elif not self.is_leaf() and not other.is_leaf():
            return all((other_child == self_child for (other_child, self_child) in zip(other.children, self.children)))
        else:
            return False

    @abstractmethod
    def get_cwl_object(self, expand_types=False):
        pass

    def has_array_type(self):
        return self.find_node(lambda node: isinstance(node, CWLArrayType)) is not None

    def contains(self, other_type: 'CWLType'):
        return self == other_type

    def has_file_type(self):
        return self.find_node(lambda cwl_type: cwl_type == CWLFileType()) is not None

    def is_leaf(self):
        """
        Returns True if this element has no children.
        """
        try:
            self.children
        except AttributeError:
            return True

        return False

    @property
    def children(self):
        if hasattr(self, "inner_type"):
            return [getattr(self, "inner_type")]
        else:
            raise AttributeError(repr(self) + " has no children")

    def find_node(self, predicate):
        """
        Traverses the AST to find a node that satifies the given predicate.
        If the no node is found, returns None
        """
        if predicate(self):
            return self
        else:
            try:
                return next(filter(None, (child.find_node(predicate) for child in self.children)))
            except (AttributeError, StopIteration):
                return None

class CWLArrayType(CWLType):
    def __init__(self, inner_type):
        self.inner_type = inner_type
        self._input_binding = None

    def add_input_binding(self, inputBinding):
        self._input_binding = inputBinding

    def get_cwl_object(self, expand_types=False):
        # NOTE: the cwl spec's schema salad doesn't expand variables on the property items
        # so we have to expand the type manually
        # issue: https://github.com/common-workflow-language/common-workflow-language/issues/608
        inner_cwl_object = self.inner_type.get_cwl_object(True)

        if isinstance(inner_cwl_object, str) and self._input_binding is None and not expand_types:
            return inner_cwl_object + "[]"
        else:
            cwl_object = {
                "type": "array",
                "items": inner_cwl_object
            }

            if self._input_binding is not None:
                cwl_object["inputBinding"] = self._input_binding

            return cwl_object

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.inner_type!r})"


class CWLUnionType(CWLType):
    def __init__(self, *items):
        self.items = items

    def contains(self, other_type: CWLType):
        return any(map(lambda item: item.contains(other_type), self.items))

    def get_cwl_object(self, expand_types=False):
        cwl_object = []

        for item in self.items:
            if isinstance(item, CWLUnionType):
                cwl_object.extend(item.get_cwl_object(expand_types))
            else:
                cwl_object.append(item.get_cwl_object(expand_types))

        return cwl_object

    @property
    def children(self):
        return self.items

    def __repr__(self):
        return f"{type(self).__name__}({self.items!r})"


class CWLEnumType(CWLType):
    def __init__(self, symbols):
        self.symbols = symbols

    def get_cwl_object(self, expand_types=False):
        return {
            "type": "enum",
            "symbols": copy.deepcopy(self.symbols)
        }

    def __repr__(self):
        return f"{type(self).__name__}({self.symbols!r})"


class CWLOptionalType(CWLType):
    def __init__(self, inner_type):
        self.inner_type = inner_type

    def get_cwl_object(self, expand_types=False):
        inner_cwl_object = self.inner_type.get_cwl_object(expand_types)

        if isinstance(inner_cwl_object, str) and not expand_types:
            return inner_cwl_object + "?"
        elif isinstance(inner_cwl_object, list):
            return ["null"] + inner_cwl_object
        else:
            return [
                "null",
                inner_cwl_object
            ]

    def contains(self, other_type: CWLType):
        return self.inner_type.contains(other_type)

    def __repr__(self):
        return f"{type(self).__name__}({self.inner_type!r})"

class CWLBasicType(CWLType):
    __metaclass__ = abc.ABCMeta

    subtypes = [] # type: List[CWLType]

    def contains(self, other_type: CWLType):
        if type(self) is type(other_type):
            return True
        else:
            return any(map(lambda subtype: subtype.contains(other_type), self.subtypes))

    @property
    @abstractmethod
    def name(self):
        pass

    def __eq__(self, other):
        return self.name == other.name

    def get_cwl_object(self, expand_types=False):
        return self.name

    def __repr__(self):
        return f"{type(self).__name__}()"

def get_cwl_basic_type(basic_type_name: str):
    try:
        return globals()[f"CWL{basic_type_name.title()}Type"]()
    except KeyError as error:
        raise Exception(f"No CWL type of name {basic_type_name} found") from error

class CWLFileType(CWLBasicType):
    name = "File"

class CWLDirectoryType(CWLBasicType):
    name = "Directory"

class CWLStringType(CWLBasicType):
    name = "string"
    def contains(self, other_type: CWLType):
        return type(self) is type(other_type) or type(other_type) is CWLEnumType

class CWLIntType(CWLBasicType):
    name = "int"

class CWLLongType(CWLBasicType):
    name = "long"
    subtypes = [CWLIntType()]

class CWLFloatType(CWLBasicType):
    name = "float"
    subtypes = [CWLLongType()]

class CWLDoubleType(CWLBasicType):
    name = "double"
    subtypes = [CWLFloatType()]

class CWLBooleanType(CWLBasicType):
    name = "boolean"
