
from botocore.exceptions import ClientError


def get_log_names(client):
    """Get vpc log names from client"""
    paginator = client.get_paginator(
        'describe_flow_logs').paginate()
    return [
        log['LogGroupName'] for val in paginator for log in val['FlowLogs']\
            if 'LogGroupName' in log
    ]


def start_query(client, log_name, start_time, end_time, query):
    """Start query"""
    return client.start_query(
        logGroupName=log_name,
        startTime=int(start_time.timestamp()),
        endTime=int(end_time.timestamp()),
        queryString=query
    )['queryId']


def query_results(client, query_id):
    """Query results"""
    try:
        return client.get_query_results(queryId=query_id)
    except ClientError:
        return None


class Log:
    """
    Log entry class for handling boto3 logs
    Attributes
        main_string (str): The raw log entry
        timestamp (str): The timestamp of the log entry
        version (str): The version of the log entry
        account_id (str): The account ID of the log entry
        interface_id (str): The interface ID of the log entry
        srcaddr (str): The source address of the log entry
        dstaddr (str): The destination address of the log entry
        srcport (str): The source port of the log entry
        dstport (str): The destination port of the log entry
        protocol (str): The protocol of the log entry
        packets (str): The number of packets of the log entry
        bytes (str): The number of bytes of the log entry
        start (str): The start time of the log entry
        end (str): The end time of the log entry
        action (str): The action of the log entry
        log_status (str): The status of the log entry
        vpc_id (str): The VPC ID of the log entry
        subnet_id (str): The subnet ID of the log entry
        instance_id (str): The instance ID of the log entry
        tcp_flags (str): The TCP flags of the log entry
        type (str): The type of the log entry
        pkt_srcaddr (str): The source address of the packet of the log entry
        pkt_dstaddr (str): The destination address of the packet of the log entry
        region (str): The region of the log entry
        az_id (str): The AZ ID of the log entry
        sublocation_type (str): The sublocation type of the log entry
        sublocation_id (str): The sublocation ID of the log entry
        pkt_src_aws_service (str): The source packet of the log entry
        pkt_dst_aws_service (str): The destination packet of the log entry
        flow_direction (str): The flow direction of the log entry
        traffic_path (str): The traffic path of the log entry
    """
    def __init__(self, log_record) -> None:
        """
        Init
        Parameters
            log_record (string): The raw log entry from boto3
        """
        self.main_string = log_record
        fields = log_record.split(' ')
        self.timestamp = fields[0] if fields[0] != '-' else None
        self.version = fields[2] if fields[2] != '-' else None
        self.account_id = fields[3] if fields[3] != '-' else None
        self.interface_id = fields[4] if fields[4] != '-' else None
        self.srcaddr = fields[5] if fields[5] != '-' else None
        self.dstaddr = fields[6] if fields[6] != '-' else None
        self.srcport = fields[7] if fields[7] != '-' else None
        self.dstport = fields[8] if fields[8] != '-' else None
        self.protocol = fields[9] if fields[9] != '-' else None
        self.packets = fields[10] if fields[10] != '-' else None
        self.bytes = fields[11] if fields[11] != '-' else None
        self.start = fields[12] if fields[12] != '-' else None
        self.end = fields[13] if fields[13] != '-' else None
        self.action = fields[14] if fields[14] != '-' else None
        self.log_status = fields[15] if fields[15] != '-' else None
        self.vpc_id = fields[16] if fields[16] != '-' else None
        self.subnet_id = fields[17] if fields[17] != '-' else None
        self.instance_id = fields[18] if fields[18] != '-' else None
        self.tcp_flags = fields[19] if fields[19] != '-' else None
        self.type = fields[20] if fields[20] != '-' else None
        self.pkt_srcaddr = fields[21] if fields[21] != '-' else None
        self.pkt_dstaddr = fields[22] if fields[22] != '-' else None
        self.region = fields[23] if fields[23] != '-' else None
        self.az_id = fields[24] if fields[24] != '-' else None
        self.sublocation_type = fields[25] if fields[25] != '-' else None
        self.sublocation_id = fields[26] if fields[26] != '-' else None
        self.pkt_src_aws_service = fields[27] if fields[27] != '-' else None
        self.pkt_dst_aws_service = fields[28] if fields[28] != '-' else None
        self.flow_direction = fields[29] if fields[29] != '-' else None
        self.traffic_path = fields[30] if fields[30] != '-' else None

    def __str__(self) -> str:
        return f"{self.timestamp} {self.region} {self.account_id}"\
            +f"{self.pkt_srcaddr} {self.pkt_dstaddr} {self.srcport}"\
                +f"{self.dstport} {self.protocol} {self.action}"
