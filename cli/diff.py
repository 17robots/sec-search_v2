from cli.common import destructure
import click


@click.comamnd()
@click.argument('sg1')
@click.argument('sg2')
def diff(**kwargs):
    [sg1, sg2] = destructure(kwargs, 'sg1', 'sg2')
