from dataclasses import dataclass
from typing import Dict, List
from pcombinator.combinators.combinator import Combinator, IdTree
import json


@dataclass
class PromptCandidatesFile:
    version: str
    seed: int
    combinators: List[Combinator]

    prompts: List[Dict[str, IdTree]]

    def to_pickle(self, path: str) -> None:
        import pickle

        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def from_pickle(path: str) -> "PromptCandidatesFile":
        import pickle

        with open(path, "rb") as f:
            return pickle.load(f)

    def to_json(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self, f)

    @staticmethod
    def from_json(path: str) -> "PromptCandidatesFile":
        with open(path, "r") as f:
            return json.load(f)
