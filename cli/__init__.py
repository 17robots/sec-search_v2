import click
from .search import search
from .log_watch import watch


@click.group()
def cli():
    """Main cli caller for click"""
    ...  # used for initial cli setup


cli.add_command(search, 'search')
cli.add_command(watch, 'watch')
