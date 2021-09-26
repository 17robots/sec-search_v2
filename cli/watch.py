import click
from cli.common import common_options, destructure


@click.command()
@common_options
@click.option('-query', default=None, type=str, help="File to output results of command to")
def watch(**kwargs):
    ...


def parse_watch_args(**kwargs):
    [srcStr, destStr, regStr, acctStr, portStr, protocolStr, outputStr, query] = destructure(
        kwargs, 'sources', 'dests', 'regions', 'accounts', 'ports', 'protocols', 'output', 'query')  # grab args
    srcs = []
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

    return [(srcs, '!' in srcStr), (dsts, '!' in destStr), (prts, '!' in portStr), (prots, '!' in protocolStr), (regs, '!' in regStr), (accts, '!' in acctStr), outputStr, query]
