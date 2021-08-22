from aws.sso import SSO
from ..common import command_arguments
from ..cli import CLI
from aws.commands.search import aws_search_gather


@command_arguments
def diff(**kwargs):
    cli = CLI(kwargs=kwargs)
    sso = SSO()
    regions = list(filter(cli.filters['region'].allow, sso.getRegions()))
    accounts = list(
        filter(cli.filters['account'].allow, sso.getAccounts()['accountList']))
    search_maps = aws_search_gather(regions=regions, accounts=accounts)
