from typing import List

from .instance import Instance


def grab_sec_group_rules(client):
    """Grab security group rules from boto3"""
    paginator = client.get_paginator('describe_security_group_rules').paginate(
        PaginationConfig={'PageSize': 1000})
    return [val for result in paginator for val in result['SecurityGroupRules']]


class Rule:
    """
    Rule class for boto3 response
    Attributes:
        id (str): The ID of the security group rule.
        description (str): A description of the rule.
        group_id (str): The security group ID in which the rule belongs.
        is_egress (bool): Indicates whether this is an inbound rule or an outbound rule
        protocol (str): The IP protocol name or number.
        from_port (int): The start of the port range.
        to_port (int): The end of the port range.
        cidrv4 (str): The IPv4 CIDR range.
        cidrv6 (str): The IPv6 CIDR range.
        ref_group (str): The ID of the referenced security group.
        source_ips (List[str]): The source IP addresses.
        dest_ips (List[str]): The destination IP addresses.
        floating (bool): Indicates whether the rule is attached to an instance.
    """
    def expand(self, instances: List[Instance]):
        """
        Expand rules if they have security group ids as source or dest and if they
        are attached to instances
        """
        def traceGroup(group):
            """function wrapper to be called"""
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
        return source_ips, dest_ips, floating

    def __init__(self, rule, instances: List[Instance]) -> None:
        """
        Init
        Parameters:
            rule (dict): The rule dict from boto3
            instances (List[Instance]): List of instances
        """
        self.id = rule['SecurityGroupRuleId']
        self.description = rule['Description'] if 'Description' in rule else ''
        self.group_id = rule['GroupId']
        self.is_egress = rule['IsEgress']
        self.protocol = rule['IpProtocol']
        self.from_port = rule['FromPort']
        self.to_port = rule['ToPort']
        self.cidrv4 = rule['CidrIpv4'] if 'CidrIpv4' in rule else None
        self.cidrv6 = rule['CidrIpv6'] if 'CidrIpv6' in rule else None
        self.ref_group = rule['ReferencedGroupInfo']['GroupId']\
            if 'ReferencedGroupInfo' in rule else None
        self.source_ips, self.dest_ips, self.floating = self.expand(instances)

    def __str__(self) -> str:
        return f"{self.id} {self.description} {self.group_id}"\
            + f"{'Egress' if self.is_egress else 'Ingress'} {self.protocol}"\
            + f"from {self.from_port} to {self.to_port} {self.cidrv4} {self.cidrv6}"\
            + f"{self.ref_group} sources: {self.source_ips} dests: {self.dest_ips}"\
            + f"{'Floating' if self.floating else 'Attached'}"
