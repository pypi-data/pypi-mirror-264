import json
from dataclasses import dataclass
from typing import Annotated, Dict, List, Union


from pcombinator.combinators.combinator import Path
from pcombinator.combinators.tests.test_jinja2_template import (
    Jinja2TemplateTests,
)
from pcombinator.combinators.named_string import NamedString
from pcombinator.combinators.pick_one import PickOne
from pcombinator.combinators.join_some_of import JoinSomeOf


@dataclass
class PromptCandidatesFile:
    version: str
    seed: int
    root_combinator: Annotated[
        Union[
            NamedString,
            PickOne,
            JoinSomeOf,
            Jinja2TemplateTests,
        ],
        # Field(discriminator="duck_type"),
        None,  # Temporary
    ]

    generated_prompts: List[Dict[str, Path]]

    def to_pickle(self, path: str) -> None:
        """
        Save the object to a pickle file.
        NOTE: pickle files are unsafe to load. Only load pickle files from trusted sources.
        """
        import pickle

        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def from_pickle(path: str) -> "PromptCandidatesFile":
        """
        Load the object from a pickle file.
        NOTE: pickle files are unsafe to load. Only load pickle files from trusted sources.
        """
        import pickle

        with open(path, "rb") as f:
            return pickle.load(f)

    def to_json(self) -> str:
        return json.dumps(
            {
                "version": self.version,
                "seed": self.seed,
                "root_combinator": self.root_combinator.to_json(),
                "generated_prompts": self.generated_prompts,
            }
        )

    def to_json_file(self, path: str) -> None:
        json = self.to_json()
        with open(path, "w") as f:
            f.write(json)

    @staticmethod
    def from_json(path: str) -> "PromptCandidatesFile":
        with open(path, "r") as f:
            json = f.read()
            return "PromptCandidatesFile".parse_raw(json)
