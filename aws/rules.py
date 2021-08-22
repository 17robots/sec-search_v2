from .searchstrings import SearchFilters


def grab_sec_group_rules(client):
    rules = []
    for val in client.get_paginator('describe_security_group_rules').paginate(
            PaginationConfig={'PageSize': 1000}).search(SearchFilters.rules.value):
        rules.append(val)
    return rules
