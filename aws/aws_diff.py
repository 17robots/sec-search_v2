from rich import print
from threading import Thread
from aws.sg import grab_sec_groups
import boto3
from aws.sso import SSO


def aws_diff(sg1_id, sg2_id, console_functions):
    sso = SSO()
    threads = []
    sg1, sg2 = None, None
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
                        if group['GroupId'] == sg1_id:
                            print('found')
                            nonlocal sg1
                            sg1 = group
                        elif group['GroupId'] == sg2_id:
                            print('found')
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
            print(console_functions['error'](
                f'Cannot find group {sg1_id}. Stopping'))
        if sg2 == None:
            print(console_functions['error'](
                f'Cannot find group {sg2_id}. Stopping'))
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
