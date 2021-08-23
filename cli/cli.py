from cli.filter import AccountFilter, DestFilter, PortFilter, ProtocolFilter, RegionFilter, SourceFilter


class CLI:
    def __init__(self, **kwargs) -> None:
        if kwargs.get('subcommand', None) is 'diff':
            pass
        else:
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
            self.cloudQuery = kwargs.get('cloudQuery', None)

            self.filters = {}
            # acct, reg, src, dst, port, protocol
            self.filters['account'] = AccountFilter(desired_vals=[acct.strip(' ') for acct in self.acctString.split(
                ',')] if self.acctString != None else [], inclusive='!' in self.acctString if self.acctString != None else False)
            self.filters['region'] = RegionFilter(desired_vals=[reg.strip(' ') for reg in self.regString.split(
                ',')] if self.regString != None else [], inclusive='!' in self.regString if self.regString != None else False)
            self.filters['source'] = SourceFilter(desired_vals=[src.strip(' ') for src in self.srcString.split(
                ',')] if self.srcString != None else [], inclusive='!' in self.srcString if self.srcString != None else False)
            self.filters['dest'] = DestFilter(desired_vals=[dst.strip(' ') for dst in self.dstString.split(
                ',')] if self.dstString != None else [], inclusive='!' in self.dstString if self.dstString != None else False)
            self.filters['port'] = PortFilter(desired_vals=[port.strip(' ') for port in self.portString.split(
                ',')] if self.portString != None else [], inclusive='!' in self.portString if self.portString != None else False)
            self.filters['protocol'] = ProtocolFilter(desired_vals=[protocol.strip(' ') for protocol in self.protocolString.split(
                ',')] if self.protocolString != None else [], inclusive='!' in self.protocolString if self.protocolString != None else False)

    def buildQuery(self):
        if self.cloudQuery is not None:
            return self.cloudQuery
        returnString = ""
        if len(self.filters['source'].desired_vals) > 0:
            returnString += "| filter ("
            for source in self.filters['source'].desired_vals:
                returnString += f"pkt_srcaddr = \"{source}\" or "
            returnString = returnString.rstrip(' or ')
            returnString += ')'
        if len(self.filters['dest'].desired_vals) > 0:
            returnString += " and (" if returnString != "" else "| filter ("
            for dest in self.filters['dest'].desired_vals:
                returnString += f"pkt_dstaddr = \"{dest}\" or "
            returnString = returnString.rstrip(' or ')
            returnString += ')'
        if len(self.filters['port'].desired_vals) > 0:
            returnString += " and (" if returnString != "" else "| filter ("
            for port in self.filters['port'].desired_vals:
                returnString += f"srcport = {port} or "
            returnString = returnString.rstrip(' or ')
            returnString += ')'
            returnString += " and (" if returnString != "" else "| filter ("
            for port in self.filters['port'].desired_vals:
                returnString += f"dstport = {port} or "
            returnString = returnString.rstrip(' or ')
            returnString += ')'
        if len(self.filters['protocol'].desired_vals) > 0:
            returnString += " and (" if returnString != "" else "| filter ("
            for protocol in self.filters['protocol'].desired_vals:
                returnString += f"protocol = {protocol} or "
            returnString = returnString.rstrip(' or ')
            returnString += ')'
        return returnString
