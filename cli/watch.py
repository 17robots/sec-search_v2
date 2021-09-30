from aws.aws_watch import aws_watch
import click
from cli.common import common_options, destructure, filter_accounts, filter_regions, parse_common_args
from threading import Event, Thread
import keyboard
from cli.console_logger import console_functions


@click.command()
@click.option('-query', default=None, type=str, help="File to output results of command to")
@common_options
def watch(**kwargs):
    kill_lock = Event()
    [info] = destructure(console_functions, 'info')
    [(srcs, src_inclusive), (dsts, dst_inclusive), (prts, prt_inclusive),
     (prots, prot_inclusive), (regs, reg_inclusive), (accts, acct_inclusive)] = parse_common_args(kwargs=kwargs)

    [query_param] = destructure(kwargs, 'query')
    query = build_query(srcs=srcs, src_inclusive=src_inclusive,
                        dsts=dsts, dst_inclusive=dst_inclusive, prts=prts, prt_inclusive=prt_inclusive, prots=prots, prot_inclusive=prot_inclusive, query=query_param)
    info(query)
    return
    watch_thread = Thread(target=aws_watch, args=(query, {
        'region': filter_regions(regs, reg_inclusive),
        'account': filter_accounts(accts, acct_inclusive)
    }, kill_lock, console_functions))

    watch_thread.start()
    keyboard.add_hotkey(hotkey='q', callback=kill_lock.set, suppress=True)
    watch_thread.join()

def build_query(**kwargs):
    protocol_table = {
        'tcp': 6,
        'udp': 17,
        'something': -1,
    }

    [srcs, src_incl, dsts, dst_incl, prts, prt_incl, prots, prot_incl, query] = destructure(
        kwargs, 'srcs', 'src_inclusive', 'dsts', 'dst_inclusive', 'prts', 'prt_inclusive', 'prots', 'prot_inclusive', 'query')
    if query:
        return query

    return_query = ''
    if len(srcs) > 0:
        not_string = 'not ' if not src_incl else ''
        return_query += f" | filter {not_string}("
        for src in srcs:
            return_query += f"pkt_srcaddr = \"{src}\" or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    if len(dsts) > 0:
        not_string = 'not ' if not dst_incl else ''
        return_query += f" and {not_string}(" if return_query != '' else f"| filter {not_string}("
        for dst in dsts:
            return_query += f"pkt_dstaddr = \"{dst}\" or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    if len(prts) > 0:
        not_string = 'not ' if not prt_incl else ''
        return_query += f" and {not_string}(" if return_query != '' else f"| filter {not_string}("
        for prt in prts:
            return_query += f"srcport = \"{prt}\" or "
            return_query += f"dstport = \"{prt}\" or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    if len(prots) > 0:
        not_string = 'not ' if not prot_incl else ''
        return_query += f" and {not_string}(" if return_query != '' else f"| filter {not_string}("
        for prot in prots:
            if not prot in protocol_table:
                print(f'[yellow]ignoring {prot}[/yellow]')
                continue
            return_query += f"protocol = {protocol_table[prot]} or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    return return_query
