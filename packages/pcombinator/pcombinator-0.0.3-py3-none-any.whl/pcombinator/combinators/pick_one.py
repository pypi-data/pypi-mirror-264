from typing import List

from pcombinator.combinators.combinator import Combinator, derived_classes
from pcombinator.combinators.combinator_or_leaf_type import CombinatorOrLeaf
from pcombinator.combinators.join_some_of import JoinSomeOf
from pcombinator.util.classname import get_fully_qualified_class_name


class PickOne(JoinSomeOf):
    """
    A combinator which renders exactly one of its children. Based on JoinSomeOf combinator.
    """

    children: List[CombinatorOrLeaf]

    def __init__(
        self,
        id: str,
        children: List[CombinatorOrLeaf] = [],
        **kwargs,
    ):
        super().__init__(
            id=id,
            n_min=1,
            n_max=1,
            separator="",
            children=children,
            combinator_type=kwargs.get("combinator_type")
            or get_fully_qualified_class_name(self.__class__),
        )

    @classmethod
    def from_json(cls, values: dict):
        return cls(
            id=values["id"],
            children=[Combinator.from_dict(child) for child in values["children"]],
        )


Combinator.register_derived_class(PickOne)
