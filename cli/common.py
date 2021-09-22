import click


def common_options(func):
    @click.option('-sources', default=None, type=str, help='Name or ip of source vm', required=False)
    @click.option('-dests',  default=None, type=str, help='Name or ip of dest vm', required=False)
    @click.option('-regions', default=None, type=str, help='Regions to filter by', required=False)
    @click.option('-accounts',  default=None, type=str, help='AWS accounts within user credentials to filter by', required=False)
    @click.option('-ports',  default=None, type=str, help='Ports to filter by', required=False)
    @click.option('-protocols',  default=None, type=str, help='Protocols to filter by', required=False)
    @click.option('-output', default=None, type=str, help="File to output results of command to")
    def wrapped_func(*args, **kwargs):
        func(*args, **kwargs)
    return wrapped_func


def destructure(obj, *keys):
    return [obj[k] if k in obj else None for k in keys]
