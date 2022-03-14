from aws.aws_diff import aws_diff
from cli.common import destructure
from cli.console_logger import console_functions
import click


# @click.command()
# @click.argument('sg1', nargs=1)
# @click.argument('sg2', nargs=1)
# def diff(**kwargs):
#     [sg1, sg2] = destructure(kwargs, 'sg1', 'sg2')
#     aws_diff(sg1, sg2, console_functions)
