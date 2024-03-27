import unittest
from unittest.mock import patch

from pcombinator.combinators import JoinSomeOf


class JoinSomeOfTests(unittest.TestCase):
    def setUp(self) -> None:
        self.three_values_some_of_combinator = JoinSomeOf(
            id="test_combinator_id_1",
            n_min=2,
            n_max=3,
            children=["abc", "def", "ghi"],
            separator="-",
        )

        self.five_values_some_of_combinator = JoinSomeOf(
            id="test_combinator_id_2",
            n_min=2,
            n_max=4,
            children=["abc", "def", "ghi", "123", "^_$"],
            separator="-",
        )
        return super().setUp()

    def test_generate_paths(self):
        # Act
        paths = self.three_values_some_of_combinator.generate_paths()

        # Assert

        self.assertIn({"test_combinator_id_1": {"0": "abc", "1": "def"}}, paths)
        self.assertIn({"test_combinator_id_1": {"0": "abc", "2": "ghi"}}, paths)
        self.assertIn({"test_combinator_id_1": {"1": "def", "2": "ghi"}}, paths)
        self.assertIn({"test_combinator_id_1": {"1": "def", "0": "abc"}}, paths)
        self.assertIn({"test_combinator_id_1": {"2": "ghi", "0": "abc"}}, paths)
        self.assertIn({"test_combinator_id_1": {"2": "ghi", "1": "def"}}, paths)

        self.assertIn(
            {"test_combinator_id_1": {"0": "abc", "1": "def", "2": "ghi"}}, paths
        )
        self.assertIn(
            {"test_combinator_id_1": {"0": "abc", "2": "ghi", "1": "def"}}, paths
        )
        self.assertIn(
            {"test_combinator_id_1": {"1": "def", "0": "abc", "2": "ghi"}}, paths
        )
        self.assertIn(
            {"test_combinator_id_1": {"1": "def", "2": "ghi", "0": "abc"}}, paths
        )
        self.assertIn(
            {"test_combinator_id_1": {"2": "ghi", "0": "abc", "1": "def"}}, paths
        )
        self.assertIn(
            {"test_combinator_id_1": {"2": "ghi", "1": "def", "0": "abc"}}, paths
        )

        self.assertEqual(len(paths), 12)

    def test_render_path(self):
        # Arrange
        paths = self.three_values_some_of_combinator.generate_paths()

        # Act
        result_0 = self.three_values_some_of_combinator.render_path(paths[0])
        result_1 = self.three_values_some_of_combinator.render_path(paths[1])
        result_2 = self.three_values_some_of_combinator.render_path(paths[2])

        # Assert
        self.assertEqual(result_0, "abc-def")
        self.assertEqual(result_1, "abc-ghi")
        self.assertEqual(result_2, "def-abc")


if __name__ == "__main__":
    unittest.main()
