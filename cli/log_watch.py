import click
from threading import Event, Thread
import keyboard
from rich import print as richprint

from cli.console_logger import console_functions
from cli.common import common_options, destructure, filter_accounts, filter_regions,\
    parse_common_args, build_query
from aws.aws_watch import aws_watch


@click.command()
@click.option(
    '-query',
    default=None,
    type=str,
    help="Query to run against cloudwatch"
)
@common_options
def watch(**kwargs):
    """Watch function called when using cli command"""
    kill_lock = Event()
    [info] = destructure(console_functions, 'info')
    [
        (srcs, src_inclusive),
        (dsts, dst_inclusive),
        (prts, prt_inclusive),
        (prots, prot_inclusive),
        (regs, reg_inclusive),
        (accts, acct_inclusive)
    ] = parse_common_args(kwargs=kwargs)

    [query_param] = destructure(
        kwargs, 'query')
    query = ""
    query = build_query(
        srcs=srcs,
        src_inclusive=src_inclusive,
        dsts=dsts,
        dst_inclusive=dst_inclusive,
        prts=prts,
        prt_inclusive=prt_inclusive,
        prots=prots,
        prot_inclusive=prot_inclusive,
        query=query_param
    )
    richprint(info(f"query: {query}"))
    # return
    watch_thread = Thread(target=aws_watch, args=(query, {
        'region': filter_regions(regs, reg_inclusive),
        'account': filter_accounts(accts, acct_inclusive)
    }, kill_lock))

    watch_thread.start()
    keyboard.add_hotkey(hotkey='q', callback=kill_lock.set, suppress=True)
    watch_thread.join()
