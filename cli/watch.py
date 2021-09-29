from aws.aws_watch import aws_watch
import click
from cli.common import common_options, destructure, filter_accounts, filter_regions, parse_common_args
from threading import Event, Thread
import keyboard


@click.command()
@click.option('-query', default=None, type=str, help="File to output results of command to")
@common_options
def watch(**kwargs):
    kill_lock = Event()
    [(srcs, src_inclusive), (dsts, dst_inclusive), (prts, prt_inclusive),
     (prots, prot_inclusive), (regs, reg_inclusive), (accts, acct_inclusive), no_ui] = parse_common_args(kwargs=kwargs)

    [query_param] = destructure(kwargs, 'query')
    query = build_query(srcs=srcs, src_inclusive=src_inclusive,
                        dsts=dsts, dst_inclusive=dst_inclusive, prts=prts, prt_inclusive=prt_inclusive, prots=prots, prot_inclusive=prot_inclusive, query=query_param)
    print(f'query: {query}')

    watch_thread = Thread(target=aws_watch, args=(query, {
        'region': filter_regions(regs, reg_inclusive),
        'account': filter_accounts(accts, acct_inclusive)
    }, kill_lock))

    watch_thread.start()
    keyboard.add_hotkey(hotkey='q', callback=kill_lock.set, suppress=True)
    watch_thread.join()


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
        return_query += " and (" if return_query != '' else "| filter ("
        for dst in dsts:
            return_query += f"pkt_dstaddr = \"{dst}\" or " if dst_incl else f"pkt_dstaddr != \"{dst}\" or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    if len(prts) > 0:
        return_query += " and (" if return_query != '' else "| filter ("
        for prt in prts:
            return_query += f"srcport = \"{prt}\" or " if prt_incl else f"srcport != \"{prt}\" or "
            return_query += f"dstport = \"{prt}\" or " if prt_incl else f"dstport != \"{prt}\" or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    if len(prots) > 0:
        return_query += " and (" if return_query != '' else "| filter ("
        for prot in prots:
            return_query += f"protocol = \"{prot}\" or " if prot_incl else f"protocol != \"{prot}\" or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    return return_query
