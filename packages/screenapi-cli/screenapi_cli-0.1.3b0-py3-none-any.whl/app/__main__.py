import os
import random
import sys

from httpx import request

sys.path.append(os.curdir)

from importlib.metadata import version
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


def get_random_epilog():
    texts = [
        "Give us a star :star: on [b][violet]https://github.com/FutureForge-Studios/screenapi-cli[/]",
        "Made with :heart: by [b i][violet]FF Studios[/]",
    ]

    return random.choice(texts)


app = typer.Typer(
    name="screenapi-cli",
    rich_markup_mode="rich",
    no_args_is_help=True,
    epilog=get_random_epilog(),
)


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
    max_workers: Annotated[int, typer.Option(help="number of workers")] = configGet(
        "default", "max_workers"
    ),
    overwrite: Annotated[bool, typer.Option(help="overwrite existing data")] = False,
    skip_images: Annotated[bool, typer.Option(help="skip saving images")] = False,
):
    from app.scrape.cli import main

    print("Scraping...")
    print(f"Urls file: {urls_file}")
    print(f"Number of workers: {max_workers}")
    print(f"Overwrite existing data: {overwrite}")
    print(f"Skip saving images: {skip_images}")

    try:
        asyncio.run(
            main(
                max_workers=max_workers,
                urls_file=urls_file,
                overwrite=overwrite,
                skip_images=skip_images,
            )
        )
    except KeyboardInterrupt:
        print("Exiting...")


@app.command(help="Setup screenapi-cli to work with api")
def setup(
    api_url: Annotated[str, typer.Option(help="api url of hosted screenapi instance")],
    api_key: Annotated[str, typer.Option(help="api key of hosted screenapi instance")],
    namespace: Annotated[str, typer.Option(help="namespace used to generate uuid")],
    # config_file: Optional[str] = config_file(),
    output_dir: Optional[str] = configGet("default", "output_dir"),
    export_dir: Optional[str] = configGet("default", "export_dir"),
    max_workers: Optional[int] = configGet("default", "max_workers"),
):  # complete
    if not os.path.exists(config_file()):
        output_dir = os.path.join(config_file(True), "output")
        export_dir = os.path.join(config_file(True), "export")
        max_workers = 10

    if output_dir is not None:
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        add_to_config("output_dir", output_dir)

    if max_workers is not None:
        add_to_config("max_workers", str(max_workers))

    if export_dir is not None:
        export_dir = os.path.abspath(export_dir)
        os.makedirs(export_dir, exist_ok=True)
        add_to_config("export_dir", export_dir)

    add_to_config("api_url", api_url)
    add_to_config("api_key", api_key)
    add_to_config("namespace", namespace)


@app.command(
    help="""
Export data

Example:
1. export --input-dir 'flipkart' --output-file 'output.xlsx' --sort-by 'sl'
    * `filpkart` will convert into --input-dir=/path/to/output/dir/"flipkart"
    * `output.xlsx` will convert into --output-file=/path/to/output/dir/"output.xlsx"

2. export --input-dir './flipkart' --output-file './output.xlsx' --sort-by 'sl'
    * `filpkart` will convert into --input-dir=/current/dir/"flipkart"
    * `output.xlsx` will convert into --output-file=/current/dir/"output.xlsx"

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

    print(
        f"[bold]Exporting data from {input_dir} to {output_file} and sort by [violet]{sort_by}[/]"
    )

    main(input_dir=input_dir, output=output_file, sort_by=sort_by)


@app.command(help="List config", name='config')
def list_configs():
    for section in config.sections():
        print(f"[bold]\[{section}]")
        options = config.options(section)
        for option in options:
            value = config.get(section, option)
            print(f"{option} = {value}")


# @app.add_typer(yper.Typer(name="check"), help="Check application health")
def version_callback(show: bool):
    __version__ = version("screenapi-cli")

    def fetch_stable_version():
        response = request("GET", "https://pypi.org/pypi/screenapi-cli/json")
        if response.status_code == 200:
            data = response.json()
            return data["info"]["version"]

    def fetch_latest_version():
        response = request("GET", "https://pypi.org/pypi/screenapi-cli/json")
        if response.status_code == 200:
            data = response.json()
            return list(data["releases"].keys())[-1]

    if show:
        stable_version = fetch_stable_version()
        latest_version = fetch_latest_version()

        if stable_version == latest_version:
            print(f"[bold white]Current version: [cyan]{__version__}[/]")
            print(f"[bold white]Stable version: [violet]{stable_version}[/]")
        else:
            print(f"[bold white]Current version: [cyan]{__version__}[/]")
            print(f"[bold white]Stable version: [violet]{stable_version}[/]")
            print(f"[bold white]Latest version: [violet]{latest_version}[/]")

        if __version__ != stable_version:
            if __version__ == latest_version:
                raise typer.Exit()
            print(
                f"[bold white]Update available:[/] [code black]pip install --upgrade screenapi-cli=={latest_version}[/]\n\n[b]More details on [yellow]https://pypi.org/project/screenapi-cli/"
            )

        raise typer.Exit()


@app.callback(
    invoke_without_command=True,
    rich_help_panel=True,
)
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            help="Check version",
            callback=version_callback,
        ),
    ] = False,
):
    pass


if __name__ == "__main__":
    # appWithoutCommand()
    app()
