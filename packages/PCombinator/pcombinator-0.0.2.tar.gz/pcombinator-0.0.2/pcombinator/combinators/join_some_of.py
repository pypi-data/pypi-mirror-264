import itertools
from typing import Any, List, Union

from pcombinator.combinators.combinator import (
    Combinator,
    Path,
    combinator_dict_to_obj,
    derived_classes,
)
from pcombinator.combinators.combinator_or_leaf_type import CombinatorOrLeaf
from pcombinator.util.classname import get_fully_qualified_class_name


class JoinSomeOf(Combinator):
    """
    On render, this combinator will select a number of children between n_min and n_max (inclusive)
    and join them with the separator.
    """

    children: List[CombinatorOrLeaf]
    n_min: int
    n_max: int
    separator: str

    def __init__(
        self,
        id: str,
        n_min: int = 1,
        n_max: int = 1,
        separator: str = "\n",
        children: List[CombinatorOrLeaf] = [],
        **kwargs,
    ):
        super().__init__(
            id=id,
            combinator_type=kwargs.get("combinator_type")
            or get_fully_qualified_class_name(self.__class__),
        )
        # Verify that children is a list with at least one element
        if not isinstance(children, list) or len(children) == 0:
            raise ValueError("children must be a list with at least one element")

        # Verify that n_min and n_max are integers, that n_min is at least 0 and that n_max is at least n_min
        if not isinstance(n_min, int) or n_min < 0:
            raise ValueError("n_min must be a non negative integer")
        if not isinstance(n_max, int) or n_max < n_min:
            raise ValueError("n_max must be an integer greater than or equal to n_min")

        # Verify that separator is a string
        if not isinstance(separator, str):
            raise ValueError("separator must be a string")

        self.n_min = n_min
        self.n_max = n_max
        self.separator = separator
        self.children = children

    def generate_paths(self) -> List[Path]:

        # Generate all unique combinations of n_min to n_max children indices
        children_indices_combinations = []
        for n_children in range(self.n_min, self.n_max + 1):
            # Create a combination
            combination = itertools.permutations(range(len(self.children)), n_children)
            # Add it to the list
            children_indices_combinations.extend(list(combination))

        # Generate all paths for each combination
        paths = []
        for children_indices_combination in children_indices_combinations:
            paths.extend(
                self._generate_paths_for_children_indices(children_indices_combination)
            )

        return paths

    def _generate_paths_for_children_indices(
        self, children_indices_combination: List[int]
    ) -> List[Path]:
        # Each combination is a list of child indices in the order of inclusion
        path = {self.id: {}}

        all_child_paths = []
        for i, child_index in enumerate(children_indices_combination):
            child = self.children[child_index]
            child_paths = self._get_paths_for_child(child)
            all_child_paths.append(child_paths)  # Appends a list

        all_child_paths_combinations = itertools.product(*all_child_paths)

        # Each combination form all_child_paths_combinations is a single path across all children
        # Reorgaze each into a dict with the child index as key
        paths = []
        for child_paths_combination in all_child_paths_combinations:
            path[self.id] = {}
            for i, child_index in enumerate(children_indices_combination):
                path[self.id][str(child_index)] = child_paths_combination[i]
            paths.append(path.copy())

        return paths

    def _get_paths_for_child(self, child) -> List[Path]:
        if child is None:
            return [{}]
        elif isinstance(child, str):
            return [child]
        else:
            return child.generate_paths()

    def render_path(self, path: Path) -> Union[str, None]:
        """
        Render self for a specific path in the tree.
        """

        # Verify that the path is a dict containing only the id of this combinator
        if len(path) != 1 or self.id not in path:
            raise ValueError(
                f"Path must contain the id of this combinator at the top level: {self.id}"
            )

        # Get the children indices by the keys appearing below the id
        children_indices = list(path[self.id].keys())

        # Render the children
        rendered_children = []
        for child_index in children_indices:
            child = self.children[int(child_index)]
            path_for_child = path[self.id][child_index]
            rendered_child = (
                child
                if isinstance(child, str)
                else child.render_path(path_for_child) if child is not None else None
            )
            rendered_children.append(rendered_child)

        # Remove all None values
        rendered_children = [child for child in rendered_children if child is not None]

        # Join the children
        rendered = self.separator.join(rendered_children)

        return rendered

    def add_child(self, child: CombinatorOrLeaf) -> None:
        self.children.append(child)

    def get_children(self) -> List[CombinatorOrLeaf]:
        return self.children

    def remove_child_by_id(self, id: str) -> None:
        for i, child in enumerate(self.children):
            if child.get_id() == id:
                del self.children[i]
                return

    @classmethod
    def from_json(cls, values: dict):

        return cls(
            id=values["id"],
            n_min=values["n_min"],
            n_max=values["n_max"],
            separator=values["separator"],
            children=[Combinator.from_json(child) for child in values["children"]],
        )


Combinator.register_derived_class(JoinSomeOf)
