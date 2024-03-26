from pathlib import Path
from xmlschema import XMLSchemaParseError
from copy import deepcopy

from xmltest import test_instance_docs as do_test, build_schema, validate


def test_simple():
    files = list(Path("./tests/instance/data/set1/").glob("*.xml"))
    schema, _ = build_schema("./tests/instance/data/set1/good.xsd")
    assert schema
    results = list(do_test(schema, files))
    assert len(files) == len(results)
    for result in results:
        if result.file.name.startswith("bad"):
            assert result.ok == False
            assert len(result.errors) > 0
        else:
            assert result.ok == True
            assert len(result.errors) == 0


json_config = {
    "coreSchema": "./tests/instance/data/set2/good_with_import.xsd",
    "supportingSchemas": ["./tests/instance/data/set2/good_imported.xsd"],
    "exampleFiles": ["./tests/instance/data/set2/good.xml"],
}


def test_json_broken_schema():
    j = deepcopy(json_config)
    j["supportingSchemas"] = []
    results = list(validate(j))
    assert len(results) == 1
    result = results[0]
    assert result.build_ok == False
    assert len(result.build_results) == 1
    assert result.build_results[0].ok == False
    assert isinstance(result.build_results[0].errors[0], XMLSchemaParseError)
    assert "unknown type" in result.build_results[0].errors[0].msg
    assert len(result.validation_results) == 0


def test_json_ok():
    results = list(validate(json_config))
    assert len(results) == 1
    result = results[0]
    assert result.build_ok == True
    assert len(result.build_results) == 2
    assert result.build_results[0].ok == True
    assert result.build_results[1].ok == True
    validation_results = list(result.validation_results)
    assert len(validation_results) == 1
    assert validation_results[0].ok == True
    assert len(validation_results[0].errors) == 0


def test_json_list_ok():
    results = list(validate([json_config, json_config]))
    assert len(results) == 2
    result = results[0]
    assert result.build_ok == True
    assert len(result.build_results) == 2
    assert result.build_results[0].ok == True
    assert result.build_results[1].ok == True
    validation_results = list(result.validation_results)
    assert len(validation_results) == 1
    assert validation_results[0].ok == True


def test_json_glob_xml():
    j = deepcopy(json_config)
    j["exampleFiles"] = ["./tests/instance/data/set2/"]
    results = list(validate(j))
    assert len(results) == 1
    result = results[0]
    assert result.build_ok == True
    assert len(result.build_results) == 2
    validation_results = list(result.validation_results)
    for r in validation_results:
        if r.file.name.startswith("bad"):
            assert r.ok == False
            assert len(r.errors) > 0
        else:
            assert r.ok == True
            assert len(r.errors) == 0

def test_json_noroot():
    j = {
        'coreSchema' : './tests/instance/data/set1/no_root_element.xsd',
        'supportingSchemas' : [],
        'exampleFiles' : []
    }
    results = list(validate(j))
    assert len(results) == 1
    result = results[0]
    assert result.build_ok == True