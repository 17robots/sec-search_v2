from .searchstrings import SearchFilters


def grab_instances(client):
    instances = []
    for val in client.get_paginator('describe_instances').paginate().search(
            SearchFilters.instances.value):
        for res in val:
            instances.append(res)
    return instances
