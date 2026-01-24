import click
import shutil
import os
import time
import http.server
import socketserver
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

here = Path(__file__).parent.resolve()
static_dir = here / "static"
template_dir = here / "templates"
project_dir = here.parents[1].resolve()
outpath = project_dir / "docs"

# Contexts
global_context = {"title": "CloverLearn"}


def render_templates():
    """Renders all Jinja2 templates to the output directory."""
    env = Environment(loader=FileSystemLoader(template_dir))

    # Ensure output directory exists
    outpath.mkdir(exist_ok=True)

    # Walk through templates
    for root, _, files in os.walk(template_dir):
        for file in files:
            if file.endswith(".html"):
                template_path = Path(root) / file
                rel_path = template_path.relative_to(template_dir)
                template_name = str(rel_path.as_posix())  # Jinja uses forward slashes

                template = env.get_template(template_name)
                output = template.render(**global_context)

                output_file = outpath / rel_path
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(output)
                print(f"Rendered {template_name}")


def copy_static():
    """Copies static files to the output directory."""
    dest_static = outpath / "static"
    if dest_static.exists():
        shutil.rmtree(dest_static)
    shutil.copytree(static_dir, dest_static)
    print("Copied static files")


def build_site():
    """Builds the entire site."""
    print("Building site...")
    copy_static()
    render_templates()
    print("Build complete.")


class BuildHandler(FileSystemEventHandler):
    """Watchdog handler to rebuild site on file changes."""

    def on_any_event(self, event):
        if event.is_directory:
            return
        print(f"File changed: {event.src_path}")
        try:
            build_site()
        except Exception as e:
            print(f"Build failed: {e}")


@click.group()
def cli():
    pass


@cli.command()
def build():
    """Builds the site once."""
    build_site()


@cli.command()
def watch():
    """Watches for changes and rebuilds."""
    build_site()
    event_handler = BuildHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(here), recursive=True)
    observer.start()
    print(f"Watching {here} for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@cli.command()
@click.option("--port", default=8085, help="Port to serve on")
def serve(port):
    """Serves the built site."""
    # check if outpath exists
    if not outpath.exists():
        print(f"Output directory {outpath} does not exist. Run 'build' first.")
        return

    os.chdir(outpath)

    Handler = http.server.SimpleHTTPRequestHandler
    # Allow address reuse to prevent "Address already in use" errors on restart
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")
            httpd.server_close()


if __name__ == "__main__":
    cli()
