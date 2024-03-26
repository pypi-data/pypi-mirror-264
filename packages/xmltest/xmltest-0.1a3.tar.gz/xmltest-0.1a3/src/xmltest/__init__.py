"""XMLTest XML validation helper"""

__version__ = "0.1a3"

from typing import Sequence
from argparse import ArgumentParser
from pathlib import Path
from json import loads, dumps

from .validator import build_schema
from .instance_docs import test_instance_docs, validate


def _print_aligned_result (condition: bool, slug: str, if_true:str, if_false: str, width = 50, padchar = "."):
    print (f"{slug}{if_true.rjust(width-len(slug), padchar) if condition else if_false.rjust(width-len(slug), padchar)}")

def _error_to_str(error: Exception, verbose = False):
    if verbose:
        return str(error)
    if hasattr(error, "message"):
        return error.message
    elif hasattr(error, "msg"):
        return error.msg
    else:
        return f"{error!r}"

def _expand_paths(paths : Sequence[str], glob_str : str = None) -> Sequence[Path]:
    out_paths = []
    for str_path in paths:
        path = Path(str_path)
        if path.is_dir():
            for file in path.rglob(glob_str):
                out_paths.append(file)
        else:
            out_paths.append(path)
    return out_paths


def xmltest_console():
    parser = ArgumentParser(description="Build a schema set and use it to validate zero or more instance documents. Returns 1 if the schema build fails, 2 if any of the instance documents fail to validate, or 0 otherwise. If JSON output is selected via the -j switch, it is always 0")
    arg_group = parser.add_mutually_exclusive_group(required=True)
    arg_group.add_argument("-c", "--config", help="Specifies the location of a JSON config file")
    arg_group.add_argument("-s", "--coreschema", help="Specifies the location of the core XSD schema file")
    parser.add_argument("-u", "--supportingschema", action="append", help="Specifies the location of any supporting schemas required. If a directory is specified, xmltest will search and add any XSD files recursively within the directory")
    parser.add_argument("-i", "--instancedoc", action="append", help="Instance XML document to validate against the schema. If a directory is specified, xmltest will search and add any XML files recursively within the directory")
    parser.add_argument("-j", "--jsonoutput", action="store_true", help="Output JSON instead of text. Return code will always be zro")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output")
    parser.add_argument("-v", action="count", help="Verbose. Can be specified multiple times to get more detailed output")
    parser.add_argument("-z", action="store_true", help="Force non-rich-format output (pip install rich to get pretty output)")
    pargs = parser.parse_args()

    verbosity = pargs.v if pargs.v else 0

    if pargs.config:
        json_config = loads(Path(pargs.config).read_text())
    else:
        if pargs.supportingschema:
            supporting_schemas = _expand_paths(pargs.supportingschema, "*.xsd")
        else:
            supporting_schemas = []
        if pargs.instancedoc:
            instance_docs = _expand_paths(pargs.instancedoc, "*.xml")
        else:
            instance_docs = []

        json_config = {
            "coreSchema" : pargs.coreschema,
            "supportingSchemas" : supporting_schemas,
            "exampleFiles" : instance_docs,
        }

    results = list(validate(json_config))

    total_fatal_build_failures = 0
    total_build_errors = 0
    total_validation_failures = 0
    total_instance_docs = 0

    for target in results:
        if not target.build_ok:
            total_fatal_build_failures += 1
        for build_result in target.build_results:
            if not build_result.ok:
                total_build_errors += len(build_result.errors)
        else:
            for v_result in target.validation_results:
                total_instance_docs += 1
                if not v_result.ok:
                    total_validation_failures += len(v_result.errors)

    if pargs.jsonoutput:
        from json import JSONEncoder
        from dataclasses import is_dataclass, asdict
        class jx(JSONEncoder):
            def default(self, o):
                if is_dataclass(o):
                    return asdict(o)
                if isinstance(o, Path):
                    return str(o.resolve())
                if isinstance(o, Exception):
                    return str(o)
                return super().default(o)
        
        j = dumps(results, cls=jx)
        rprint(j)
        exit(0)

    try:
        if pargs.z:
            raise ModuleNotFoundError("Aborting attempt to import rich")
        from rich import print as rprint, box
        from rich.console import Console, Group
        from rich.panel import Panel
        from rich.table import Table
        from rich.rule import Rule

        console = Console()
        use_rich = True
    except ModuleNotFoundError:
        use_rich = False
        if (verbosity > 3):
            print ("Rich not found, falling back to regular console (use 'pip install rich' to make this prettier)")

    if not pargs.quiet:
        from os import get_terminal_size
        width = get_terminal_size().columns
        if verbosity > 2:
            if use_rich:
                for target in results:
                    table = Table(show_header=False, expand=True, box=box.ROUNDED)
                    table.add_column("String")
                    table.add_column("Status", width=4)
                    table.add_row(f"Building [yellow]{target.core_schema_path}[/]",
                                  "[green]OK[/]" if target.build_ok else "[red]Fail[/]")
                    table.add_section()
                    for build_result in target.build_results:
                        table.add_row(str(build_result.file), "[green]OK[/]" if build_result.ok else "[red]Fail[/]")
                        for error in build_result.errors:
                            table.add_row(f"[red]{_error_to_str(error, verbosity > 3)}[/]","")
                    table.add_section()
                    table.add_row(f"Validating instance documents","")
                    table.add_section()
                    for vresult in target.validation_results:
                        table.add_row(f"{vresult.file.resolve()}",
                                      "[green]OK[/]" if vresult.ok else "[red]Fail[/]")
                        for error in vresult.errors:
                            table.add_row(f"[yellow]{_error_to_str(error, verbosity > 3)}[/]","")
                    console.print(table)
            else:
                for target in results:
                    build_errors = 0
                    validation_failures = 0

                    print ("=" * width)
                    print (f"Testing target {target.core_schema_path}")
                    print ("-" * width)
                    _print_aligned_result(target.build_ok, "  Build", "[OK]", "[FAIL]", width=width)
                    for build_result in target.build_results:
                        build_errors += len(build_result.errors)
                        _print_aligned_result(build_result.ok, "    " + str(build_result.file.resolve()), "[OK]", "[FAIL]", width=width)
                        for error in build_result.errors:
                            print(f"      {_error_to_str(error, verbosity > 3)}")
                    print ("-" * width)
                    print(f"  Validating {len(target.validation_results)} instance documents")

                    for vresult in target.validation_results:
                        validation_failures += len(vresult.errors)
                        _print_aligned_result(vresult.ok, "    " + str(vresult.file.resolve()), "[OK]", "[FAIL]", width=width)
                        for error in vresult.errors:
                            print(f"      {_error_to_str(error, verbosity > 3)}")         
        if verbosity > 1:
            if use_rich:
                table = Table(show_header=True, expand=True, box=box.ROUNDED)
                table.add_column("File")
                table.add_column("Built")
                table.add_column("XSD")
                table.add_column("Err")
                table.add_column("XML")
                table.add_column("Err")
                for target in results:
                    build_errors = 0
                    validation_failures = 0

                    build_files = len(target.build_results)
                    build_error_count = sum([len(error.errors) for error in target.build_results])
                    instance_files = len(target.validation_results)
                    validation_error_count = sum([len(error.errors) for error in target.validation_results])

                    table.add_row(str(target.core_schema_path.name),
                                  "[green]OK[/]" if target.build_ok else "[red]Fail[/]",
                                  str(build_files),
                                  f"{"[green]" if build_error_count == 0 else "[red]"}{build_error_count}[/]",
                                  str(instance_files),
                                  f"{"[green]" if validation_error_count == 0 else "[red]"}{validation_error_count}[/]")
                console.print(table)
            else:
                print ("=" * width)
                print ("Build summary (Core file [status] [XSD files/errors] [XML files/errors])")
                for target in results:
                    build_errors = 0
                    validation_failures = 0

                    build_files = len(target.build_results)
                    build_error_count = sum([len(error.errors) for error in target.build_results])
                    instance_files = len(target.validation_results)
                    validation_error_count = sum([len(error.errors) for error in target.validation_results])

                    status_line = f"{"[OK]  " if target.build_ok else "[FAIL] "} [{build_files}/{build_error_count}] [{instance_files}/{validation_error_count}]"
                    print(f"  {target.core_schema_path}{status_line.rjust(width - len(str(target.core_schema_path)) - 2, ".")}")

        if verbosity > 0:
            if use_rich:
                table = Table(show_header=False, expand=True, box=box.ROUNDED)
                if (total_build_errors + total_fatal_build_failures + total_validation_failures) == 0:
                    table.add_row(f"Issues{"[green]None[/]".rjust(width, " ")}")
                else:
                    table.add_row(f"Issues")
                    for target in results:
                        for result in target.build_results:
                            for error in result.errors:
                                table.add_section()
                                table.add_row(f"Build error in [red]{result.file}[/]")
                                table.add_row(f"  {_error_to_str(error, verbosity > 1)}")
                        for result in target.validation_results:
                            for error in result.errors:
                                table.add_section()
                                table.add_row(f"Validation error in [red]{result.file}[/]")
                                table.add_row(f"against {target.core_schema_path}")
                                table.add_row(f"[yellow]{_error_to_str(error, verbosity > 1)}[/]")
                console.print(table)
            else:
                print ("=" * width)

                if (total_build_errors + total_fatal_build_failures + total_validation_failures) == 0:
                    print (f"Issues{"None".rjust(width-10," ")}")
                else:
                    print ("Issues")
                    for target in results:
                        for result in target.build_results:
                            for error in result.errors:
                                print ("-" * width)
                                print (f"Build error in {result.file}")
                                print (f"  {_error_to_str(error, verbosity > 1)}")
                        for result in target.validation_results:
                            for error in result.errors:
                                print ("-" * width)
                                print (f"Validation error in {result.file}")
                                print (f"  (against {target.core_schema_path})")
                                print (f"  {_error_to_str(error, verbosity > 1)}")

        if use_rich:
            table = Table(show_header=False, expand=True, box=box.ROUNDED)
            table.add_column("Field", width=8, justify="left")
            table.add_column("Value", justify="left")
            table.add_row("Validation targets", str(len(results)))
            table.add_row("Build failures", f"{"[green]" if total_fatal_build_failures == 0 else "[red]"}{total_fatal_build_failures}[/] fatal, {"[green]" if total_build_errors == 0 else "[yellow]"}{total_build_errors}[/] non-fatal")
            table.add_row("Validation instance docs", str(total_instance_docs))
            table.add_row("Validation failures", f"{"[green]" if total_validation_failures == 0 else "[red]"}{str(total_validation_failures)}[/]")
            table.add_section()
            table.add_row("Outcome", "[green]OK[/]" if total_fatal_build_failures + total_validation_failures == 0 else "[red]FAIL[/]")
            console.print(table)
        else:
            print ("=" * width)
            print (f"Validation targets.........{len(results)}")
            print (f"Build failures.............{total_fatal_build_failures} fatal, {total_build_errors} non-fatal")
            print (f"Validation instance docs...{total_instance_docs}")
            print (f"Validation failures........{total_validation_failures}")
            print (f"Outcome....................{"OK" if total_fatal_build_failures + total_validation_failures == 0 else "FAIL"}")
            print ("=" * width)

    if total_fatal_build_failures > 0:
        exit(1)
    if total_validation_failures > 0:
        exit(2)