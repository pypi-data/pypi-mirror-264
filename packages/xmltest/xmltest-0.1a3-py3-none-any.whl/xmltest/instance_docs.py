import logging
from typing import Generator, Sequence
from pathlib import Path
from collections.abc import Mapping

from xmlschema import XMLSchema
from xml.etree.ElementTree import ParseError

from .validator import build_schema
from .types import InstanceValidationResult, SchemaValidationResult


def _test_instance_doc(
    schema: XMLSchema, instance_doc_path: Path
) -> InstanceValidationResult:
    try:
        path_str = str(instance_doc_path)
        errors = list(schema.iter_errors(path_str))
        if len(errors) > 0:
            logging.info(f"{path_str} failed validation with {len(errors)} errors")
        else:
            logging.info(f"{path_str} passed validation")
        return InstanceValidationResult(Path(path_str), len(errors) == 0, errors)
    except ParseError as ex:
        return InstanceValidationResult(Path(path_str), False, [ex])


def test_instance_docs(
    schema: XMLSchema, instance_docs: Sequence[str | Path]
) -> Generator[InstanceValidationResult, None, None]:
    """Helper function for using an XMLSchema to validate a sequence of XML instance
    documents against that schema.

    Uses the XMLSchema.iter_error function to ensure that (where possible)
    multiple errors can be returned for each instance document.

    :param schema: XSD schema to use for validation
    :type schema: XMLSchema
    :param instance_docs: Sequence of paths (Path or str) to instance documents to validate against the schema
    :type instance_docs: Sequence[str  |  Path]
    :yield: Yields an InstanceValidationResults for each instance doc passed
    :rtype: Generator[InstanceValidationResult, None, None]
    """
    for instance_doc in instance_docs:
        instance_doc_path = Path(instance_doc)
        if instance_doc_path.is_dir():
            for globbed_path in instance_doc_path.glob("*.xml"):
                yield _test_instance_doc(schema, globbed_path)
        else:
            yield _test_instance_doc(schema, instance_doc_path)


def validate(json_config: Sequence[dict] | dict | str | Path) -> Generator[SchemaValidationResult, None, None]:
    """
    Helper function for calling test_instance_docs using a JSON config object.
    The config object contains either a single instance of, or a list of, dicts
    that describe the schema and instance documents. This can be loaded from
    a file, providing a

    Each dict must have:
     - a 'coreSchema' element giving a path to the cor
     - a 'supportSchemas' element giving a list of paths to supporting schemas (or an empty list)
     - a 'exampleFiles' element giving a list of paths to instance documents to check (or an empty list)

    :param: json_config - input dict or list of dicts, or a string / pathlib Path pointing to a file containing the same
    :param: instance_doc - sequence of paths (str or pathlib Path) to instance documents
    :returns: Generator of tuples (path to instance doc, list of errors)
    """

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
            validation_results = test_instance_docs(schema, instance_docs)
            yield SchemaValidationResult(
                Path(core_schema), True, build_results, list(validation_results)
            )
        else:
            yield SchemaValidationResult(Path(core_schema), False, build_results, [])
