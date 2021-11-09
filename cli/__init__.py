import click
from .diff import diff
from .search import search
from .log_watch import watch


@click.group()
def cli():
    pass


cli.add_command(search, 'search')
cli.add_command(watch, 'log-watch')
cli.add_command(diff, 'diff')
