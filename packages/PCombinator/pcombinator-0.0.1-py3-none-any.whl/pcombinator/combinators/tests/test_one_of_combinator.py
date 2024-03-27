import unittest
from pcombinator.combinators.one_of_combinator import OneOfCombinator
from pcombinator.combinators.combinator import Combinator


class OneOfCombinatorTests(unittest.TestCase):
    def test_initialization(self):
        one_of_combinator = OneOfCombinator(
            seed=123, children=["abc", "def"], id="test_id"
        )
        self.assertEqual(one_of_combinator._combinator_type, "one_of")
        self.assertEqual(one_of_combinator.n_min, 1)
        self.assertEqual(one_of_combinator.n_max, 1)
        self.assertEqual(one_of_combinator.seed, 123)
        self.assertEqual(one_of_combinator.children, ["abc", "def"])
        self.assertEqual(one_of_combinator.id, "test_id")

    def test_default_values(self):
        one_of_combinator = OneOfCombinator()
        self.assertEqual(one_of_combinator._combinator_type, "one_of")
        self.assertEqual(one_of_combinator.n_min, 1)
        self.assertEqual(one_of_combinator.n_max, 1)
        self.assertIsNone(one_of_combinator.seed)
        self.assertEqual(one_of_combinator.children, [])
        self.assertIsNone(one_of_combinator.id)

    # Add more test cases as needed


if __name__ == "__main__":
    unittest.main()
