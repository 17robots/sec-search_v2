import click
from .common import common_options, destructure


@click.comamnd()
@common_options()
@click.option('-output', default=None, type=str, help="File to output results of command to")
def search(**kwargs):
    [srcStr, destStr, regStr, acctStr, portStr, protocolStr, outputStr] = destructure(
        kwargs, 'sources', 'dests', 'regions', 'accounts', 'ports', 'protocols', 'output')  # grab args
