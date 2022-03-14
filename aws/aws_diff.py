# from rich import print
# from threading import Thread
# from aws.sg import grab_sec_groups
# import boto3
# from aws.sso import SSO


# def aws_diff(sg1_id, sg2_id, console_functions):
#     sso = SSO()
#     threads = []
#     sg1_inbound, sg1_outbound = [], []
#     sg2_inbound, sg2_outbound = [], []
#     sg1, sg2 = None, None
#     for region in sso.getRegions():
#         for account in sso.getAccounts()['accountList']:
#             def thread_func():
#                 thread_region = region
#                 thread_account = account['accountId']
#                 try:
#                     creds = sso.getCreds(account_id=thread_account)
#                     client = boto3.client('ec2', region_name=thread_region, aws_access_key_id=creds.access_key,
#                                           aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
#                     for group in grab_sec_groups(client):
#                         if group['GroupId'] == sg1_id:
#                             print('found')
#                             nonlocal sg1
#                             sg1 = group
#                         elif group['GroupId'] == sg2_id:
#                             print('found')
#                             nonlocal sg2
#                             sg2 = group
#                 except:
#                     pass

#             x = Thread(daemon=True, target=thread_func,
#                        name=f"{region}-{account}")
#             threads.append(x)
#             x.start()
#     for process in threads:
#         process.join()

#     if sg1 == None or sg2 == None:
#         if sg1 == None:
#             print(console_functions['error'](
#                 f'Cannot find group {sg1_id}. Stopping'))
#         if sg2 == None:
#             print(console_functions['error'](
#                 f'Cannot find group {sg2_id}. Stopping'))
#         return

#     for rule in sg1['IpPermissions']:
#         if len(list(filter(lambda x: 'ToPort' in x and 'ToPort' in rule and rule['FromPort'] == x['FromPort'] and rule['ToPort'] == x['ToPort'] and rule['IpProtocol'] == x['IpProtocol'] and rule['Description'] == x['Description'], sg2['IpPermissions']))) == 0:
#             sg1_inbound.append(rule)

#     for rule in sg2['IpPermissions']:
#         if len(list(filter(lambda x: 'ToPort' in x and 'ToPort' in rule and rule['FromPort'] == x['FromPort'] and rule['ToPort'] == x['ToPort'] and rule['IpProtocol'] == x['IpProtocol'] and rule['Description'] == x['Description'], sg1['IpPermissions']))) == 0:
#             sg2_inbound.append(rule)

#     for rule in sg1['IpPermissionsEgress']:
#         if len(list(filter(lambda x: 'ToPort' in x and 'ToPort' in rule and rule['FromPort'] == x['FromPort'] and rule['ToPort'] == x['ToPort'] and rule['IpProtocol'] == x['IpProtocol'] and rule['Description'] == x['Description'], sg2['IpPermissionsEgress']))) == 0:
#             sg1_outbound.append(rule)

#     for rule in sg2['IpPermissionsEgress']:
#         if len(list(filter(lambda x: 'ToPort' in x and 'ToPort' in rule and rule['FromPort'] == x['FromPort'] and rule['ToPort'] == x['ToPort'] and rule['IpProtocol'] == x['IpProtocol'] and rule['Description'] == x['Description'], sg1['IpPermissionsEgress']))) == 0:
#             sg2_outbound.append(rule)

#     # output to files
#     with open(f'{sg1_id}-{sg2_id}_{sg1_id}.txt', 'w') as f:
#         f.write('Inbound Rules\n')
#         f.write('\n'.join(str(rule) for rule in sg1_inbound))
#         f.write('\n')
#         f.write('Outbound Rules\n')
#         f.write('\n'.join(str(rule) for rule in sg1_outbound))

#     with open(f'{sg1_id}-{sg2_id}_{sg2_id}.txt', 'w') as f:
#         f.write('Inbound Rules\n')
#         f.write('\n'.join(str(rule) for rule in sg2_inbound))
#         f.write('\n')
#         f.write('Outbound Rules\n')
#         f.write('\n'.join(str(rule) for rule in sg2_outbound))
