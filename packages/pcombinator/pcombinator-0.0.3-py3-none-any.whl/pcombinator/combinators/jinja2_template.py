import itertools
from typing import Dict, List
from jinja2 import Template

from pcombinator.combinators.combinator import (
    Combinator,
    Path,
    combinator_dict_to_obj,
    derived_classes,
)
from pcombinator.combinators.combinator_or_leaf_type import CombinatorOrLeaf
from pcombinator.util.classname import get_fully_qualified_class_name


class Jinja2Template(Combinator):
    """
    A combinator that renders a template with its rendered children as arguments.
    """

    _template: Template
    template_source: str
    children: Dict[str, CombinatorOrLeaf]

    def __init__(
        self,
        id: str,
        template_source: str,
        children: Dict[str, CombinatorOrLeaf],
        **kwargs,
    ):
        super().__init__(
            id=id,
            combinator_type=kwargs.get("combinator_type")
            or get_fully_qualified_class_name(self.__class__),
        )

        # Verify that children is a dict with at least one element
        if not isinstance(children, dict) or len(children) == 0:
            raise ValueError("children must be a dict with at least one element")

        # Verify that template source is a non empty string
        if not isinstance(template_source, str) or len(template_source) == 0:
            raise ValueError("template_source must be a non empty string")

        self._template = Template(source=template_source)
        self.template_source = template_source
        self.children = children

    def generate_paths(self) -> List[Path]:
        """
        Generate all paths in the tree under this combinator id. Each path is a dict with the id of the combinator as the only key.
        """
        # Generate the paths for each child
        children_paths = {
            key: (
                child
                if isinstance(child, str)
                else child.generate_paths() if child is not None else None
            )
            for key, child in self.children.items()
        }

        # Generate the cartesian product of all children paths
        res = []
        for combination in itertools.product(*children_paths.values()):
            res.append({self.id: dict(zip(children_paths.keys(), combination))})

        return res

    def render_path(self, path: Path) -> str:
        """
        Render the template, passing the specific rendered children in `path` as arguments.

        Returns:
            rendered: The rendered template
        """
        # Verify that the path dict contains the key of this combinator
        if len(path) != 1 or self.id not in path:
            raise ValueError(
                f"Path must contain the id of this combinator at the top level: {self.id}"
            )

        rendered_children_dict = {}
        for key in self.children.keys():
            path_for_child = path[self.id][key]
            child = self.children[key]
            rendered = (
                child
                if isinstance(child, str)
                else child.render_path(path_for_child) if child is not None else None
            )
            rendered_children_dict[key] = rendered

        res = self._template.render(rendered_children_dict)
        return res

    def add_child(self, key: str, child: CombinatorOrLeaf) -> None:
        self.children[key] = child

    def get_children(self) -> Dict[str, CombinatorOrLeaf]:
        return self.children

    def remove_child_by_key(self, key: str) -> None:
        del self.children[key]

    def remove_child_by_id(self, id: str) -> None:
        for key, child in self.children.items():
            if child.get_id() == id:
                del self.children[key]
                return

    @classmethod
    def from_json(cls, values: dict):

        return cls(
            id=values["id"],
            template_source=values["template_source"],
            children={
                key: Combinator.from_json(child) if child.startswith("{") else child
                for key, child in values["children"].items()
            },
        )


Combinator.register_derived_class(Jinja2Template)
