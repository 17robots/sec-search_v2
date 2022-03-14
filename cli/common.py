import click
import ipaddress


def common_options(func):
    """Wrapper for multiple common options for commands"""
    @click.option('-sources', default=None, type=str, help='Name or ip of source vm', required=False)
    @click.option('-dests',  default=None, type=str, help='Name or ip of dest vm', required=False)
    @click.option('-regions', default=None, type=str, help='Regions to filter by', required=False)
    @click.option('-accounts',  default=None, type=str, help='AWS accounts within user credentials to filter by', required=False)
    @click.option('-ports',  default=None, type=str, help='Ports to filter by', required=False)
    @click.option('-protocols',  default=None, type=str, help='Protocols to filter by', required=False)
    @click.option('--no-ui',  default=False, type=bool, help='Disable TUI And Show Raw Output', required=False)
    def wrapped_func(*args, **kwargs):
        """function wrapper to be called"""
        func(*args, **kwargs)
    return wrapped_func


def destructure(obj, *keys):
    """Destructure a dict into a list of values."""
    return [obj[k] if k in obj else None for k in keys]


def filter_regions(regions, inclusive):
    """Filter regions based on what is specified"""
    def filter_func(region):
        """Function wrapper to be called"""
        if len(regions) > 0:
            if region in regions:
                return inclusive
            return not inclusive
        return True
    return filter_func


def filter_accounts(accounts, inclusive):
    """Filter accounts based on what is specified"""
    def filter_func(account):
        """Function wrapper to be called"""
        if len(accounts) > 0:
            if account['accountId'] in accounts:
                return inclusive
            return not inclusive
        return True
    return filter_func


# return whether the rule should be let through based on the ip filter
def filter_ips(ips, criteria_ips, inclusive):
    """Filter ips based on what is specified"""
    if len(criteria_ips) > 0:
        for ip in ips:
            for criteria in criteria_ips:
                try:
                    x = ipaddress.ip_network(ip)
                    y = ipaddress.ip_network(criteria)
                    if x.subnet_of(y):
                        return inclusive
                    if y.subnet_of(x):
                        return inclusive
                except:
                    continue
                if ip in criteria:
                    return inclusive
                if criteria in ip:
                    return inclusive
            return not inclusive
    return True


# return whether the rule should be let through based on the port filter
def filter_port(port, ports, inclusive):
    """Filter ips based on what is specified"""
    if len(ports) > 0:
        if str(port) in ports:
            return inclusive
        return not inclusive
    return True


# return whether the rule should be let through based on the port filter
def filter_protocol(proto, protos, inclusive):
    """Filter ips based on what is specified"""
    if len(protos) > 0:
        if proto in protos:
            return inclusive
        return not inclusive
    return True


def parse_common_args(**kwargs):
    """Parse and return the common args among commands from console input"""
    [srcStr, destStr, regStr, acctStr, portStr, protocolStr] = destructure(
        kwargs.get('kwargs'), 'sources', 'dests', 'regions', 'accounts', 'ports', 'protocols')  # grab args

    srcs = []
    if srcStr:
        srcs = read_arr_file(srcStr[srcStr.index('@')+1:]) if '@' in srcStr else [src.strip(' ') for src in srcStr.strip('!').split(',')]
    dsts = []
    if destStr:
        dsts = read_arr_file(destStr[destStr.index('@')+1:]) if '@' in destStr else [dst.strip(' ') for dst in destStr.strip('!').split(',')]
    prts = [prt.strip(' ') for prt in portStr.strip(
        '!').split(',')] if portStr is not None else []
    prots = [prot.strip(' ') for prot in protocolStr.strip(
        '!').split(',')] if protocolStr is not None else []
    regs = [reg.strip(' ') for reg in regStr.strip(
        '!').split(',')] if regStr is not None else []
    accts = [acct.strip(' ') for acct in acctStr.strip(
        '!').split(',')] if acctStr is not None else []

    return [(srcs, '!' not in srcStr if srcStr is not None else True), (dsts, '!' not in destStr if destStr is not None else True), (prts, '!' not in portStr if portStr is not None else True), (prots, '!' not in protocolStr if protocolStr is not None else True), (regs, '!' not in regStr if regStr is not None else True), (accts, '!' not in acctStr if acctStr is not None else True)]


def read_arr_file(file):
    """Read lines of file into arr """
    ret = []
    try:
        with open(file, 'w') as f:
            for line in f:
                ret.append(line)
    except:
        pass  # change this
    return ret

def build_query(**kwargs):
    """Create the aws query based on the console args"""
    protocol_table = {
        'tcp': 6,
        'udp': 17,
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
            if prot not in protocol_table:
                print(f'[yellow]ignoring {prot}[/yellow]')
                continue
            return_query += f"protocol = {protocol_table[prot]} or "
        return_query = return_query.rstrip(' or')
        return_query += ')'

    return_query += " and log_status='OK'" if return_query != '' else "| filter log_status='OK'"

    return return_query
