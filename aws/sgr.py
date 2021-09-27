from typing import List
from traceback import print_stack
from .instance import Instance


def grab_sec_group_rules(client):
    paginator = client.get_paginator('describe_security_group_rules').paginate(
        PaginationConfig={'PageSize': 1000})
    return [val for result in paginator for val in result['SecurityGroupRules']]


class Rule:
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

        floating: bool
        try:
            source_ips = []
            dest_ips = []
            myIps = traceGroup(self.group_id)
            floating = len(myIps) == 0
            if self.ref_group:
                sec_ips = traceGroup(self.ref_group)
                if self.is_egress:
                    source_ips = myIps
                    dest_ips = sec_ips
                else:
                    source_ips = sec_ips
                    dest_ips = myIps
            elif self.cidrv4:
                if self.is_egress:
                    source_ips = myIps
                    dest_ips = [self.cidrv4]
                else:
                    source_ips = [self.cidrv4]
                    dest_ips = myIps
            elif self.cidrv6:
                if self.is_egress:
                    source_ips = myIps
                    dest_ips = [self.cidrv6]
                else:
                    source_ips = [self.cidrv6]
                    dest_ips = myIps
            else:
                source_ips = ['0.0.0.0/0']
                dest_ips = ['0.0.0.0/0']
        except Exception as e:
            print_stack(e)
        return source_ips, dest_ips, floating

    def __init__(self, rule, instances: List[Instance]) -> None:
        self.id = rule['SecurityGroupRuleId']
        self.description = rule['Description'] if 'Description' in rule else ''
        self.group_id = rule['GroupId']
        self.is_egress = rule['IsEgress']
        self.protocol = rule['IpProtocol']
        self.from_port = rule['FromPort']
        self.to_port = rule['ToPort']
        self.cidrv4 = rule['CidrIpv4'] if 'CidrIpv4' in rule else None
        self.cidrv6 = rule['CidrIpv6'] if 'CidrIpv6' in rule else None
        self.ref_group = rule['ReferencedGroupInfo']['GroupId'] if 'ReferencedGroupInfo' in rule else None
        self.source_ips, self.dest_ips, self.floating = self.expand(instances)

    def __str__(self) -> str:
        return f"{self.id} {self.description} {self.group_id} {'Egress' if self.is_egress else 'Ingress'} {self.protocol} from {self.from_port} to {self.to_port} {self.cidrv4} {self.cidrv6} {self.ref_group} sources: {self.source_ips} dests: {self.dest_ips} {'Floating' if self.floating else 'Attached'}"
