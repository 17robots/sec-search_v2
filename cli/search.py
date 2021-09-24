from aws.aws_search import aws_search
from aws.sgr import Rule
import click
from .common import *


@click.command()
@common_options
@click.option('-output', default=None, type=str, help="File to output results of command to")
@click.option('--show-floating', default=False, type=bool, help="Show rules not attached to instances")
def search(**kwargs):
    [srcStr, destStr, regStr, acctStr, portStr, protocolStr, outputStr, allow_floating] = destructure(
        kwargs, 'sources', 'dests', 'regions', 'accounts', 'ports', 'protocols', 'output', 'show-floating')  # grab args

    def filterRule(rule: Rule):
        if rule.floating and not allow_floating:
            return False

        inclusive = ''
        if not filter_ips(rule.source_ips, [], inclusive=inclusive):
            return False
        if not filter_ips(rule.dest_ips, [], inclusive=inclusive):
            return False

        inclusive = ''
        if not filter_port(rule.to_port, [], inclusive=inclusive):
            return False

        inclusive = ''
        if not filter_protocol(rule.protocol, [], inclusive=inclusive):
            return False

    filters = {
        'accounts': filter_accounts,
        'regions': filter_regions,
        'rules': filterRule
    }

    results = aws_search(filters)
