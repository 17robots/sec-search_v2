from cli.common import destructure
import click


@click.command()
@click.argument('sg1', nargs=1)
@click.argument('sg2', nargs=1)
def diff(**kwargs):
    [sg1, sg2] = destructure(kwargs, 'sg1', 'sg2')
