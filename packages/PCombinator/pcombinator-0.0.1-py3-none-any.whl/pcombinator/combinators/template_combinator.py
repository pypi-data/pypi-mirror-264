from typing import Dict
from jinja2 import Template

from pcombinator.combinators.combinator import Combinator, IdTree, render_children


class TemplateCombinator(Combinator):
    """
    A combinator that renders a template with its rendered children as arguments.
    """

    children: Dict[str, "Combinator"]

    def __init__(self, template: Template, children: Dict[str, "Combinator"], id=None):
        super().__init__(id)
        self._combinator_type = "template"
        self.template = template
        self.children = children

    def render(self) -> (str, IdTree):
        """
        Render the template, passing the rendered children as arguments.

        Returns:
            rendered: The rendered template
            rendered_id_tree: An IdTree of rendered children under this combinator id.
        """
        rendered_children_dict = {}
        res_id_tree = {self.id: {}}
        for key in self.children.keys():
            rendered, id_tree = render_children([self.children[key]])
            res_id_tree[self.id][key] = id_tree
            rendered_children_dict[key] = rendered[0]

        res = self.template.render(rendered_children_dict)
        return res, res_id_tree

    def add_child(self, key: str, child: "Combinator") -> None:
        self.children[key] = child

    def get_children(self) -> Dict[str, "Combinator"]:
        return self.children

    def remove_child_by_key(self, key: str) -> None:
        del self.children[key]

    def remove_child_by_id(self, id: str) -> None:
        for key, child in self.children.items():
            if child.get_id() == id:
                del self.children[key]
                return
