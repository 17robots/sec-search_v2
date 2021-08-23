import click
from .commands.search import search
from .commands.watch import watch
from .commands.diff import diff


@click.group()
def cli():
    pass


cli.add_command(search, 'search')
cli.add_command(watch, 'watch')
cli.add_command(diff, 'diff')
