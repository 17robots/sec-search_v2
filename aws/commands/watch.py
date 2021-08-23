from aws.logs import grab_flow_logs
import boto3
from datetime import datetime, timedelta
from time import sleep
from threading import Thread, Event
from aws.sso import SSO


def aws_watch(accounts, regions, filterstring, killEvent: Event):
    sso = SSO()
    threads = []
    for region in regions:
        for account in accounts:
            try:
                creds = sso.getCreds(account=account)
                client = boto3.client('ec2', region_name=region, aws_access_key_id=creds.access_key,
                                      aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                names = grab_flow_logs(client)

                def sub_thread_func(name):
                    myAccount = account
                    start_time = None
                    while not killEvent.is_set():
                        try:
                            haveResults = False
                            creds = sso.getCreds(account=myAccount)
                            threadClient = boto3.client('logs', region_name=region, aws_access_key_id=creds.access_key,
                                                        aws_secret_access_key=creds.secret_access_key, aws_session_token=creds.session_token)
                            # {cli.buildFilters()}
                            fullQuery = f"fields @timestamp, @message | parse @message {filterstring}"

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
                                    # do something with the results for the ui
                                    sleep(.5)
                                if response['status'] == 'Complete':
                                    break
                        except Exception as e:
                            break
                    return

                for name in names:
                    x = Thread(daemon=True, target=sub_thread_func, args=(
                        name,), name=f"{region}-{account['accountId']}-{name}")
                    threads.append(x)
                    x.start()

            except Exception as e:
                pass
        for process in threads:
            process.join()
