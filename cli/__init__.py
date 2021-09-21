import click
from .diff import diff
from .search import search
from .watch import watch


@click.group()
def cli():
    pass


cli.add_command(search, 'search')
cli.add_command(watch, 'watch')
cli.add_command(diff, 'diff')
