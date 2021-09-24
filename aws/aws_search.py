from threading import Thread
from aws.instance import Instance, grab_instances
import boto3
from sso import SSO
from sgr import grab_sec_group_rules, Rule

def aws_search(filters):
    sso = SSO()
    threads = []
    ruleMap = {}

    for region in list(filter(filters['region'], sso.getRegions())):
        if not region in ruleMap:
            ruleMap[region] = {}
        for account in list(filter(filters['account'], sso.getAccounts()['accountList'])):
            if not account['accountId'] in ruleMap[region]:
                ruleMap[region][account['accountId']] = []
            
            def thread_func():
                try:
                    thread_region = region
                    thread_account = account['accountId']
                    creds = sso.getCreds(account_id=thread_account)
                    client = boto3.client('ec2', region_name=region, aws_access_key_id=creds.access_key,
                                                  aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                    instances = list(map(lambda x : Instance(x), grab_instances(client)))
                    ruleMap[thread_region][thread_account] = filter(lambda x : filters['rule'](x, instances), list(map(lambda x : Rule(x), grab_sec_group_rules(client))))
                except:
                    pass

            x = Thread(daemon=True, target=thread_func, name=f"{region}-{account['accountId']}")
            threads.append(x)
            x.start()
            for process in threads:
                process.join()
        return [rule for region in ruleMap for account in ruleMap[region] for rule in ruleMap[region][account]]