from dataclasses import dataclass
from pathlib import Path
from typing import List

from json import JSONDecodeError

from jsonschema import RefResolutionError

BuildExceptions = FileNotFoundError | JSONDecodeError | KeyError | RefResolutionError

@dataclass
class BuildResult:
    file: Path
    ok : bool
    errors: list[BuildExceptions]

@dataclass
class InstanceValidationResult:
    file: Path
    ok : bool
    errors : List[Exception]

@dataclass
class SchemaValidationResult:
    core_schema_path: Path
    build_ok: bool
    build_results: list[BuildResult]
    validation_results: list[InstanceValidationResult]