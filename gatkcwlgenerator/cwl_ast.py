"""
Classes to make an AST for CWL types
"""
import abc

class CWLType:
    __metaclass__ = abc.ABCMeta

    def __eq__(self, other):
        if self.is_leaf() and other.is_leaf():
            if type(self) is type(other):
                raise NotImplementedError(f"Leaf comparison not implemented for {type(self)} (__eq__ should be overloaded)")
            else:
                return False
        elif not self.is_leaf() and not other.is_leaf():
            return all((other_child == self_child for (other_child, self_child) in zip(other.children, self.children)))
        else:
            return False

    @abc.abstractmethod
    def get_cwl_object(self):
        pass

    def has_array_type(self):
        return self.find_node(lambda node: isinstance(node, CWLArrayType)) is not None

    def has_file_type(self):
        def is_file_type(cwl_type):
            return isinstance(cwl_type, CWLBasicType) and cwl_type.name == "File"

        return self.find_node(is_file_type) is not None

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


class CWLBasicType(CWLType):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def get_cwl_object(self):
        return self.name


class CWLArrayType(CWLType):
    def __init__(self, inner_type):
        self.inner_type = inner_type
        self._input_binding = None

    def add_input_binding(self, inputBinding):
        self._input_binding = inputBinding

    def get_cwl_object(self):
        inner_cwl_object = self.inner_type.get_cwl_object()

        if isinstance(inner_cwl_object, str) and self._input_binding is None:
            return inner_cwl_object + "[]"
        else:
            cwl_object = {
                "type": "array",
                "items": self.inner_type.get_cwl_object()
            }

            if self._input_binding is not None:
                cwl_object["inputBinding"] = self._input_binding

            return cwl_object


class CWLUnionType(CWLType):
    def __init__(self, *items):
        self.items = items

    def get_cwl_object(self):
        cwl_object = []

        for item in self.items:
            if isinstance(item, CWLUnionType):
                cwl_object.extend(item.get_cwl_object())
            else:
                cwl_object.append(item.get_cwl_object())

        return cwl_object

    @property
    def children(self):
        return self.items


class CWLEnumType(CWLType):
    def __init__(self, symbols):
        self.symbols = symbols

    def get_cwl_object(self):
        return {
            "type": "enum",
            "symbols": self.symbols
        }

class CWLOptionalType(CWLType):
    def __init__(self, inner_type):
        self.inner_type = inner_type

    def get_cwl_object(self):
        inner_cwl_object = self.inner_type.get_cwl_object()

        if isinstance(inner_cwl_object, str):
            return inner_cwl_object + "?"
        elif isinstance(inner_cwl_object, list):
            return ["null"] + inner_cwl_object
        else:
            return [
                "null",
                inner_cwl_object
            ]
