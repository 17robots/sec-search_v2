import boto3
from traceback import print_stack
from threading import Thread
from aws.instance import Instance, grab_instances
from .sso import SSO
from .sgr import grab_sec_group_rules, Rule


def aws_search(filters):
    auth = SSO()
    threads = []
    ruleMap = {}

    regions = list(filter(filters['region'], auth.getRegions()))
    for region in regions:
        if not region in ruleMap:
            ruleMap[region] = {}
        accounts = list(
            filter(filters['account'], auth.getAccounts()['accountList']))
        for account in accounts:
            if not account['accountId'] in ruleMap[region]:
                ruleMap[region][account['accountId']] = []

            def thread_func():
                try:
                    thread_region = region
                    thread_account = account['accountId']
                    creds = auth.getCreds(account_id=thread_account)
                    client = boto3.client('ec2', region_name=region, aws_access_key_id=creds.access_key,
                                          aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                    instances = list(
                        map(lambda x: Instance(x), grab_instances(client)))
                    rules = list(map(lambda x: Rule(x, instances),
                                     grab_sec_group_rules(client)))
                    print(f'{thread_region}-{thread_account}: {len(rules)}')
                    ruleMap[thread_region][thread_account] = list(filter(lambda x: filters['rule'](
                        x), rules))
                except Exception as e:
                    print_stack(e)

            x = Thread(daemon=True, target=thread_func,
                       name=f"{region}-{account['accountId']}")
            threads.append(x)
            x.start()
    for process in threads:
        process.join()
    return [rule for region in ruleMap for account in ruleMap[region] for rule in ruleMap[region][account]]
