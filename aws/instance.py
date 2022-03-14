def grab_instances(client):
    """Grab instances from aws"""
    paginator = client.get_paginator('describe_instances').paginate()
    return [
        val for
        result in paginator
        for reservation in result['Reservations']
        for val in reservation['Instances']
    ]


class Instance:
    """
    Instance class based on data from boto3
    Attributes:
        id (str): instance id
        priv_dns (str): private dns name
        pub_dns (str): public dns name
        sec_grps (list): security groups
        other_grps (list): other groups
        pub_ip (str): public ip address
        vpc_id (str): vpc id
        priv_ipv4 (list): private ipv4 addresses
        priv_ipv6 (list): private ipv6 addresses
    """

    def __init__(self, instance) -> None:
        """
        Init
        Parameters
            instance (string): instance data from boto3 as string
        """
        self.id = instance['InstanceId']
        self.priv_dns = instance['PrivateDnsName']
        self.pub_dns = instance['PublicDnsName']
        self.sec_grps = [grpId['GroupId']
                         for grpId in instance['SecurityGroups']]
        self.other_grps = [
            grp['GroupId'] for interface in instance['NetworkInterfaces']
            for grp in interface['Groups']
        ]
        self.pub_ip = instance['PublicIpAddress']\
            if 'PublicIpAddress' in instance else None
        self.vpc_id = instance['VpcId'] if 'VpcId' in instance else None
        self.priv_ipv4 = [
            address['PrivateIpAddress']
            for interface in instance['NetworkInterfaces']
            for address in interface['PrivateIpAddresses']
        ]
        self.priv_ipv6 = [
            address for
            interface in instance['NetworkInterfaces']
            for address in interface['Ipv6Addresses']
        ]
