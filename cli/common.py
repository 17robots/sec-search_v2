import click


def common_options(func):
    @click.option('-sources', default=None, type=str, help='Name or ip of source vm', required=False)
    @click.option('-dests',  default=None, type=str, help='Name or ip of dest vm', required=False)
    @click.option('-regions', default=None, type=str, help='Regions to filter by', required=False)
    @click.option('-accounts',  default=None, type=str, help='AWS accounts within user credentials to filter by', required=False)
    @click.option('-ports',  default=None, type=str, help='Ports to filter by', required=False)
    @click.option('-protocols',  default=None, type=str, help='Protocols to filter by', required=False)
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
            else:
                return not inclusive
        return True
    return filter_func


def filter_accounts(accounts, inclusive):
    def filter_func(account):
        if len(account) > 0:
            if account in accounts:
                return inclusive
            else:
                return not inclusive
        return True
    return filter_func


# return whether the rule should be let through based on the ip filter
def filter_ips(ips, criteria_ips, inclusive):
    if len(ips) > 0:
        for ip in ips:
            if ip in criteria_ips:
                return inclusive
            return not inclusive
    return True


# return whether the rule should be let through based on the port filter
def filter_port(port, ports, inclusive):
    if len(ports) > 0:
        if port in ports:
            return inclusive
        else:
            return not inclusive
    return True


# return whether the rule should be let through based on the port filter
def filter_protocol(proto, protos, inclusive):
    if len(protos) > 0:
        if proto in protos:
            return inclusive
        else:
            return not inclusive
    return True
