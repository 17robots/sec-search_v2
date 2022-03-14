import click
import time
from aws.aws_search import aws_search
from aws.sgr import Rule
from datetime import datetime
from .common import *
from cli.console_logger import console_functions


@click.command()
@click.option('-output', default=None, type=str, help="File to output results of command to")
@click.option('-show-floating', default=False, type=bool, help="Show rules not attached to instances")
@common_options
def search(**kwargs):
    [(srcs, src_inclusive), (dsts, dst_inclusive), (prts, prt_inclusive),
     (prots, prot_inclusive), (regs, reg_inclusive), (accts, acct_inclusive)] = parse_common_args(kwargs=kwargs)

    # command-specific args
    [output, allow_floating] = destructure(kwargs, 'output', 'show_floating')

    if not allow_floating:
        allow_floating = False

    def filterRule(rule: Rule):
        if rule.floating == True and allow_floating == False:
            return False
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

    start = time.time()
    results = aws_search(filters)
    print(f'{len(results)} results found in {time.time() - start}s')
    filename = output if output != None else "{}-{}.txt".format("search",
                                                                str(datetime.now()).replace(" ", "_").replace(":", "-"))
    print(f"Printing results to {filename}")
    try:
        with open(filename, 'w') as f:
            f.write('\n'.join([str(result) for result in results]))
    except Exception as e:
        print(str(e))
    if len(results) < 20:
        print('\n'.join([str(result) for result in results]))
