from aws.aws_watch import aws_watch
import click
from cli.common import common_options, destructure, filter_accounts, filter_regions
from threading import Event

@click.command()
@click.option('-query', default=None, type=str, help="File to output results of command to")
@common_options
def watch(**kwargs):
    kill_lock = Event()
    [(srcs, src_inclusive), (dsts, dst_inclusive), (prts, prt_inclusive),
     (prots, prot_inclusive), (regs, reg_inclusive), (accts, acct_inclusive), query, no_ui] = parse_watch_args(kwargs=kwargs)
    aws_watch(query="", filters={
        'region': filter_regions(regs, reg_inclusive),
        'account': filter_accounts(accts, acct_inclusive)
    }, kill_lock=kill_lock)


def parse_watch_args(**kwargs):
    [srcStr, destStr, regStr, acctStr, portStr, protocolStr, query, no_ui] = destructure(
        kwargs, 'sources', 'dests', 'regions', 'accounts', 'ports', 'protocols', 'query', 'no_ui')  # grab args
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
            '!').split(', ')] if srcStr != None else []

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
            '!').split(', ')] if destStr != None else []

    prts = [prt.strip(' ') for prt in portStr.strip(
        '!').split(', ')] if portStr != None else []
    prots = [prot.strip(' ') for prot in protocolStr.strip(
        '!').split(', ')] if protocolStr != None else []
    regs = [reg.strip(' ') for reg in regStr.strip(
        '!').split(', ')] if protocolStr != None else []
    accts = [acct.strip(' ') for acct in acctStr.strip(
        '!').split(', ')] if protocolStr != None else []

    return [(srcs, not '!' in srcStr if srcStr != None else True), (dsts, not '!' in destStr if destStr != None else True), (prts, not '!' in portStr if portStr != None else True), (prots, not '!' in protocolStr if protocolStr != None else True), (regs, not '!' in regStr if regStr != None else True), (accts, not '!' in acctStr if acctStr != None else True), query, no_ui]
