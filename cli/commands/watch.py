from os import kill
from threading import Event
from aws.commands.watch import aws_watch
from cli.common import command_arguments
from cli.cli import CLI
from aws.sso import SSO


@command_arguments
def watch(**kwargs):
    pass


def watch_thread(**kwargs):
    cli = CLI(kwargs, subcommand="watch")
    sso = SSO()
    regions = list(filter(cli.filters['region'].allow, sso.getRegions()))
    accounts = list(
        filter(cli.filters['account'].allow, sso.getAccounts()['accountList']))
    killEvent = Event()
    killEvent.clear()
    aws_watch(accounts=accounts, regions=regions,
              filterstring=cli.buildQuery(), killEvent=kwargs.get('killEvent'))
