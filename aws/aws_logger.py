import boto3
from aws.common import error_handling
from aws.log import Log, get_log_names, query_results, start_query
from aws.sso import SSO
from datetime import datetime, timedelta, timestamp

import threading

message_pattern = '/(?<version>\S+)\s+(?<account_id>\S+)\s+(?<interface_id>\S+)\s+(?<srcaddr>\S+)\s+(?<dstaddr>\S+)\s+(?<srcport>\S+)\s+(?<dstport>\S+)\s+(?<protocol>\S+)\s+(?<packets>\S+)\s+(?<bytes>\S+)\s+(?<start>\S+)\s+(?<end>\S+)\s+(?<action>\S+)\s+(?<log_status>\S+)(?:\s+(?<vpc_id>\S+)\s+(?<subnet_id>\S+)\s+(?<instance_id>\S+)\s+(?<tcp_flags>\S+)\s+(?<type>\S+)\s+(?<pkt_srcaddr>\S+)\s+(?<pkt_dstaddr>\S+))?(?:\s+(?<region>\S+)\s+(?<az_id>\S+)\s+(?<sublocation_type>\S+)\s+(?<sublocation_id>\S+))?(?:\s+(?<pkt_src_aws_service>\S+)\s+(?<pkt_dst_aws_service>\S+)\s+(?<flow_direction>\S+)\s+(?<traffic_path>\S+))?/'


def aws_log_grabber(query, filters, start_date, end_date, start_time, end_time, start_time_full, end_time_full):

    # handle time conversion

    # so there are 2 ways we can handle this
    # 1. we can use a date and a time for each and then we can convert them to datetimes and add them
    # lets do this one first
    query_start_datetime: datetime
    try:
        query_start_datetime = datetime.combine(
            datetime.date(start_date), datetime.time(start_time))
    except Exception as e:
        print(e)
        return

    query_end_datetime: datetime
    try:
        query_end_datetime = datetime.combine(
            datetime.date(end_date), datetime.time(end_time))
    except Exception as e:
        print(e)
        return
    # 2. we can make them submit the datetime in the proper format
    try:
        query_start_datetime = datetime(start_time_full)
        query_end_datetime = datetime(end_time_full)
    except Exception as e:
        print(e)
        return
    # do our bound checking

    # start after end
    if start_date > end_date:
        raise ValueError('Start date cannot be after end date')

    # end date not tomorrow

    # start not in future

    sso = SSO()
    threads = []
    log_entries = []
    client_lock = threading.Lock()
    regions = list(filter(filters['region'], sso.getRegions()))

    for region in regions:
        accounts = list(
            filter(filters['account'], sso.getAccounts()['accountList']))

        for account in accounts:
            creds = sso.getCreds(account_id=account['accountId'])
            client = boto3.client('ec2', region_name=region, aws_access_key_id=creds.access_key,
                                  aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
            names = get_log_names(client)

            @error_handling
            def thread_function(name):
                thread_region = region
                thread_account = account
                thread_account_id = thread_account['accountId']

                # deal with the times and date
                nonlocal client_lock
                with client_lock:
                    creds = sso.getCreds(account_id=thread_account_id)
                    thread_client = boto3.client('logs', region_name=thread_region, aws_access_key_id=creds.access_key,
                                                 aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                full_query = f"fields @timestamp, @message | parse @message {message_pattern} {query}"
# bound check
#  check the start time is lesser than the end time
#  check the start time is not in the future
#  then check end time is not beyond the current time??
# start threads that go through the logs specified in the regions and accounts
# start polling the log items
# throw into large list
# sort it based on time
# spit out to file
# log size of the list as x records found
