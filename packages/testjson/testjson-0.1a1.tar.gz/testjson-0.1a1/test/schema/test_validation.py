import pytest
from pathlib import Path
from json import JSONDecodeError, dumps

from jsonschema import ValidationError

from testjson import validate_string, validate_json, validate_path, build_schema

def test_not_a_dict():
    schema, _ = build_schema("./test/schema/data/simple.schema.json", [])
    assert schema is not None
    result = validate_json(schema, "{}")
    assert result.ok == False
    assert len(result.errors) == 1
    assert type(result.errors[0]) == ValidationError

def test_empty_dict():
    schema, _ = build_schema("./test/schema/data/simple.schema.json", [])
    assert schema is not None
    result = validate_json(schema, {})
    assert result.ok == True
    assert len(result.errors) == 0
    schema, _ = build_schema("./test/schema/data/simple_required.schema.json", [])
    assert schema is not None
    result = validate_json(schema, {})
    assert result.ok == False
    assert len(result.errors) == 1
    assert type(result.errors[0]) == ValidationError
    assert "'firstName' is a required property" in str(result.errors[0])

def test_simple():
    schema, _ = build_schema("./test/schema/data/simple.schema.json", [])
    assert schema is not None
    result = validate_json(schema, {"firstName" : "foo", "lastName" : "bar"})
    assert result.ok == True
    assert len(result.errors) == 0
    result = validate_json(schema, {"firstName" : "foo", "lastName" : "bar", "age" : -4})
    assert result.ok == False
    assert len(result.errors) == 1
    assert "Failed validating 'minimum'" in str(result.errors[0])

def test_extra_fields_ok():
    schema, _ = build_schema("./test/schema/data/simple.schema.json", [])
    assert schema is not None
    result = validate_json(schema, { 'unrelated_field' : 'foo' })
    assert result.ok == True
    assert len(result.errors) == 0

def test_empty_string():
    schema, _ = build_schema("./test/schema/data/simple.schema.json", [])
    assert schema is not None
    result = validate_string(schema, "")
    assert result.ok == False
    assert len(result.errors) == 1
    assert type(result.errors[0]) == JSONDecodeError

def test_string():
    schema, _ = build_schema("./test/schema/data/simple.schema.json", [])
    j = {"firstName" : "foo", "lastName" : "bar", "age" : -4}
    s = dumps(j)
    result = validate_string(schema, s)
    assert result.ok == False
    assert len(result.errors) == 1
    assert "Failed validating 'minimum'" in str(result.errors[0])

def test_bad_path():
    schema, _ = build_schema("./test/schema/data/simple.schema.json", [])
    assert schema is not None
    result = validate_path(schema, "not_a_file")
    assert result.ok == False
    assert len(result.errors) == 1
    assert type(result.errors[0]) == FileNotFoundError

def test_path():
    schema, _ = build_schema("./test/schema/data/simple.schema.json", [])
    assert schema is not None
    result = validate_path(schema, "./test/schema/data/bad_simple.json")
    assert result.ok == False
    assert len(result.errors) == 1
    assert "Failed validating 'minimum'" in str(result.errors[0])