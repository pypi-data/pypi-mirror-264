import unittest

import jinja2
from pcombinator.combinators.random_join_combinator import RandomJoinCombinator
from pcombinator.combinators.template_combinator import TemplateCombinator


class TemplateCombinatorTests(unittest.TestCase):
    def test_render(self):
        # Create a TemplateCombinator instance
        template = jinja2.Template("{{role}}\n{{task}}\n{{question}}\n")

        template_combinator = TemplateCombinator(
            template=template,
            children={
                "role": "value_1",
                "task": "value_2",
                "question": RandomJoinCombinator(
                    n_max=1,
                    n_min=1,
                    children=["option_1"],
                    separator="\n",
                    id="question_randomizer_1",
                ),
            },
            id="template_1",
        )

        # Render
        result, id_tree = template_combinator.render()

        # Check the result
        self.assertEqual(
            result,
            "value_1\nvalue_2\noption_1",
        )

        # Check the id_tree
        self.assertEqual(
            id_tree,
            {
                "template_1": {
                    "role": {},
                    "task": {},
                    "question": {"question_randomizer_1": {}},
                }
            },
        )


if __name__ == "__main__":
    unittest.main()
