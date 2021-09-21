import click
from .common import common_options


@click.comamnd()
@common_options()
def search(**kwargs):
    srcStr = kwargs.get('sources', None)
    destStr = kwargs.get('dests', None)
    regStr = kwargs.get('regions', None)
    acctStr = kwargs.get('accounts', None)
    portStr = kwargs.get('ports', None)
    protocolStr = kwargs.get('protocols', None)
    outputStr = kwargs.get('output', None)
