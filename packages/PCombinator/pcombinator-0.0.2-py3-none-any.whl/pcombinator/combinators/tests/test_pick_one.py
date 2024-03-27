import unittest

from pcombinator.combinators import PickOne


class PickOneTests(unittest.TestCase):
    def test_initialization(self):
        one_of_combinator = PickOne(
            id="id_1",
            children=["abc", "def"],
        )
        self.assertEqual(
            one_of_combinator.combinator_type,
            "pcombinator.combinators.pick_one.type",
        )
        self.assertEqual(one_of_combinator.n_min, 1)
        self.assertEqual(one_of_combinator.n_max, 1)
        self.assertEqual(one_of_combinator.children, ["abc", "def"])
        self.assertEqual(one_of_combinator.id, "id_1")

    def test_default_values(self):
        one_of_combinator = PickOne(id="id_1", children=["a", "b"])
        self.assertEqual(
            one_of_combinator.combinator_type,
            "pcombinator.combinators.pick_one.type",
        )
        self.assertEqual(one_of_combinator.n_min, 1)
        self.assertEqual(one_of_combinator.n_max, 1)
        self.assertEqual(one_of_combinator.children, ["a", "b"])
        self.assertEqual(one_of_combinator.id, "id_1")

    def test_generate_paths(self):
        # Arrange
        one_of_combinator = PickOne(id="id_1", children=["a", "b"])

        # Act
        paths = one_of_combinator.generate_paths()

        # Assert
        self.assertIn({"id_1": {"0": "a"}}, paths)
        self.assertIn({"id_1": {"1": "b"}}, paths)
        self.assertEqual(len(paths), 2)

    def test_render_path(self):
        # Arrange
        one_of_combinator = PickOne(id="id_1", children=["a", "b"])
        paths = one_of_combinator.generate_paths()

        # Act
        result_a = one_of_combinator.render_path(paths[0])
        result_b = one_of_combinator.render_path(paths[1])

        # Assert
        self.assertEqual(result_a, "a")
        self.assertEqual(result_b, "b")


if __name__ == "__main__":
    unittest.main()
