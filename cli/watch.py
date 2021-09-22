import click
from cli.common import common_options, destructure


@click.comamnd()
@common_options
@click.option('-query', default=None, type=str, help="File to output results of command to")
def watch(**kwargs):
    [srcStr, destStr, regStr, acctStr, portStr, protocolStr, outputStr, queryStr] = destructure(
        kwargs, 'sources', 'dests', 'regions', 'accounts', 'ports', 'protocols', 'output', 'query')  # grab args
