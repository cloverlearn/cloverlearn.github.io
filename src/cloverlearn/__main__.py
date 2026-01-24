import click

from staticjinja import Site
from pathlib import Path
from flask import Flask, send_from_directory
import shutil

here = Path(__file__).parent.resolve()

static_dir = here / "static"
template_dir = here / "templates"

project_dir = here.parents[1].resolve()

outpath = project_dir / "docs"

contexts = [
    (".*", {"title": "CloverLearn"}),
]


def copy_static_dir():
    if outpath.exists():
        shutil.rmtree(outpath)
    shutil.copytree(static_dir, outpath / "static")


@click.group()
def cli(): ...


@cli.command()
def watch():
    site = Site.make_site(
        searchpath=template_dir,
        outpath=outpath,
        contexts=contexts,
    )
    copy_static_dir()
    site.render(use_reloader=True)


@cli.command()
def serve():
    app = Flask(__name__, static_folder=str(outpath))

    @app.route("/")
    def index():
        return send_from_directory(str(outpath), "index.html")

    @app.route("/<path:filename>")
    def serve_static(filename):
        return send_from_directory(str(outpath), filename)

    app.run(port=8085, debug=True)


if __name__ == "__main__":
    cli()
