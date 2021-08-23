from .searchstrings import SearchFilters


def grab_sec_group_rules(client):
    rules = []
    paginator = client.get_paginator('describe_security_group_rules').paginate(
        PaginationConfig={'PageSize': 1000}).search(SearchFilters.rules.value)
    for val in paginator:
        rules.append(val)
    return rules
