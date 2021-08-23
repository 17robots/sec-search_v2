from threading import Thread
from aws.instances import grab_instances
from aws.rules import grab_sec_group_rules
from logging import getLogger

import boto3
from aws.sso import SSO

# logger = getLogger(__name__)


def aws_search_gather(regions, accounts):
    sso = SSO()
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

            def thread_function(region, account):
                try:
                    reg = region
                    acct = account['accountId']
                    creds = sso.getCreds(account=acct)
                    client = boto3.client('ec2', region_name=reg, aws_access_key_id=creds.access_key,
                                          aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                    maps['ruleMap'][reg][acct] = grab_sec_group_rules(client)
                    maps['instanceMap'][reg][acct] = grab_instances(client)
                except:
                    pass
            x = Thread(daemon=True, target=thread_function,
                       name=f"{region}-{account['accountId']}")
            threads.append(x)
            x.start()
    for x in threads:
        x.join()
    return maps
