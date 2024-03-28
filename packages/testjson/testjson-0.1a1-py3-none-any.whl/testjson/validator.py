import logging
from pathlib import Path
from typing import Sequence, Tuple, Generator, List, Mapping
from json import load, loads, JSONDecodeError

from jsonschema import RefResolver, Draft202012Validator, Validator, RefResolutionError

from .types import BuildResult, SchemaValidationResult, InstanceValidationResult

def recursively_find_refs(j) -> Generator[Tuple[str, str], None, None]:
    for k,v in j.items():
        if k == "$ref":
            yield k,v
        if isinstance(v, dict):
            yield from recursively_find_refs(v)

def check_refs(schema: Validator, resolver: RefResolver) -> List[RefResolutionError]:
    refs = list(recursively_find_refs(schema.schema))
    errors = []
    for key, ref in refs:
        try:
            if ref.startswith("#"):
                continue
            resolved_ref = resolver.resolve(ref)
        except RefResolutionError as ex:
            errors.append(ex)
    return errors
        
def build_schema(core_schema_path: str | Path, supporting_schema_paths: Sequence[Path | str] = None) -> Tuple[Draft202012Validator | None, list[BuildResult]]:
    core_schema_path = Path(core_schema_path)
    if not core_schema_path.exists():
        logging.warning(f"Cannot find core schema file {core_schema_path} for schema files")
        return None, [BuildResult(core_schema_path, False, [FileNotFoundError(f"Cannot find file {core_schema_path}")])]
    build_results = []
    try:        
        _core_schema = load(core_schema_path.open())
        _schema_dict = { _core_schema['$id'] : _core_schema }
    except (JSONDecodeError, KeyError) as ex:
        logging.warning(f"Could not parse {core_schema_path} ({ex!r})")
        return None, [BuildResult(core_schema_path, False, [ex])]
    logging.info(f"Loaded {core_schema_path}")
    _supporting_paths = []
    for thing in supporting_schema_paths:
        path = Path(thing)
        if path.is_dir():
            logging.debug(f"Searching {path} for schema files")
            _supporting_paths.extend(path.rglob("*.schema.json"))
        else:
            logging.debug(f"Appending {path} as schema file")
            _supporting_paths.append(path)
    logging.info(f"Supporting schema paths: {_supporting_paths}")
    _supporting_schemas = []
    _schema_dict = {}
    for path in _supporting_paths:
        try:
            new_schema = load(path.open())
            _supporting_schemas.append(new_schema)
            new_id = new_schema['$id']
            _schema_dict[new_id] = new_schema
            build_results.append(BuildResult(path, True, []))            
        except (FileNotFoundError, JSONDecodeError, KeyError) as ex:
            if ex is FileNotFoundError:
                logging.warning(f"Could not find supporting file {path}")
            else:
                logging.warning(f"Could not parse file {path} ({ex!r})")
            build_results.append(BuildResult(path, False, [ex]))
    # _schema_dict = _schema_dict | { s['$id'] : s for s in _supporting_schemas }
    logging.info(f"Loaded schema IDs: {[k for k in _schema_dict.keys()]}")    
    _resolver = RefResolver(None, 
                    referrer=None, 
                    store=_schema_dict)
    logging.info("Created RefResolver")
    _validator = Draft202012Validator(_core_schema, resolver=_resolver)
    logging.info("Created validator")
    ref_errors = check_refs(_validator, _resolver)
    if len(ref_errors) > 0:
        build_results.append(BuildResult(core_schema_path, False, ref_errors))
        return None, build_results
    else:
        build_results.append(BuildResult(core_schema_path, True, []))
        return _validator, build_results


def validate_json(schema: Validator, instance_json: dict, path = Path | None) -> InstanceValidationResult:
    errors = list(schema.iter_errors(instance_json))
    return InstanceValidationResult(
        path,
        len(errors) == 0,
        errors=errors
    )

def validate_string(schema: Validator, string: str, path = Path | None) -> InstanceValidationResult:
    try:
        json = loads(string)
        return validate_json(schema, json, path)
    except JSONDecodeError as ex:
        return InstanceValidationResult(path, False, [ex])

def validate_path(schema: Validator, path: Path | str) -> InstanceValidationResult:
    try:
        path = Path(path)
        string = path.open().read()
        return validate_string(schema, string, path)
    except FileNotFoundError as ex:
        return InstanceValidationResult(path, False, [ex])

def validate_from_config(json_config: Sequence[dict] | dict | str | Path) -> Generator[SchemaValidationResult, None, None]:
    if isinstance(json_config, Mapping):
        targets = [json_config]
    else:
        targets = json_config

    for target in targets:
        core_schema = target["coreSchema"]
        supporting_schemas = target["supportingSchemas"]
        instance_docs = target["exampleFiles"]
        schema, build_results = build_schema(core_schema, supporting_schemas)
        if schema is not None:
            validation_results = [validate_path(schema, instance_doc) for instance_doc in instance_docs]
            yield SchemaValidationResult(
                Path(core_schema), True, build_results, list(validation_results)
            )
        else:
            yield SchemaValidationResult(Path(core_schema), False, build_results, [])

# class JsonValidator:
#     def __init__(self, core_schema: str | Path, other_schemas : dict):
#         core_schema = Path(core_schema)
#         if not core_schema.exists():
#             self.build_errors.append(FileExistsError(f"Could not find core schema {core_schema}"))
#             return
#         self._core_schema = json.load(core_schema.open())
#         self._schema_dict = { self._core_schema['$id'] : self._core_schema }
#         self._supporting_paths = []
#         for thing in other_schemas:
#             path = Path(thing)
#             if path.is_dir():
#                 logging.debug(f"Searching {path} for schema files")
#                 self._supporting_paths.extend(path.rglob("*.schema.json"))
#             else:
#                 logging.debug(f"Appending {path} as schema file")
#                 self._supporting_paths.append(path)
#         logging.info(f"Supporting schema paths: {self._supporting_paths}")
#         self._supporting_schemas = [json.load(p.open()) for p in self._supporting_paths]
#         self._schema_dict = self._schema_dict | { s['$id'] : s for s in self._supporting_schemas }
#         logging.info(f"Loaded schema IDs: {[k for k in self._schema_dict.keys()]}")
#         self._resolver = RefResolver(None, 
#                         referrer=None, 
#                         store=self._schema_dict)
#         logging.info("Created RefResolver")
#         self._validator = Draft202012Validator(self._core_schema, resolver=self._resolver)
#         logging.info("Created validator")
    
#     def is_ok(self) -> bool:
#         return self._validator is not None
    
#     def validate(self, instance_doc: str):
#         yield self._validator.iter_errors(instance_doc)