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

    srcs = []
    if '@' in srcStr:
        try:
            with open(srcStr[srcStr.index('@')+1:], 'w') as f:
                for line in f:
                    srcs.append(line)
        except:
            pass # change this
    
    if not srcs:
        srcs = [ src.strip(' ') for src in srcStr.strip('!').split(', ')] if srcStr != None else []

    dsts = []
    if '@' in destStr:
        try:
            with open(destStr[destStr.index('@')+1:], 'w') as f:
                for line in f:
                    dsts.append(line)
        except:
            pass # change this
    
    if not dsts:
        dsts = [ dst.strip(' ') for dst in destStr.strip('!').split(', ')] if destStr != None else []
    
    prts = [ prt.strip(' ') for prt in portStr.strip('!').split(', ')] if portStr != None else []
    prots = [ prot.strip(' ') for prot in protocolStr.strip('!').split(', ')] if protocolStr != None else []

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
