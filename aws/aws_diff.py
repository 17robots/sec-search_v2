from threading import Thread
from aws.sg import grab_sec_groups
import boto3
from aws.sso import SSO


def diff(sg1_id, sg2_id):
    sso = SSO()
    threads = []
    group1_rules = []
    group2_rules = []
    sg1, sg2 = None
    for region in sso.getRegions():
        for account in sso.getAccounts()['accountList']:
            def thread_func():
                thread_region = region
                thread_account = account['accountId']
                try:
                    creds = sso.getCreds(account_id=thread_account)
                    client = boto3.client('ec2', region_name=thread_region, aws_access_key_id=creds.access_key,
                                              aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                    for group in grab_sec_groups(client):
                        if group.id == sg1_id:
                            nonlocal sg1
                            sg1 = group
                        elif group.id == sg2_id:
                            nonlocal sg2
                            sg2 = group
                except:
                    pass
            
            x = Thread(daemon=True, target=thread_func, name=f"{region}-{account}")
            threads.append(x)
            x.start()
    for process in threads:
        process.join()
    
    if sg1 == None or sg2 == None:
        if sg1 == None:
            if sg2 == None:
                pass
            else:
                pass
            return
        if sg2 == None:
            pass
        return