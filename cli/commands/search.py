import boto3
from rich.console import Console
from threading import Thread
from aws.sso import SSO
from ..common import command_arguments
from ..cli import CLI
from aws.instances import grab_instances
from aws.rules import grab_sec_group_rules


@command_arguments
def search(**kwargs):
    print(kwargs)
    console = Console()
    cli = CLI(kwargs=kwargs)
    sso = SSO()
    threads = []
    regions = list(filter(cli.filters['region'].allow, sso.getRegions()))
    accounts = list(
        filter(cli.filters['account'].allow, sso.getAccounts()['accountList']))
    maps = {
        'ruleMap': {},
        'instanceMap': {}
    }
    threads = []
    for region in regions:
        if not region in maps['ruleMap']:
            maps['ruleMap'][region] = {}
            maps['instanceMap'][region] = {}
        for account in accounts:
            if not account['accountId'] in maps['ruleMap'][region]:
                maps['ruleMap'][region][account['accountId']] = []
                maps['instanceMap'][region][account['accountId']] = []

            def thread_function():
                try:
                    reg = region
                    acct = account['accountId']
                    console.print(f"In Thread {reg}-{acct}")
                    creds = sso.getCreds(account=acct)
                    client = boto3.client('ec2', region_name=reg, aws_access_key_id=creds.access_key,
                                          aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                    maps['ruleMap'][reg][acct] = grab_sec_group_rules(client)
                    maps['instanceMap'][reg][acct] = grab_instances(client)
                    maps['ruleMap'][reg][acct] = list(
                        filter(cli.filters['port'].allow, ['ruleMap'][reg][acct]))
                    maps['ruleMap'][reg][acct] = list(
                        filter(cli.filters['protocol'].allow, ['ruleMap'][reg][acct]))
                    maps['ruleMap'][reg][acct] = list(
                        filter(cli.filters['source'].allow, ['ruleMap'][reg][acct]))
                    maps['ruleMap'][reg][acct] = list(
                        filter(cli.filters['dest'].allow, ['ruleMap'][reg][acct]))
                except Exception as e:
                    console.print(e)
            x = Thread(daemon=True, target=thread_function,
                       name=f"{region}-{account['accountId']}")
            threads.append(x)
            x.start()
    for x in threads:
        x.join()
    # for region in maps['ruleMap']:
    #     console.print(f"{region}")
    #     for account in maps['ruleMap'][region]:
    #         console.print(f"\t{account}")
    #         for result in maps['ruleMap'][region][account]:
    #             console.print(f"\t\t{result}")

# def search_thread(**kwargs):
#     cli = CLI(kwargs=kwargs)
#     sso = SSO()
#     threads = []
#     regions = list(filter(cli.filters['region'].allow, sso.getRegions()))
#     accounts = list(
#         filter(cli.filters['account'].allow, sso.getAccounts()['accountList']))
#     search_maps = aws_search_gather(regions=regions, accounts=accounts)
#     for region in search_maps['ruleMap']:
#         for account in search_maps['ruleMap'][region]:
#             def thread_function():
#                 reg = region
#                 acct = account
#                 ['ruleMap'][reg][acct] = list(
#                     filter(cli.filters['port'].allow, ['ruleMap'][reg][acct]))
#                 ['ruleMap'][reg][acct] = list(
#                     filter(cli.filters['protocol'].allow, ['ruleMap'][reg][acct]))
#                 ['ruleMap'][reg][acct] = list(
#                     filter(cli.filters['source'].allow, ['ruleMap'][reg][acct]))
#                 ['ruleMap'][reg][acct] = list(
#                     filter(cli.filters['dest'].allow, ['ruleMap'][reg][acct]))
#             x = Thread(daemon=True, target=thread_function,
#                        name=f"{region}-{account}")
#             threads.append(x)
#             x.start()
#     for x in threads:
#         x.join()
