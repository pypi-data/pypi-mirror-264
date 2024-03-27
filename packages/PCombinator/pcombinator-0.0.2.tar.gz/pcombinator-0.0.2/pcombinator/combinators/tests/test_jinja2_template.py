import unittest

from pcombinator.combinators import Jinja2Template, JoinSomeOf, NamedString, PickOne


class Jinja2TemplateTests(unittest.TestCase):

    def setUp(self) -> None:
        self.single_path_template_combinator = (
            self._generate_single_path_template_combinator()
        )
        self.multi_path_template_combinator = (
            self._generate_multi_path_template_combinator()
        )

        return super().setUp()

    def test_generate_paths(self):
        # Act
        paths = self.single_path_template_combinator.generate_paths()

        # Assert
        self.assertIn(
            {
                "template_1": {
                    "role": "v",
                    "task": "v",
                    "question": {"question_randomizer_1": {"0": "option_1"}},
                }
            },
            paths,
        )
        self.assertEqual(len(paths), 225)

    def test_render_path(self):
        # Act
        paths = self.single_path_template_combinator.generate_paths()
        result = self.single_path_template_combinator.render_path(paths[0])

        # Assert
        self.assertEqual(result, "value_1_of_role\nvalue_1_of_task\noption_1")

    def _generate_single_path_template_combinator(self):
        # Create a TemplateCombinator instance
        template_source = "{{role}}\n{{task}}\n{{question}}\n"

        template_combinator = Jinja2Template(
            id="template_1",
            template_source=template_source,
            children={
                "role": "value_1_of_role",
                "task": "value_1_of_task",
                "question": JoinSomeOf(
                    id="question_randomizer_1",
                    n_max=1,
                    n_min=1,
                    children=["option_1"],
                    separator="\n",
                ),
            },
        )

        return template_combinator

    def _generate_multi_path_template_combinator(self):
        template_source = "{{role}}\n{{task}}\n{{question}}\n"

        template_combinator = Jinja2Template(
            id="template_1",
            template_source=template_source,
            children={
                "role": PickOne(
                    "value_1_of_role",
                    [NamedString("key_of_val_2_role", "value_2_of_role")],
                ),
                "task": "value_1_of_task",
                "question": JoinSomeOf(
                    id="question_randomizer_1",
                    n_max=3,
                    n_min=0,
                    children=[
                        "option_1",
                        "option_2",
                        "option_3",
                        "option_4",
                        "option_5",
                        "option_6",
                    ],
                    separator="\n",
                ),
            },
        )

        return template_combinator


if __name__ == "__main__":
    unittest.main()
