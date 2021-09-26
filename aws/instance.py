def grab_instances(client):
    paginator = client.get_paginator('describe_instances').paginate()
    return [val for result in paginator for reservation in result['Reservations'] for val in reservation['Instances']]


class Instance:
    def __init__(self, instance) -> None:
        self.id = instance['InstanceId']
        self.priv_dns = instance['PrivateDnsName']
        self.pub_dns = instance['PublicDnsName']
        self.sec_grps = [grpId['GroupId']
                         for grpId in instance['SecurityGroups']]
        self.other_grps = [grp['GroupId']
                           for interface in instance['NetworkInterfaces'] for grp in interface['Groups']]
        self.pub_ip = instance['PublicIpAddress'] if 'PublicIpAddress' in instance else None
        self.vpc_id = instance['VpcId']
        self.priv_ipv4 = [address['PrivateIpAddress'] for interface in instance['NetworkInterfaces']
                          for address in interface['PrivateIpAddresses']]
        self.priv_ipv6 = [address for interface in instance['NetworkInterfaces']
                          for address in interface['Ipv6Addresses']]
