import json
from typing import Any, Dict, List, NewType, Optional, Type, Union

from pcombinator.util.classname import get_fully_qualified_class_name

Path = NewType("Path", Dict[str, "Path"])


class Combinator:
    """
    Base class for combinators.
    """

    combinator_type: str
    id: str

    def __init__(self, id: str, combinator_type: Optional[str], **kwargs):
        super().__init__(**kwargs)

        self.id = id
        if combinator_type is not None:
            # From deserialization
            self.combinator_type = combinator_type
            # Verify that the combinator type is known
            self.__class__.verify_known_combinator_type(self.combinator_type)
        else:
            # Otherwise
            self.combinator_type = get_fully_qualified_class_name(self.__class__)
            # Allow implicit registration of derived classes
            self.__class__.register_derived_class(self.__class__)

    @classmethod
    def verify_known_combinator_type(cls, combinator_type: str):
        if combinator_type not in derived_classes:
            raise ValueError(
                f"No registered combinator implementation for: {combinator_type}"
            )

    @classmethod
    def register_derived_class(cls, derived_class):
        fq_cls_name = get_fully_qualified_class_name(derived_class)
        # Verify that this has not been registered before with a different name
        if fq_cls_name in derived_classes:
            if derived_classes[fq_cls_name] != derived_class:
                raise ValueError(
                    f"Class {fq_cls_name} already registered with a different class"
                )
        else:
            derived_classes[fq_cls_name] = derived_class

    def get_id(self):
        """
        Get the id of the combinator.
        """
        return self.id

    def generate_paths(self) -> List[Path]:
        """
        Generate all paths in the tree under this combinator id.
        """
        raise NotImplementedError("generate_paths() not implemented")

    def render_path(self, path: Path) -> Union[str, None]:
        """
        Render one specific path. To be implemented by subclasses.
        """
        raise NotImplementedError("render_path() not implemented")

    @staticmethod
    def default(obj):
        """
        Default method to serialize objects. If the object has a `to_json` method, it uses it.
        """
        if hasattr(obj, "to_json"):
            return obj.to_json()
        raise TypeError(
            f"default() - Object of type {obj.__class__.__name__} is not JSON serializable"
        )

    def to_json(self):
        return json.dumps(
            self.to_dict(),
            default=self.default,
        )

    def to_dict(self):
        res = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return res

    @classmethod
    def from_dict(cls, values: dict):
        """
        Create a new combinator from a dictionary.
        """
        combinator_type = values["combinator_type"]
        if combinator_type in derived_classes:
            return derived_classes[combinator_type].from_json(values)
        else:
            raise ValueError(f"Unknown combinator type (from_json): {combinator_type}")

    @classmethod
    def from_json(cls, json_str: str):
        if not json_str.startswith("{"):
            # Workaround for the stange nesting rules of the json parser
            return json_str
        values = json.loads(json_str)
        # If string value or none just return the value
        if not isinstance(values, dict):
            return values
        return cls.from_dict(values)


# Map of combinator types to classes
derived_classes: Dict[str, Type[Combinator]] = {}


def combinator_dict_to_obj(
    child: Union[dict, str, None]
) -> Union[str, None, Combinator]:
    # No need to convert string and None
    if not isinstance(child, dict):
        return child

    combinator_type = child.get("combinator_type")
    if combinator_type in derived_classes:
        derived_class = derived_classes[combinator_type]
        return derived_class(child)  # TODO: need to unwrap the dict
    else:
        raise ValueError(
            f"combinator_dict_to_obj: cannot convert dict to combinator object - unknown combinator type: {combinator_type}"
        )
