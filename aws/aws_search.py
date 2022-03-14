import boto3
from threading import Thread
from aws.instance import Instance, grab_instances
from .sso import SSO
from .sgr import grab_sec_group_rules, Rule
from rich import print as richprint


def aws_search(filters):
    auth = SSO()
    threads = []
    ruleMap = {}

    regions = list(filter(filters['region'], auth.getRegions()))
    for region in regions:
        if region not in ruleMap:
            ruleMap[region] = {}
        accounts = list(
            filter(filters['account'], auth.getAccounts()['accountList']))
        for account in accounts:
            if not account['accountId'] in ruleMap[region]:
                ruleMap[region][account['accountId']] = []

            def thread_func(thread_region, thread_account):
                creds = auth.getCreds(account_id=thread_account)
                client = boto3.client('ec2', region_name=thread_region, aws_access_key_id=creds.access_key,
                                      aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                instances = list(
                    map(Instance, grab_instances(client)))
                rules = list(map(lambda x: Rule(x, instances),
                                 grab_sec_group_rules(client)))
                ruleMap[thread_region][thread_account] = list(filter(filters['rule'], rules))

                color = 'red' if len(
                    ruleMap[thread_region][thread_account]) == 0 else 'green'
                richprint(
                    f"[{color}]{thread_region}-{thread_account}: {len(ruleMap[thread_region][thread_account])} results[/{color}]")

            x = Thread(daemon=True, target=thread_func,
                       name=f"{region}-{account['accountId']}", args=(region, account['accountId']))
            threads.append(x)
            x.start()
    for process in threads:
        process.join()

    return [rule for region in ruleMap for account in ruleMap[region] for rule in ruleMap[region][account]]
