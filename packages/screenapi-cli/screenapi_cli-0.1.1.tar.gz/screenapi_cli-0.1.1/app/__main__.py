import os
import sys

sys.path.append(os.curdir)

from rich import print
import asyncio
import typer
import configparser
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from app.setup.utils import add_to_config, config_file


try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


app = typer.Typer()
config = configparser.ConfigParser()
config.read(config_file())

try:
    config.add_section("default")
except configparser.DuplicateSectionError:
    pass


# custom
def configGet(section: str, key: str, fallback: str = None):
    if config.has_option(section, key):
        return config.get(section, key)
    else:
        return fallback


@app.command(help="Scrape data")
def scrape(
    urls_file: str,
    concurrency: Optional[int] = configGet("default", "concurrency"),
    overwrite: Optional[bool] = False,
):
    from app.scrape.cli import main

    asyncio.run(main(concurrency=concurrency, urls_file=urls_file, overwrite=overwrite))


@app.command(help="Setup screenapi-cli to work with api")
def setup(
    api_url: Annotated[str, typer.Option(help="api url of hosted screenapi instance")],
    api_key: Annotated[str, typer.Option(help="api key of hosted screenapi instance")],
    namespace: Annotated[str, typer.Option(help="namespace used to generate uuid")],
    # config_file: Optional[str] = config_file(),
    output_dir: Optional[str] = configGet("default", "output_dir"),
    export_dir: Optional[str] = configGet("default", "export_dir"),
    concurrency: Optional[int] = configGet("default", "concurrency"),
):  # complete
    if not os.path.exists(config_file()):
        output_dir = os.path.join(config_file(True), "output")
        export_dir = os.path.join(config_file(True), "export")
        concurrency = 10

    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)
        add_to_config("output_dir", output_dir)

    if concurrency is not None:
        add_to_config("concurrency", str(concurrency))

    if export_dir is not None:
        os.makedirs(export_dir, exist_ok=True)
        add_to_config("export_dir", export_dir)

    add_to_config("api_url", api_url)
    add_to_config("api_key", api_key)
    add_to_config("namespace", namespace)


@app.command(
    help="""
Export data

Example:
    1. export --input-dir 'flipkart' --output-file 'output.xlsx' --sort-by 'sl'\n\n 
    * `filpkart` will convert into --input-dir=/path/to/output/dir/"flipkart"\n\n
    * `output.xlsx` will convert into --output-file=/path/to/output/dir/"output.xlsx"\n\n

    ---\n\n
    2. export --input-dir './flipkart' --output-file './output.xlsx' --sort-by 'sl'\n\n
    * `filpkart` will convert into --input-dir=/current/dir/"flipkart"\n\n
    * `output.xlsx` will convert into --output-file=/current/dir/"output.xlsx"\n\n


"""
)
def export(
    input_dir: Annotated[str, typer.Option(help="input directory")],
    output_file: Annotated[str, typer.Option(help="output file")] = None,
    sort_by: Annotated[str, typer.Option(help="sort by")] = "sl",
):
    from app.export.cli import main

    if not input_dir.startswith("./") and not input_dir.startswith("/"):
        input_dir = os.path.join(config.get("default", "output_dir"), input_dir)

    if output_file is None:
        output_file = os.path.join(
            os.path.abspath(input_dir), Path(input_dir).stem + ".xlsx"
        )
    elif not output_file.startswith("./") and not output_file.startswith("/"):
        output_file = os.path.join(config.get("default", "output_dir"), output_file)

    print(f"[bold]Exporting data from {input_dir} to {output_file} and sort by [violet]{sort_by}[/]")

    main(input_dir=input_dir, output=output_file, sort_by=sort_by)


@app.command(help="List config")
def list():
    for section in config.sections():
        print(f"[bold]\[{section}]")
        options = config.options(section)
        for option in options:
            value = config.get(section, option)
            print(f"{option} = {value}")
    

if __name__ == "__main__":
    app()
