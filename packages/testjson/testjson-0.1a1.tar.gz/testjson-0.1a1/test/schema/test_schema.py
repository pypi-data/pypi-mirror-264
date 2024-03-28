import pytest
from pathlib import Path
from json import JSONDecodeError

from jsonschema import RefResolutionError

from testjson import build_schema

def test_empty():
    schema, results = build_schema('not_a_file', [])
    assert schema is None
    assert len(results) == 1
    result = results[0]
    assert result.ok == False
    assert len(result.errors) == 1
    assert isinstance(result.errors[0], FileNotFoundError)

def test_invalid_json():
    schema, results = build_schema('./test/schema/data/invalid_json.schema.json', [])
    assert schema is None
    assert len(results) == 1
    result = results[0]
    assert result.ok == False
    assert len(result.errors) == 1

def test_missing_id():
    schema, results = build_schema('./test/schema/data/invalid_no_id.schema.json', [])
    assert schema is None
    assert len(results) == 1
    result = results[0]
    assert result.ok == False
    assert len(result.errors) == 1
    schema, results = build_schema('./test/schema/data/simple.schema.json', ['./test/schema/data/invalid_no_id.schema.json'])
    assert schema is not None
    assert len(results) == 2
    result = results[0]
    assert result.ok == False
    assert len(result.errors) == 1
    assert type (result.errors[0]) == KeyError

def test_missing_dep():
    schema, results = build_schema('./test/schema/data/simple.schema.json', ["not_a_file"])
    assert schema is not None
    assert len(results) == 2
    assert results[1].file == Path('./test/schema/data/simple.schema.json')
    assert results[1].ok == True
    assert results[0].ok == False
    assert len(results[0].errors) == 1
    assert isinstance(results[0].errors[0], FileNotFoundError)

def test_importing():
    schema, results = build_schema('./test/schema/data/imports.schema.json', 
                                   ["./test/schema/data/imported.schema.json"])
    assert schema is not None
    assert len(results) == 2
    assert all([x.ok for x in results])
    assert all([len(x.errors) == 0 for x in results])

def test_invalid_import():
    schema, results = build_schema('./test/schema/data/imports.schema.json', 
                                   ["./test/schema/data/invalid_json.schema.json"])
    assert len(results) == 2
    assert results[1].ok == False
    assert results[0].ok == False
    assert len(results[0].errors) == 1
    assert isinstance(results[0].errors[0], JSONDecodeError)
    assert len(results[1].errors) == 1
    assert isinstance(results[1].errors[0], RefResolutionError)
    assert schema is None

def test_wrong_import():
    schema, results = build_schema('./test/schema/data/imports_wrong.schema.json', 
                                   ["./test/schema/data/imported.schema.json"])
    assert schema is None
    assert results[0].ok == True
    assert len(results[0].errors) == 0
    assert results[1].ok == False
    assert len(results[1].errors) == 1
    assert isinstance(results[1].errors[0], RefResolutionError)

    