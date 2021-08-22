from aws.searchstrings import SearchFilters


def grab_flow_logs(client):
    paginator = client.get_paginator(
        'describe_flow_logs').paginate().search(SearchFilters.logs.value)

    return [val for val in paginator]
