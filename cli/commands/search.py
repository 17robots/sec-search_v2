from threading import Thread
from aws.sso import SSO
from ..common import command_arguments
from ..cli import CLI
from aws.commands.search import aws_search_gather


@command_arguments
def search(**kwargs):
    pass


def filterSearch(**kwargs):
    cli = CLI(kwargs=kwargs)
    sso = SSO()
    threads = []
    regions = list(filter(cli.filters['region'].allow, sso.getRegions()))
    accounts = list(
        filter(cli.filters['account'].allow, sso.getAccounts()['accountList']))
    search_maps = aws_search_gather(regions=regions, accounts=accounts)
    for region in search_maps['ruleMap']:
        for account in search_maps['ruleMap'][region]:
            def thread_function():
                reg = region
                acct = account
                ['ruleMap'][reg][acct] = list(
                    filter(cli.filters['port'].allow, ['ruleMap'][reg][acct]))
                ['ruleMap'][reg][acct] = list(
                    filter(cli.filters['protocol'].allow, ['ruleMap'][reg][acct]))
                ['ruleMap'][reg][acct] = list(
                    filter(cli.filters['source'].allow, ['ruleMap'][reg][acct]))
                ['ruleMap'][reg][acct] = list(
                    filter(cli.filters['dest'].allow, ['ruleMap'][reg][acct]))
            x = Thread(daemon=True, target=thread_function,
                       name=f"{region}-{account}")
            threads.append(x)
            x.start()
    for x in threads:
        x.join()
