from threading import Thread
from aws.common import error_handling
from aws.sg import grab_sec_groups
import boto3
from aws.sso import SSO


def aws_diff(sg1_id, sg2_id):
    sso = SSO()
    threads = []
    sg1 = None
    sg2 = None
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

            x = Thread(daemon=True, target=thread_func,
                       name=f"{region}-{account}")
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

    # output to files
    with open(f'{sg1_id}-{sg2_id}_{sg1}.txt', 'w') as f:
        f.write('Inbound Rules')
        f.write(*sg1['inbound'], sep='\n')
        f.write('Outbound Rules')
        f.write(*sg1['outbound'], sep='\n')
    with open(f'{sg1_id}-{sg2_id}_{sg2_id}.txt', 'w') as f:
        f.write('Inbound Rules')
        f.write(*sg2['inbound'], sep='\n')
        f.write('Outbound Rules')
        f.write(*sg2['outbound'], sep='\n')
