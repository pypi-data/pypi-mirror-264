import pathlib
import sys
from pathlib import Path

import click
import orjson

from g3t_etl import factory
from g3t_etl.factory import transform_csv
from g3t_etl.submission_dictionary import spreadsheet_json_schema

from g3t_etl.loader import load_plugins
from importlib.metadata import version as pkg_version

from g3t_etl.util.local_fhir_db import LocalFHIRDatabase


class OrderCommands(click.Group):

    def list_commands(self, ctx: click.Context) -> list[str]:
        return list(self.commands)


@click.group(invoke_without_command=True, cls=OrderCommands)
@click.option('--version', is_flag=True, help="Show version")
@click.option('--plugin', help="python module of transformer env:G3T_PLUGIN", envvar="G3T_PLUGIN")
@click.pass_context
def cli(ctx, version, plugin):
    """Create ACED metadata submissions."""
    if version:
        _ = pkg_version('g3t-etl')
        click.echo(_)
        ctx.exit()

    # If no arguments are given, g3t should return the help menu
    if len(sys.argv[1:]) == 0:
        click.echo(ctx.get_help())
        ctx.exit()

    if plugin:
        load_plugins([plugin])
        click.secho(f"Loaded {plugin}", fg="green", file=sys.stderr)
    else:
        click.secho("No plugin loaded", fg="yellow", file=sys.stderr)


@cli.command('dictionary')
@click.argument('input_path', type=click.Path(), default=None,
                required=False)
@click.argument('output_path', type=click.Path(), default='templates/submission.schema.json', required=False)
@click.option('--verbose', default=False, show_default=True, is_flag=True,
              help='verbose output')
def spreadsheet_json_schema_cli(input_path: str, output_path: str, verbose):
    """Code generation. Create python model class from a dictionary spreadsheet.

    \b
    Use this command to track changes to the data dictionary.
    INPUT_PATH: where to read master spreadsheet default: provided by plugin
    OUTPUT_PATH: where to write per subject csvs default: templates/submission.schema.json
    """
    try:
        if not input_path:
            input_path = factory.default_dictionary_path

        input_path = Path(input_path)
        assert input_path.exists(), f"Spreadsheet not found at {input_path},"\
                                    " please see README in docs/ for instructions."
        schema = spreadsheet_json_schema(input_path)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as fp:
            fp.write(orjson.dumps(schema, option=orjson.OPT_INDENT_2).decode())

        click.secho(f"Transformed {input_path} into jsonschema file in {output_path}",
                    fg='green', file=sys.stderr)
        transformer_path = '<your_transformer>'
        if len(factory.transformers) > 0:
            transformer_path = factory.transformers[0].__module__.split('.')[0]

        cmd = f"datamodel-codegen  --input {output_path} --input-file-type jsonschema  "\
              f"--output {transformer_path}/submission.py --field-extra-keys json_schema_extra"
        click.secho("Use this command to generate pydantic model from schema (change paths depending on your environment):", fg='green', file=sys.stderr)
        print(cmd)
    except Exception as e:
        click.secho(f"Error parsing {input_path} into {output_path}: {e}", fg='red')
        if verbose:
            raise e


@cli.command('transform')
@click.argument('input_path', type=click.Path(exists=True, dir_okay=False),
                default=None, required=True)
@click.argument('output_path', type=click.Path(dir_okay=True), default='META', required=False)
@click.option('--verbose', default=False, show_default=True, is_flag=True,
              help='verbose output')
def transform_csv_cli(input_path: str, output_path: str, verbose: bool):
    """Transform csv based on data dictionary to FHIR.

    \b
    INPUT_PATH: where to read spreadsheet. required, (convention data/raw/XXXX.xlsx)
    OUTPUT_PATH: where to write FHIR. default: META/
    """

    transformation_results = transform_csv(input_path=input_path, output_path=output_path, verbose=verbose)
    if not transformation_results.transformer_errors and not transformation_results.validation_errors:
        click.secho(f"Transformed {input_path} into {output_path}", fg='green', file=sys.stderr)
    else:
        click.secho(f"Error transforming {input_path}")
        if verbose:
            click.secho(f"Validation errors: {transformation_results.validation_errors}", fg='red')
            click.secho(f"Transformer errors: {transformation_results.transformer_errors}", fg='red')


@cli.command('dataframe')
@click.argument('input_path',
                default='META',
                type=click.Path(exists=True, dir_okay=True),
                required=False)
@click.argument('output_path',
                type=click.Path(dir_okay=False),
                required=True)
@click.option('--verbose',
              default=False,
              show_default=True, is_flag=True,
              help='verbose output')
def extract_cli(input_path: str, output_path: str, verbose: bool):
    """Create flattened dataframe (experimental).

    \b
    INPUT_PATH: where to read FHIR  default: META/
    OUTPUT_PATH: where to write db.
    """
    db = LocalFHIRDatabase(db_name=pathlib.Path(output_path))
    db.load_ndjson_from_dir(input_path)
    click.secho(f"Exported {input_path} into {output_path}", fg='green', file=sys.stderr)


if __name__ == '__main__':
    cli()
