import random
from typing import List, Union

from pcombinator.combinators.combinator import Combinator, IdTree, render_children


class RandomJoinCombinator(Combinator):
    """
    On render, this combinator will randomly select a number of children between n_min and n_max (inclusive)
    and join them with the separator.
    """


    children: List[Union["Combinator", str]]

    def __init__(
        self,
        n_min: int = 1,
        n_max: int = 1,
        separator: str = "\n",
        seed: Union[int, None] = None,  # TODO: Determine if seed is better placed at render()
        children: List[Union["Combinator", str]] = [],
        id: str = None,
    ):
        super().__init__(id=id)
        self._combinator_type = "random_join"
        self.n_min = n_min
        self.n_max = n_max
        self.separator = separator
        self.seed = seed
        self.children = children

    def render(self) -> (str, IdTree):
        # Choose how many children will be selected
        n_children = random.randint(self.n_min, self.n_max)

        # Select children (without replacement)
        selected_children = random.sample(self.children, n_children)

        # Render children
        rendered_children, rendered_child_id_tree = render_children(
            selected_children
        )

        # Join children
        rendered = self.separator.join(rendered_children)

        # Return
        return rendered, {self.id: rendered_child_id_tree}

    def add_child(self, child: Union[Combinator, str]) -> None:
        self.children.append(child)

    def get_children(self) -> List[Union[Combinator, str]]:
        return self.children

    def remove_child_by_id(self, id: str) -> None:
        for i, child in enumerate(self.children):
            if child.get_id() == id:
                del self.children[i]
                return
