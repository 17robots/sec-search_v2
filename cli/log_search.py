import click
from cli.common import common_options, parse_common_args, destructure, build_query, filter_accounts, filter_regions
from cli.console_logger import console_functions
from aws.aws_logger import aws_log_grabber
from threading import Thread


# @click.command()
# @click.option('-query', default=None, type=str, help="Query to run against cloudwatch")
# @click.option('-startdate', default=None, type=str, help="Date To Collect Log From")
# @click.option('-enddate', default=None, type=str, help="Date To Collect Log From")
# @click.option('-starttime', default=None, type=str, help="Start time for pulling logs")
# @click.option('-endtime', default=None, type=str, help="End time for pulling logs")
# @click.option('-start', default=None, type=str, help="Start datetime for pulling logs")
# @click.option('-end', default=None, type=str, help="End datetime for pulling logs")
# @common_options
# def log_search(**kwargs):
#     [info] = destructure(console_functions, 'info')
#     [(srcs, src_inclusive), (dsts, dst_inclusive), (prts, prt_inclusive),
#      (prots, prot_inclusive), (regs, reg_inclusive), (accts, acct_inclusive)] = parse_common_args(kwargs=kwargs)

#     [query_param, start_time, end_time, start_date, end_date, start, end] = destructure(
#         kwargs, 'query', 'starttime', 'endtime', 'startdate', 'enddate', 'start', 'end')

#     query = build_query(srcs=srcs, src_inclusive=src_inclusive,
#                         dsts=dsts, dst_inclusive=dst_inclusive, prts=prts, prt_inclusive=prt_inclusive, prots=prots, prot_inclusive=prot_inclusive, query=query_param)

#     print(info(f"query: {query}"))
#     log_thread = Thread(target=aws_log_grabber, args=(query, {
#         'region': filter_regions(regs, reg_inclusive),
#         'account': filter_accounts(accts, acct_inclusive)
#     }, start_date, end_date, start_time, end_time, start, end))

#     log_thread.start()
#     log_thread.join()
