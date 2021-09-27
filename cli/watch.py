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
     (prots, prot_inclusive), (regs, reg_inclusive), (accts, acct_inclusive), no_ui, query] = parse_watch_args(kwargs=kwargs)

    query = build_query(srcs=srcs, src_inclusive=src_inclusive,
                        dsts=dsts, dst_inclusive=dst_inclusive, prts=prts, prt_inclusive=prt_inclusive, prots=prots, prot_inclusive=prot_inclusive, query=query)
    aws_watch(query=query, filters={
        'region': filter_regions(regs, reg_inclusive),
        'account': filter_accounts(accts, acct_inclusive)
    }, kill_lock=kill_lock)


def parse_watch_args(**kwargs):
    [srcStr, destStr, regStr, acctStr, portStr, protocolStr, no_ui, query] = destructure(
        kwargs.get('kwargs'), 'sources', 'dests', 'regions', 'accounts', 'ports', 'protocols', 'no_ui', 'query')  # grab args
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
            '!').split(',')] if destStr != None else []

    prts = [prt.strip(' ') for prt in portStr.strip(
        '!').split(',')] if portStr != None else []
    prots = [prot.strip(' ') for prot in protocolStr.strip(
        '!').split(',')] if protocolStr != None else []
    regs = [reg.strip(' ') for reg in regStr.strip(
        '!').split(',')] if regStr != None else []
    accts = [acct.strip(' ') for acct in acctStr.strip(
        '!').split(',')] if acctStr != None else []

    return [(srcs, not '!' in srcStr if srcStr != None else True), (dsts, not '!' in destStr if destStr != None else True), (prts, not '!' in portStr if portStr != None else True), (prots, not '!' in protocolStr if protocolStr != None else True), (regs, not '!' in regStr if regStr != None else True), (accts, not '!' in acctStr if acctStr != None else True), no_ui, query]


def build_query(**kwargs):
    [srcs, src_incl, dsts, dst_incl, prts, prt_incl, prots, prot_incl, query] = destructure(
        kwargs, 'srcs', 'src_inclusive', 'dsts', 'dst_inclusive', 'prts', 'prt_inclusive', 'prots', 'prot_inclusive', 'query')
    if query:
        return query

    return_query = ''
    if len(srcs) > 0:
        return_query += " | filter ("
        for src in srcs:
            return_query += f"pkt_srcaddr = \"{src}\" or " if src_incl else f"pkt_srcaddr != \"{src}\" or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    if len(dsts) > 0:
        return_query += " and (" if not return_query else "| filter ("
        for dst in dsts:
            return_query += f"pkt_dstaddr = \"{dst}\" or " if dst_incl else f"pkt_dstaddr != \"{dst}\" or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    if len(prts) > 0:
        return_query += " and (" if not return_query else "| filter ("
        for prt in prts:
            return_query += f"srcport = \"{prt}\" or " if prt_incl else f"srcport != \"{prt}\" or "
            return_query += f"dstport = \"{prt}\" or " if prt_incl else f"dstport != \"{prt}\" or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    if len(prots) > 0:
        return_query += " and (" if not return_query else "| filter ("
        for prot in prots:
            return_query += f"protocol = \"{prot}\" or " if prot_incl else f"protocol != \"{prot}\" or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    return return_query
