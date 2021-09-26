import json
from aws.aws_search import aws_search
from aws.sgr import Rule
import click
from .common import *


@click.command()
@click.option('-output', default=None, type=str, help="File to output results of command to")
@click.option('-show-floating', default=False, type=bool, help="Show rules not attached to instances")
@common_options
def search(**kwargs):
    [(srcs, src_inclusive), (dsts, dst_inclusive), (prts, prt_inclusive),
     (prots, prot_inclusive), (regs, reg_inclusive), (accts, acct_inclusive), output, allow_floating] = parse__search_args(kwargs=kwargs)

    print(regs)

    if not allow_floating:
        allow_floating = False

    def filterRule(rule: Rule):
        # if rule.floating and not allow_floating:
        #     print('false 1')
        #     return False
        if not filter_ips(rule.source_ips, srcs, inclusive=src_inclusive):
            return False
        if not filter_ips(rule.dest_ips, dsts, inclusive=dst_inclusive):
            return False
        if not filter_port(rule.to_port, prts, inclusive=prt_inclusive):
            return False
        if not filter_protocol(rule.protocol, prots, inclusive=prot_inclusive):
            return False
        return True

    filters = {
        'account': filter_accounts(accts, acct_inclusive),
        'region': filter_regions(regs, reg_inclusive),
        'rule': filterRule
    }

    print(len(results := aws_search(filters)))


def parse__search_args(**kwargs):
    [srcStr, destStr, regStr, acctStr, portStr, protocolStr, no_ui, outputStr, allow_floating] = destructure(
        kwargs.get('kwargs'), 'sources', 'dests', 'regions', 'accounts', 'ports', 'protocols', 'no_ui', 'output', 'show_floating')  # grab args

    srcs = []
    if srcStr:
        if '@' in srcStr:
            try:
                with open(srcStr[srcStr.index('@')+1:], 'w') as f:
                    for line in f:
                        srcs.append(line)
            except:
                pass  # change this

    if not srcs:
        srcs = [src.strip(' ') for src in srcStr.strip(
            '!').split(',')] if srcStr != None else []

    dsts = []
    if destStr:
        if '@' in destStr:
            try:
                with open(destStr[destStr.index('@')+1:], 'w') as f:
                    for line in f:
                        dsts.append(line)
            except:
                pass  # change this

    if not dsts:
        dsts = [dst.strip(' ') for dst in destStr.strip(
            '!').split(',')] if destStr != None else []

    prts = [prt.strip(' ') for prt in portStr.strip(
        '!').split(',')] if portStr != None else []
    prots = [prot.strip(' ') for prot in protocolStr.strip(
        '!').split(',')] if protocolStr != None else []
    regs = [reg.strip(' ') for reg in regStr.strip(
        '!').split(',')] if regStr != None else []
    accts = [acct.strip(' ') for acct in acctStr.strip(
        '!').split(',')] if acctStr != None else []

    return [(srcs, not '!' in srcStr if srcStr != None else True), (dsts, not '!' in destStr if destStr != None else True), (prts, not '!' in portStr if portStr != None else True), (prots, not '!' in protocolStr if protocolStr != None else True), (regs, not '!' in regStr if regStr != None else True), (accts, not '!' in acctStr if acctStr != None else True), no_ui, outputStr, allow_floating]
