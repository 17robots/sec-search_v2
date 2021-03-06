
import time
from datetime import datetime, timedelta
import threading
import boto3
from rich import print as richprint

from aws.common import error_handling
from aws.log import Log, get_log_names, query_results, start_query
from aws.sso import SSO

message_pattern = r'/(?<version>\S+)\s+(?<account_id>\S+)\s+(?<interface_id>\S+)\s+'\
    + r'(?<srcaddr>\S+)\s+(?<dstaddr>\S+)\s+(?<srcport>\S+)\s+(?<dstport>\S+)\s+'\
    + r'(?<protocol>\S+)\s+(?<packets>\S+)\s+(?<bytes>\S+)\s+(?<start>\S+)\s+'\
    + r'(?<end>\S+)\s+(?<action>\S+)\s+(?<log_status>\S+)(?:\s+(?<vpc_id>\S+)\s+'\
    + r'(?<subnet_id>\S+)\s+(?<instance_id>\S+)\s+(?<tcp_flags>\S+)\s+(?<type>\S+)\s+'\
    + r'(?<pkt_srcaddr>\S+)\s+(?<pkt_dstaddr>\S+))?(?:\s+(?<region>\S+)\s+'\
    + r'(?<az_id>\S+)\s+(?<sublocation_type>\S+)\s+(?<sublocation_id>\S+))?(?:\s+'\
    + r'(?<pkt_src_aws_service>\S+)\s+(?<pkt_dst_aws_service>\S+)\s+'\
    + r'(?<flow_direction>\S+)\s+(?<traffic_path>\S+))?/'


def aws_watch(query, filters, kill_lock):
    """Keep live watch on aws vpc logs using specified filters"""
    sso = SSO()
    threads = []
    regions = list(filter(filters['region'], sso.getRegions()))
    clientLock = threading.Lock()

    for region in regions:
        accounts = list(
            filter(filters['account'], sso.getAccounts()['accountList']))
        for account in accounts:
            creds = sso.getCreds(account_id=account['accountId'])
            client = boto3.client(
                'ec2',
                region_name=region,
                aws_access_key_id=creds.access_key,
                aws_secret_access_key=creds.secret_access_key,
                aws_session_token=creds.session_token
            )
            richprint(
                f"[yellow]Grabbing Names For {region}-{account['accountId']}[/yellow]"
            )
            names = get_log_names(client)

            @error_handling
            def sub_thread_func(name, thread_region, thread_account):
                nonlocal clientLock
                start_time = None
                while True:
                    if kill_lock.is_set():
                        return
                    haveResults = False
                    with clientLock:
                        creds = sso.getCreds(account_id=thread_account)
                        thread_client = boto3.client(
                            'logs',
                            region_name=thread_region,
                            aws_access_key_id=creds.access_key,
                            aws_secret_access_key=creds.secret_access_key,
                            aws_session_token=creds.session_token
                        )
                    full_query = "fields @timestamp, @message | parse @message"\
                        + f"{message_pattern} {query}"
                    if start_time:
                        if haveResults:
                            start_time = end_time
                            end_time = datetime.now()
                            haveResults = False
                    else:
                        end_time = datetime.now()
                        start_time = end_time - \
                            timedelta(minutes=5)

                    query_id = start_query(
                        thread_client, name, start_time, end_time, full_query)
                    if kill_lock.is_set():
                        return
                    while True:
                        response = query_results(
                            thread_client, query_id)
                        if response['results']:
                            haveResults = True
                        for result in response['results']:
                            log_entry = ' '.join(
                                [val['value'] for val in result])
                            log = Log(log_entry)
                            if log.log_status != 'NODATA':
                                color = 'green' if log.action == 'ACCEPT' else 'red'
                                richprint(f"[{color}]{log}[/{color}]")
                            if kill_lock.is_set():
                                return
                            time.sleep(1)

                        if response['status'] == 'Complete':
                            break
            if kill_lock.is_set():
                return
            for name in names:
                x = threading.Thread(
                    target=sub_thread_func,
                    args=(name, region, account['accountId']),
                    name=f"{region}-{account['accountId']}-{name}"
                )
                threads.append(x)
                x.start()
    for process in threads:
        process.join()
