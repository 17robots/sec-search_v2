
from datetime import date, datetime, timedelta
import threading
import boto3
from aws.sso import SSO

message_pattern = '/(?<version>\S+)\s+(?<account_id>\S+)\s+(?<interface_id>\S+)\s+(?<srcaddr>\S+)\s+(?<dstaddr>\S+)\s+(?<srcport>\S+)\s+(?<dstport>\S+)\s+(?<protocol>\S+)\s+(?<packets>\S+)\s+(?<bytes>\S+)\s+(?<start>\S+)\s+(?<end>\S+)\s+(?<action>\S+)\s+(?<log_status>\S+)(?:\s+(?<vpc_id>\S+)\s+(?<subnet_id>\S+)\s+(?<instance_id>\S+)\s+(?<tcp_flags>\S+)\s+(?<type>\S+)\s+(?<pkt_srcaddr>\S+)\s+(?<pkt_dstaddr>\S+))?(?:\s+(?<region>\S+)\s+(?<az_id>\S+)\s+(?<sublocation_type>\S+)\s+(?<sublocation_id>\S+))?(?:\s+(?<pkt_src_aws_service>\S+)\s+(?<pkt_dst_aws_service>\S+)\s+(?<flow_direction>\S+)\s+(?<traffic_path>\S+))?/'


# inputs: query, filters, kill_lock
# outputs: none
def aws_watch(**kwargs):
    sso = SSO()
    threads = []
    query = kwargs.get('query', None)
    filters = kwargs.get('filters', None)
    kill_lock = kwargs.get('kill_lock', None)

    for region in list(filter(filters['region'], sso.getRegions())):
        for account in list(filter(filters['account'], sso.getAccounts()['accountList'])):
            try:
                creds = sso.getCreds(account_id=account['accountId'])
                client = boto3.client('ec2', region_name=region, aws_access_key_id=creds.access_key,
                                      aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                paginator = client.get_paginator(
                    'describe_flow_logs').paginate().search("FlowLogs[*].LogGroupName")
                names = [val for val in paginator]
                lock = threading.Lock()

                def thread_func(name):
                    thread_account = account['accountId']
                    nonlocal lock
                    start_time = None
                    while not kill_lock.is_set():
                        try:
                            haveResults = False
                            with lock:
                                creds = sso.getCreds(account_id=thread_account)
                                thread_client = boto3.client('logs', region_name=region, aws_access_key_id=creds.access_key,
                                                             aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                                full_query = f"fields @timestamp, @message | parse @message {message_pattern} {query}"

                                if start_time:
                                    if haveResults:
                                        start_time = end_time
                                        end_time = datetime.now()
                                        haveResults = False
                                else:
                                    end_time = datetime.now()
                                    start_time = end_time - \
                                        timedelta(minutes=5)

                                query_id = thread_client.start_query(logGroupName=name, startTime=int(
                                    start_time.timestamp()), endTime=int(end_time.timestamp()), queryString=full_query)['queryId']
                                while True:
                                    response = thread_client.get_query_results(
                                        queryId=query_id)
                                    if response['results']:
                                        haveResults = True
                                    for result in response['results']:
                                        pass
                                    if response['status'] == 'Complete':
                                        break
                        except:
                            pass
                    return

                for name in names:
                    x = threading.Thread(target=thread_func, args=(
                        name,), name=f"{region}-{account['accountId']}={name}")
                    threads.append(x)
                    x.start()
            except:
                pass
    for process in threads:
        process.join()
