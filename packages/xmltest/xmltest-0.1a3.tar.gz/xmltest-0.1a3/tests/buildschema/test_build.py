from pathlib import Path
from xmlschema import XMLSchemaParseError, XMLSchemaModelError
from xml.etree.ElementTree import ParseError

from xmltest.validator import build_schema


def test_simple():
    schema, results = build_schema(Path("./tests/buildschema/data/good.xsd"))
    assert schema
    assert len(results) == 1
    assert results[0].ok == True


def test_simple_bad():
    schema, results = build_schema("./tests/buildschema/data/bad_namespace_error.xsd")
    assert schema is None
    assert len(results) == 1
    assert results[0].ok == False
    assert isinstance(results[0].errors[0], XMLSchemaParseError)
    assert "is not an element of the schema" in results[0].errors[0].message


def test_upa_bad():
    schema, results = build_schema("./tests/buildschema/data/bad_upa.xsd")
    assert schema is None
    assert len(results) == 1
    assert results[0].ok == False
    assert isinstance(results[0].errors[0], XMLSchemaModelError)
    assert "Unique Particle" in results[0].errors[0].message


def test_mixed():
    schema, results = build_schema(
        "./tests/buildschema/data/good.xsd",
        ["./tests/buildschema/data/bad_syntax.xsd"],
    )
    assert schema
    assert len(results) == 2
    assert results[0].ok == False
    assert isinstance(results[0].errors[0], ParseError)
    assert "mismatched tag" in results[0].errors[0].msg
    assert results[1].ok == True
    assert len(results[1].errors) == 0

def test_no_root():
   schema, results = build_schema(
       "./tests/buildschema/data/no_root_element.xsd"
   )
   assert schema
   print(results)