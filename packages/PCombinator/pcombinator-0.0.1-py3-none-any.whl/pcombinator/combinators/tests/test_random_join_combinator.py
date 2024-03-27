import unittest
from unittest.mock import patch
from pcombinator.combinators.random_join_combinator import RandomJoinCombinator
from pcombinator.combinators.combinator import render_children


class RandomJoinCombinatorTests(unittest.TestCase):
    def test_render(self):
        random_join_combinator = RandomJoinCombinator(
            n_min=2,
            n_max=4,
            children=["abc", "def", "ghi"],
            separator="-",
            id="test_combinator_id",
        )

        with \
            patch("random.randint") as mock_randint, \
            patch("random.sample") as mock_sample:
            # patch("render_children") as mock_render_children:

            mock_randint.return_value = 3
            mock_sample.return_value = ["def", "abc", "ghi"]
            # mock_render_children.return_value = (
            #     ["ABC", "DEF", "GHI"],
            #     {"test_id": "child_id_tree"},
            # )

            rendered, id_tree = random_join_combinator.render()

            self.assertEqual(rendered, "def-abc-ghi")
            self.assertEqual(id_tree, {'test_combinator_id': {}})

            mock_randint.assert_called_once_with(2, 4)
            mock_sample.assert_called_once_with(["abc", "def", "ghi"], 3)
            # mock_render_children.assert_called_once_with(["abc", "def", "ghi"])


if __name__ == "__main__":
    unittest.main()
