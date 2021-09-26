def grab_sec_groups(client):
    groups = []
    paginator = client.get_paginator('describe_security_groups').paginate(
        PaginationConfig={'PageSize': 1000})
    return [val for result in paginator for val in result['SecurityGroups']]


class GroupRule:
    def __init__(self, rule) -> None:
        self.ipv4s = [ip['CidrIp'] for ip in rule['IpRanges']]
        self.ipv6s = [ip['CidrIp'] for ip in rule['IpRanges']]
        self.from_port = rule['FromPort']
        self.to_port = rule['ToPort']
        self.protocol = rule['IpProtocol']


class Group:
    def __init__(self, group) -> None:
        self.id = group['GroupId']
        self.name = group['GroupName']
        self.descriptiom = group['Description']
        self.vpc = group['VpcId']
        self.inbound = [GroupRule(rule) for rule in group['IpPermissions']]
        self.outbound = [GroupRule(rule)
                         for rule in group['IpPermissionsEgress']]
