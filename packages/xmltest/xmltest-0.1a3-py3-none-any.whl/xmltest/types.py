from dataclasses import dataclass
from pathlib import Path
from xmlschema import XMLSchemaValidatorError
from xml.etree.ElementTree import ParseError

BuildExceptions = XMLSchemaValidatorError | ParseError
ValidationExceptions = XMLSchemaValidatorError | ParseError


@dataclass
class BuildResult:
    file: Path
    ok: bool
    errors: list[BuildExceptions]


@dataclass
class InstanceValidationResult:
    file: Path
    ok: bool
    errors: list[ValidationExceptions]


@dataclass
class SchemaValidationResult:
    core_schema_path: Path
    build_ok: bool
    build_results: list[BuildResult]
    validation_results: list[InstanceValidationResult]
