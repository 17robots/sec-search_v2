from cli.filter import AccountFilter, DestFilter, PortFilter, ProtocolFilter, RegionFilter, SourceFilter


class CLI:
    def __init__(self, **kwargs) -> None:
        # grab args
        self.acctString = kwargs.get('accounts', None)
        self.regString = kwargs.get('regions', None)
        self.srcString = kwargs.get('sources', None)
        self.dstString = kwargs.get('dests', None)
        self.portString = kwargs.get('ports', None)
        self.protocolString = kwargs.get('protocols', None)
        self.queryString = kwargs.get('query', None)
        self.dispString = kwargs.get('display', None)
        self.outString = kwargs.get('output', None)

        self.filters = {}
        # acct, reg, src, dst, port, protocol
        self.filters['account'] = AccountFilter(desired_vals=[acct.strip(' ') for acct in self.acctString.split(
            ',')] if self.acctString != None else [], inclusive='!' in self.acctString)
        self.filters['region'] = RegionFilter(desired_vals=[reg.strip(' ') for reg in self.regString.split(
            ',')] if self.regString != None else [], inclusive='!' in self.regString)
        self.filters['source'] = SourceFilter(desired_vals=[src.strip(' ') for src in self.srcString.split(
            ',')] if self.srcString != None else [], inclusive='!' in self.srcString)
        self.filters['dest'] = DestFilter(desired_vals=[dst.strip(' ') for dst in self.dstString.split(
            ',')] if self.dstString != None else [], inclusive='!' in self.dstString)
        self.filters['port'] = PortFilter(desired_vals=[port.strip(' ') for port in self.portString.split(
            ',')] if self.portString != None else [], inclusive='!' in self.portString)
        self.filters['protocol'] = ProtocolFilter(desired_vals=[protocol.strip(' ') for protocol in self.protocolString.split(
            ',')] if self.protocolString != None else [], inclusive='!' in self.protocolString)
