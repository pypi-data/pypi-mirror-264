Getting started
===============

Description
------------
xmltest is a small package to help with testing XSD schema sets. Under the hood it uses the `xmlschema
library <https://pypi.org/project/xmlschema/>`_, and provides a simple interface for common tasks, namely:

- Building an XMLSchema instance from a set of XSD documents and returning any errors
- Testing instance XML documents against the schema set and returning any errors
- Provides a command-line tool for testing multiple schema sets and instance docs

Installation
------------
xmltest can be installed via pip.::

    pip install xmltest

It requires Python 3.7 or later.

Basic usage
-----------

Use the `build_schema()` function to build an XMLSchema instance from a bunch of schema files. This takes
care of building the schema location dictionary and applying different validation rules so that imported schema
files can be syntax checked before attempting to build.

.. code-block:: Python

    from xmltest import build_schema

    schema, build_results = build_schema("path_to_core_schema.xsd", ["path_to_imported_schema.xsd"])

The `build_results` returned provide a BuildResult structure for each file passed in, 
as well as an indication of whether the build succeeded or not. If it did not, `schema` will be `None`

The returned XMLSchema instance can then be used as per the XMLSchema library docs.
However, for the common case of wanting to both build a schema set and then test a bunch of instance files,
the `test_instance_docs` helper function is provided.

.. code-block:: Python

    from xmltest import build_schema, test_instance_docs

    schema, build_results = build_schema("path_to_core_schema.xsd", ["path_to_imported_schema.xsd"])
    if build_results.built_ok:
        for result in test_instance_docs(schema, ["path_to_instance_doc.xml"]):
            print (f"{result.file} OK = {result.ok}")

There is yet another helper function called `validate` that combines both `build_schema` and `test_instance_docs`
into one function call. Instead of named parameters, it accepts a dict (or a list of dicts)
which are expected to contain paths to the core schema, supporting schemas and instance docs.

.. code-block:: Python

    from xmltest import validate

    config = {
        "coreSchema" : "path_to_core_schema.xsd",
        "supportingSchemas" : ["path_to_supporting_schema.xsd"], # can be empty list if not needed
        "instanceDocs" : ["path_to_instance_doc.xml"]            # can be empty list if not needed
    }

    results = validate(config)
    # Returns a generator for each config passed in. Here, only a single
    # object is passed in, so only a single result will be returned
    for result in results:
        print(f"Core schema: {result.core_schema_path})
        print(f"Schema built OK? {result.built_ok}")
        for validation_result in validation_results:
            print(f"Instance doc: {validation_result.file} OK? {validation_result.ok}")

CLI
---
A command line tool is also provided which performs the build and validation steps based
on either command line parameters or on a JSON config file of the same format used by `validate`

::

    xmltest -c config.JSON

The tool will output the build and validation results to stdout, either in tabular form
or as JSON if the `-j` switch is used. If tabular form is used and the rich library is present,
output will be prettier. 

The tool will return:
- 0 if the build and validation steps both succeeded without errors
- if there were fatal build failures
- if there were errors in the instance document validation

As with `validate`, the JSON configuration can either contain a single dict giving
paths to a schema set and a list of instance documents to test against it, or can contain
a list of the same. This allows multiple schema sets and their instance documents to
be tested in one pass.

======= ============
Switch   Description
======= ============
-h      Shows help information
-c      Path to JSON config file (exclusive with -s)
-s      Path to core schema XSD file (exclusive with -c)
-u      Path to a supporting schema file (can be specified multiple times, ignored if -c is given)
-i      Path to an instance XML doc to be validated (can be specified multiple times, ignored if -c is given)
-j      Provide JSON output rather than tabular output
-q      Suppress all output (only return code indicates failure or success)
-v      Verbose. Can be specified multiple times. Ignored if -j or -q is specified
======= ============

The verbosity switch -v can be given multiple times for more verbose output.

- 0: A summary table is printed showing the number of validation targets (schema set + instance docs), total build failures, instance docs and validation failures
- 1: As 0, but a list of issues (build or validation errors) is printed first
- 2: As 1, but a summary of each validation target (build errors, validation errors) is printed first
- 3: As 2, but a detailed list of each file in each validation target is printed first