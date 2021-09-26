import click
import ipaddress


def common_options(func):
    @click.option('-sources', default=None, type=str, help='Name or ip of source vm', required=False)
    @click.option('-dests',  default=None, type=str, help='Name or ip of dest vm', required=False)
    @click.option('-regions', default=None, type=str, help='Regions to filter by', required=False)
    @click.option('-accounts',  default=None, type=str, help='AWS accounts within user credentials to filter by', required=False)
    @click.option('-ports',  default=None, type=str, help='Ports to filter by', required=False)
    @click.option('-protocols',  default=None, type=str, help='Protocols to filter by', required=False)
    @click.option('--no-ui',  default=False, type=bool, help='Disable TUI And Show Raw Output', required=False)
    def wrapped_func(*args, **kwargs):
        func(*args, **kwargs)
    return wrapped_func


def destructure(obj, *keys):
    return [obj[k] if k in obj else None for k in keys]


def filter_regions(regions, inclusive):
    def filter_func(region):
        if len(regions) > 0:
            if region in regions:
                return inclusive
            return not inclusive
        return True
    return filter_func


def filter_accounts(accounts, inclusive):
    def filter_func(account):
        if len(accounts) > 0:
            if account in accounts:
                return inclusive
            return not inclusive
        return True
    return filter_func


# return whether the rule should be let through based on the ip filter
def filter_ips(ips, criteria_ips, inclusive):
    if len(ips) > 0:
        for ip in ips:
            for criteria in criteria_ips:
                x = ipaddress.ip_network(ip)
                y = ipaddress.ip_network(criteria)
                if x.subnet_of(y):
                    return inclusive
                if y.subnet_of(x):
                    return inclusive
                if ip in criteria:
                    return inclusive
                if criteria in ip:
                    return inclusive
            return not inclusive
    return True


# return whether the rule should be let through based on the port filter
def filter_port(port, ports, inclusive):
    if len(ports) > 0:
        if str(port) in ports:
            return inclusive
        return not inclusive
    return True


# return whether the rule should be let through based on the port filter
def filter_protocol(proto, protos, inclusive):
    if len(protos) > 0:
        if proto in protos:
            return inclusive
        return not inclusive
    return True
