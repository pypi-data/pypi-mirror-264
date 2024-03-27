from typing import List, Union
from pcombinator.combinators.combinator import Combinator, Path, derived_classes
from pcombinator.util.classname import get_fully_qualified_class_name


class NamedString(Combinator):
    """
    A combinator that renders a fixed string.

    NOTE: This is only necessary when you want to preserve the id of the string in the Path. Otherwise you can just use a string as a child of a higher combinator.
    """

    string: str

    def __init__(
        self,
        id: str,
        string: str,
        **kwargs,
    ):
        """
        Initialize a new FixedStringCombinator.

        Args:
            id: The id of the combinator.
            string: The string to render.
        """
        super().__init__(
            id=id,
            combinator_type=kwargs.get("combinator_type")
            or get_fully_qualified_class_name(self.__class__),
        )

        if not isinstance(string, str) or string is None:
            raise ValueError(f"string must be a string, not {type(string)}")

        self.string = string

    def generate_paths(self) -> List[Path]:
        """
        Generate all paths in the tree under this combinator id.
        """
        return [{self.id: {}}]

    def render_path(self, path: Path) -> Union[str, None]:
        """
        Render a specific path. In our case the path is expected to be empty.
        """
        if path != {self.id: {}}:
            raise ValueError(
                "render_path called with either incorrect id or with children (this combinator does not support children)"
            )
        res = self.string
        return res

    @classmethod
    def from_json(cls, values: dict):
        return cls(
            id=values["id"],
            string=values["string"],
        )


Combinator.register_derived_class(NamedString)
