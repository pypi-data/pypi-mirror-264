from dataclasses import dataclass, field
from typing import List


@dataclass
class InputOutput:
    name: str
    datatype: str
    shape: List[int]


@dataclass
class ModelConfig:
    name: str
    versions: List[str]
    platform: str
    inputs: List[InputOutput] = field(default_factory=list)
    outputs: List[InputOutput] = field(default_factory=list)
