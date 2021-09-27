import time
from datetime import datetime, timedelta
import threading
import boto3
from aws.sso import SSO
from traceback import print_stack


message_pattern = '/(?<version>\S+)\s+(?<account_id>\S+)\s+(?<interface_id>\S+)\s+(?<srcaddr>\S+)\s+(?<dstaddr>\S+)\s+(?<srcport>\S+)\s+(?<dstport>\S+)\s+(?<protocol>\S+)\s+(?<packets>\S+)\s+(?<bytes>\S+)\s+(?<start>\S+)\s+(?<end>\S+)\s+(?<action>\S+)\s+(?<log_status>\S+)(?:\s+(?<vpc_id>\S+)\s+(?<subnet_id>\S+)\s+(?<instance_id>\S+)\s+(?<tcp_flags>\S+)\s+(?<type>\S+)\s+(?<pkt_srcaddr>\S+)\s+(?<pkt_dstaddr>\S+))?(?:\s+(?<region>\S+)\s+(?<az_id>\S+)\s+(?<sublocation_type>\S+)\s+(?<sublocation_id>\S+))?(?:\s+(?<pkt_src_aws_service>\S+)\s+(?<pkt_dst_aws_service>\S+)\s+(?<flow_direction>\S+)\s+(?<traffic_path>\S+))?/'


def aws_watch(**kwargs):
    sso = SSO()
    filters = kwargs.get('filters')
    query = kwargs.get('query')
    kill_lock = kwargs.get('kill_lock')
    threads = []
    regions = list(filter(filters['region'], sso.getRegions()))

    for region in regions:
        accounts = list(
            filter(filters['account'], sso.getAccounts()['accountList']))
        for account in accounts:
            try:
                creds = sso.getCreds(account_id=account['accountId'])
                client = boto3.client('ec2', region_name=region, aws_access_key_id=creds.access_key,
                                      aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                paginator = client.get_paginator(
                    'describe_flow_logs').paginate().search("FlowLogs[*].LogGroupName")

                names = [val for val in paginator]
                clientLock = threading.Lock()

                def sub_thread_func(name):
                    myAccount = account
                    thread_account = myAccount['accountId']
                    nonlocal clientLock

                    start_time = None
                    while not kill_lock.is_set():
                        try:
                            haveResults = False
                            with clientLock:
                                creds = sso.getCreds(account_id=thread_account)
                                threadClient = boto3.client('logs', region_name=region, aws_access_key_id=creds.access_key,
                                                            aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                            fullQuery = f"fields @timestamp, @message | parse @message {message_pattern} {query}"

                            if start_time:
                                if haveResults:
                                    start_time = end_time
                                    end_time = datetime.now()
                                    haveResults = False
                            else:
                                end_time = datetime.now()
                                start_time = end_time - \
                                    timedelta(minutes=5)

                            query_id = threadClient.start_query(logGroupName=name, startTime=int(start_time.timestamp()), endTime=int(
                                end_time.timestamp()), queryString=fullQuery)['queryId']
                            while True:
                                response = threadClient.get_query_results(
                                    queryId=query_id)
                                if response['results']:
                                    haveResults = True
                                for result in response['results']:
                                    print(' '.join([val['value']
                                                    for val in result]))
                                    time.sleep(1)

                                if response['status'] == 'Complete':
                                    break
                        except Exception as e:
                            print_stack(e)
                            break
                    return

                for name in names:
                    x = threading.Thread(target=sub_thread_func, args=(
                        name,), name=f"{region}-{account['accountId']}-{name}")
                    threads.append(x)
                    x.start()

            except Exception as e:
                print_stack(e)
    for process in threads:
        process.join()
