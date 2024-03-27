from typing import List, Union
from pcombinator.combinators.combinator import Combinator
from pcombinator.combinators.random_join_combinator import RandomJoinCombinator


class OneOfCombinator(RandomJoinCombinator):
    """
    On render, this combinator will randomly select one of the children and render it.
    """    

    def __init__(
        self,
        seed: Union[int, None] = None,
        children: List[Union[Combinator, str]] = [],
        id: str = None,
    ):
        super().__init__(1, 1, "", seed, children, id)
        self._combinator_type = "one_of"
