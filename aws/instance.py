def grab_instances(client):
    paginator = client.get_paginator('describe_instances').paginate()
    return [ val for val in paginator ]

class Instance:
    def __init__(self, instance) -> None:
        self.id = instance['InstanceId']
        self.priv_dns = instance['PrivateDnsName']
        self.pub_dns = instance['PublicDnsName']
        self.sec_grps = [grpId['GroupId'] for grpId in instance['SecurityGroups']]
        self.other_grps = [grp['GroupId'] for interface in instance['NetworkInterfaces'] for grp in interface['Groups']]
        self.pub_ip = instance['PublicIpAddress']
        self.vpc_id = instance['VpcId']
        self.priv_ipv4 = [address['PrivateIpAddress'] for interface in instance['NetworkInterfaces'] for address in interface['PrivateIpAddresses']]
        self.priv_ipv6 = [address for interface in instance['NetworkInterfaces'] for address in interface['Ipv6Addresses']]