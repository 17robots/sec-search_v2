import click


@click.comamnd()
@click.argument('sg1')
@click.argument('sg2')
def diff(**kwargs):
    sg1 = kwargs.get('sg1', None)
    sg2 = kwargs.get('sg1', None)
