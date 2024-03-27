import unittest
from pcombinator.combinators.fixed_string_combinator import FixedStringCombinator


class FixedStringCombinatorTest(unittest.TestCase):
    def test_render(self):
        string = "Hello, World!"
        combinator = FixedStringCombinator(string, "id1")
        expected_output = (string, {'id1': {}})
        self.assertEqual(combinator.render(), expected_output)


if __name__ == "__main__":
    unittest.main()
