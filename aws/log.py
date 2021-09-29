
from dataclasses import field


def get_log_names(client):
    paginator = client.get_paginator(
                    'describe_flow_logs').paginate()
    return [log['LogGroupName'] for val in paginator for log in val['FlowLogs']]

def start_query(client, log_name, start_time, end_time, query):
    return client.start_query(logGroupName=log_name, startTime=int(start_time.timestamp()), endTime=int(
                                end_time.timestamp()), queryString=query)['queryId']

def query_results(client, query_id):
    return client.get_query_results(queryId=query_id)

class Log:
    def __init__(self, log_record) -> None:
        self.main_string = log_record
        fields = log_record.split(' ')
        print(fields)
        self.version = fields[0] if fields[0] != '-' else None
        self.account_id = fields[1] if fields[1] != '-' else None
        self.interface_id = fields[2] if fields[2] != '-' else None
        self.srcaddr = fields[3] if fields[3] != '-' else None
        self.dstaddr = fields[4] if fields[4] != '-' else None
        self.srcport = fields[5] if fields[5] != '-' else None
        self.dstport = fields[6] if fields[6] != '-' else None
        self.protocol = fields[7] if fields[7] != '-' else None
        self.packets = fields[8] if fields[8] != '-' else None
        self.bytes = fields[9] if fields[9] != '-' else None
        self.start = fields[10] if fields[10] != '-' else None
        self.end = fields[11] if fields[11] != '-' else None
        self.action = fields[12] if fields[12] != '-' else None
        self.log_status = fields[13] if fields[13] != '-' else None
        self.vpc_id = fields[14] if fields[14] != '-' else None
        self.subnet_id = fields[15] if fields[15] != '-' else None
        self.instance_id = fields[16] if fields[16] != '-' else None
        self.tcp_flags = fields[17] if fields[17] != '-' else None
        self.type = fields[18] if fields[18] != '-' else None
        self.pkt_srcaddr = fields[19] if fields[19] != '-' else None
        self.pkt_dstaddr = fields[20] if fields[20] != '-' else None
        self.region = fields[21] if fields[21] != '-' else None
        self.az_id = fields[22] if fields[22] != '-' else None
        self.sublocation_type = fields[23] if fields[23] != '-' else None
        self.sublocation_id = fields[24] if fields[24] != '-' else None
        self.pkt_src_aws_service = fields[25] if fields[25] != '-' else None
        self.pkt_dst_aws_service = fields[26] if fields[26] != '-' else None
        self.flow_direction = fields[27] if fields[27] != '-' else None
        self.traffic_path = fields[28] if fields[28] != '-' else None
    
    def __str__(self) -> str:
        return self.vpc_id
        return self.main_string