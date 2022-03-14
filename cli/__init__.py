import click
# from .diff import diff
from .search import search
from .log_watch import watch
# from .log_search import log_search


@click.group()
def cli():
    ... ### used for initial cli setup


cli.add_command(search, 'search')
cli.add_command(watch, 'watch')
# cli.add_command(diff, 'diff')
# cli.add_command(log_search, 'log-search')
