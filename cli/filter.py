
import ipaddress


class Filter:
    def __init__(self, desired_vals, inclusive) -> None:
        self.desired_vals = desired_vals
        self.inclusive = inclusive

    def allow(self, item):
        pass


class RegionFilter(Filter):
    def allow(self, region):
        if self.desired_vals == None or len(self.desired_vals) == 0:
            return True
        return region in self.desired_vals


class AccountFilter(Filter):
    def allow(self, account):
        if self.desired_vals == None or len(self.desired_vals) == 0:
            return True
        return account['accountId'] in self.desired_vals


class SourceFilter(Filter):
    def allow(self, rule):
        if self.desired_vals == None or len(self.desired_vals) == 0:
            return True
        rules = expand_rule(rule=rule)
        for expanded_rule in rules:
            if self.inclusive:
                for val in self.desired_vals:
                    try:
                        x = ipaddress.ip_network(val)
                        y = ipaddress.ip_network(expanded_rule.source)
                        if x.subnet_of(y):
                            return True
                        if y.subnet_of(x):
                            return True
                        if val in expanded_rule.source:
                            return True
                        if expanded_rule.source in val:
                            return True
                        return False
                    except:
                        continue
                return True
            else:
                for val in self.desired_vals:
                    try:
                        x = ipaddress.ip_network(val)
                        y = ipaddress.ip_network(expanded_rule.source)
                        if x.subnet_of(y):
                            return False
                        if y.subnet_of(x):
                            return False
                        if val in expanded_rule.source:
                            return False
                        if expanded_rule.source in val:
                            return False
                        return True
                    except:
                        continue
                return False


class DestFilter(Filter):
    def allow(self, rule):
        if self.desired_vals == None or len(self.desired_vals) == 0:
            return True
        rules = expand_rule(rule=rule)
        for expanded_rule in rules:
            if self.inclusive:
                for val in self.desired_vals:
                    try:
                        x = ipaddress.ip_network(val)
                        y = ipaddress.ip_network(expanded_rule.dest)
                        if x.subnet_of(y):
                            return True
                        if y.subnet_of(x):
                            return True
                        if val in expanded_rule.dest:
                            return True
                        if expanded_rule.dest in val:
                            return True
                        return False
                    except:
                        continue
                return True
            else:
                for val in self.desired_vals:
                    try:
                        x = ipaddress.ip_network(val)
                        y = ipaddress.ip_network(expanded_rule.dest)
                        if x.subnet_of(y):
                            return False
                        if y.subnet_of(x):
                            return False
                        if val in expanded_rule.dest:
                            return False
                        if expanded_rule.dest in val:
                            return False
                        return True
                    except:
                        continue
                return False


class PortFilter(Filter):
    def allow(self, rule):
        if self.desired_vals == None or len(self.desired_vals) == 0:
            return True
        if self.inclusive:
            for val in self.desired_vals:
                if int(val) == int(rule['from']):
                    return True
                if int(val) == int(rule['to']):
                    return True
                return False
        else:
            for val in self.desired_vals:
                if int(val) == int(rule['from']):
                    return False
                if int(val) == int(rule['to']):
                    return False
                return True


class ProtocolFilter(Filter):
    def allow(self, rule):
        if self.desired_vals == None or len(self.desired_vals) == 0:
            return True
        if self.inclusive:
            for val in self.desired_vals:
                if val in rule['protocol']:
                    return True
                return False
        else:
            for val in self.desired_vals:
                if val in rule['protocol']:
                    return False
                return True


def expand_rule(rule):
    pass
