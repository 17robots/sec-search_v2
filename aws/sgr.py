from typing import List
from .instance import Instance


def grab_sec_group_rules(client):
    paginator = client.get_paginator('describe_security_group_rules').paginate(
        PaginationConfig={'PageSize': 1000})
    return [val for result in paginator for val in result['SecurityGroupRules']]


class Rule:
    def __init__(self, rule, instances: List[Instance]) -> None:
        self.id = rule['SecurityGroupRuleId']
        self.description = rule['Description'] if 'Description' in rule else ''
        self.source_ips, self.dest_ips, self.floating = self.expand(instances)
        self.group_id = rule['GroupId']
        self.is_egress = rule['IsEgress']
        self.protocol = rule['IpProtocol']
        self.from_port = rule['FromPort']
        self.to_port = rule['ToPort']
        self.cidrv4 = rule['CidrIpv4'] if 'CidrIpv4' in rule else None
        self.cidrv6 = rule['CidrIpv6'] if 'CidrIpv6' in rule else None
        self.ref_group = rule['ReferencedGroupInfo']['GroupId'] if 'ReferencedGroupInfo' in rule else None

    def expand(self, instances: List[Instance]):
        def traceGroup(group):
            ipaddresses = []
            for instance in instances:
                if instance.sec_grps and group in instance.sec_grps:
                    if instance.priv_ipv4:
                        for ip in instance.priv_ipv4:
                            ipaddresses.append(ip)
                    if instance.priv_ipv6:
                        for ip in instance.priv_ipv6:
                            ipaddresses.append(ip)

                if instance.other_grps and group in instance.other_grps:
                    if instance.priv_ipv4:
                        for ip in instance.priv_ipv4:
                            ipaddresses.append(ip)
                    if instance.priv_ipv6:
                        for ip in instance.priv_ipv6:
                            ipaddresses.append(ip)
            return ipaddresses

        myIps = []
        try:
            source_ips = []
            dest_ips = []
            myIps = traceGroup(self.group_id)
            if self.ref_group:
                sec_ips = traceGroup(self.ref_group)
                if self.is_egress:
                    source_ips = myIps
                    dest_ips = sec_ips
            else:
                if self.cidrv4:
                    if self.is_egress:
                        source_ips = myIps
                        dest_ips = [self.cidrv4]
                elif self.cidrv6:
                    if self.is_egress:
                        source_ips = myIps
                        dest_ips = [self.cidrv6]
                else:
                    source_ips = ['0.0.0.0/0']
                    dest_ips = ['0.0.0.0/0']
        except:
            pass
        return source_ips, dest_ips, len(myIps) == 0