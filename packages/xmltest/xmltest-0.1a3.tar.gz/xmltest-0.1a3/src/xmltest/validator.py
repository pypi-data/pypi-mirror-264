import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Tuple

from xmlschema import XMLSchema, XMLSchemaValidatorError
from xml.etree.ElementTree import ParseError

from .types import BuildResult


def _build_schema_location_dict(
    schema_paths: Sequence[Path | str],
) -> Tuple[list, list[BuildResult]]:
    """
    Takes a sequence of file paths and builds a schema location list
    of tuples containing the schema's default namespace and the file location.
    This is the format used by the XMLSchema constructor.

    Build results are also provided using the BuildResult class, which indicates any
    validation errors encountered when attempting to parse each file.

    :param: schema_paths: List of filenames (str or pathlib Path) to scan.
    :returns: A tuple of (schema location list, build results)
    """
    logging.info("Schema locations:")
    schema_locations = []
    build_results = []
    for schema_path in schema_paths:
        try:
            xs = XMLSchema(schema_path, validation="skip")
            schema_locations.append(
                (xs.target_namespace, str(Path(schema_path).resolve()))
            )
            logging.info(" [ {0}  ->  {1} ]".format(xs.target_namespace, schema_path))
            # For some reason we get spurious UPA errors in the supporting schemas
            # so these are filtered out. A real UPA error will be caught when the
            # schema set if built with "strict" later on.
            build_errors = [
                error
                for error in xs.all_errors
                if not error.message.startswith("Unique Particle Attribution violation")
            ]
            if len(build_errors) > 0:
                build_results.append(
                    BuildResult(Path(schema_path), False, build_errors)
                )
            else:
                build_results.append(BuildResult(Path(schema_path), True, []))
        except ParseError as ex:
            logging.warning(" [ {0} failed to parse:  {1} ]".format(schema_path, ex))
            build_results.append(BuildResult(Path(schema_path), False, [ex]))
        except XMLSchemaValidatorError as ex:
            logging.warning(" [ {0} failed to validate:  {1} ]".format(schema_path, ex))
            build_results.append(BuildResult(Path(schema_path), False, [ex]))
    return (schema_locations, build_results)


def build_schema(
    core_schema_path: Path | str, supporting_schema_paths: Sequence[Path | str] = None
) -> Tuple[XMLSchema | None, list[BuildResult]]:
    """
    Attempts to build an XMLSchema instance given a core schema file and a set
    of supporting schemas that satisfy any <import> statements. The XMLSchema instance
    returned can then be used to validate instance documents.

    Build results are also provided using the BuildResult class, which indicates any
    validation errors encountered when attempting to parse each file and when attempting
    to build the schema. Build errors are generally reported against the core schema file.

    :param: core_schema_path - Path to the core schema, either as a str or pathlib Path
    :param: supporting_schema_paths - Sequence of paths to any supporting schemas
    :returns: A tuple of (XMLSchema or None if build failed, build results)
    """
    schema_locations = []
    core_schema = None
    build_results = []
    core_schema_path = Path(core_schema_path)
    if supporting_schema_paths:
        schema_locations, build_results = _build_schema_location_dict(
            supporting_schema_paths
        )
    try:
        core_schema = XMLSchema(
            str(core_schema_path), locations=schema_locations, validation="strict"
        )
        if len(core_schema.all_errors) > 0:
            build_results.append(
                BuildResult(core_schema_path, False, core_schema.all_errors)
            )
        else:
            build_results.append(BuildResult(core_schema_path, True, []))
    except XMLSchemaValidatorError as ex:
        logging.warning(
            " [ {0} failed to build:  {1} ]".format(core_schema_path, ex.message)
        )
        build_results.append(BuildResult(Path(core_schema_path), False, [ex]))
    return (core_schema, build_results)
