import re
import os

class Tools(object):
    def subnet(self, address, segment):
        from ipaddress import ip_network
        try:
            return ip_network(address).subnet_of(ip_network(segment))
        except BaseException:
            return False

    def ipget(self):
        from psutil import net_if_addrs
        self.ip = set(j[1] for i in net_if_addrs().values() for j in i if (j[0] == 2 or j[0] == 10) and j[1] != '127.0.0.1' and j[1] != '::1' and not '%' in j[1])

    def excel(self, file, table):
        from openpyxl import load_workbook
        self.error = None
        try:
            self.data = load_workbook(file, read_only=True)[table].values
        except BaseException as e:
            self.error = e

    def query(self, service, qname, rdtype=1, tcp=False, source=None, lifetime=None):
        from dns.resolver import Resolver
        self.error = None
        self.dns = Resolver()
        self.dns.nameservers = [service]
        try:
            begin = self.dns.query(qname, rdtype=rdtype, tcp=tcp, source=source, raise_on_no_answer=False,
                                   lifetime=lifetime)
            self.ttl = begin.rrset.ttl
            self.answer = tuple(i.to_text() for i in begin.response.answer)
            self.result = self.answer[-1]
            print(self.result)
            self.short = tuple(''.join(i.split(' ', 4)[4:]) for i in self.result.split('\n'))
            print(self.short)
        except BaseException as e:
            print(e)
            self.error = e
            
    def yrdns_query(self, service, qname, rdtype=1, tcp=False, source=None, lifetime=None, subnet=None, norecurse=0, mask=24):
        import clientsubnetoption
        if not subnet is None:
            import dns
            cso = clientsubnetoption.ClientSubnetOption(subnet, bits=mask)
            message = dns.message.make_query(qname, rdtype)
            if norecurse == 1:
                message.flags = 0x20
            message.use_edns(options=[cso])
            r = dns.query.udp(message, service[0])
            answer = [i.to_text() for i in r.answer]
            self.answer = list()
            for i in answer:
                self.answer += i.split('\n')
                
            authority = [i.to_text() for i in r.authority]
            self.authority = list()
            for i in authority:
                self.authority += i.split('\n')
            
            additional = [i.to_text() for i in r.additional]
            self.additional = list()
            for i in additional:
                self.additional += i.split('\n')
            self.rcode = r.rcode()
        else:
            from dns.resolver import Resolver
            from dns.resolver import NXDOMAIN, NoAnswer
            self.error = None
            self.dns = Resolver()
            self.dns.nameservers = service
            self.YRerror = ''
            if norecurse == 1:
                self.dns.set_flags = 0x20
            try:
                begin = self.dns.query(qname, rdtype=rdtype, tcp=tcp, source=source, raise_on_no_answer=False, lifetime=lifetime)
                self.ttl = begin.rrset.ttl
                answer = tuple(i.to_text() for i in begin.response.answer)
                self.result = answer[-1]
                self.short = tuple(''.join(i.split(' ', 4)[4:]) for i in self.result.split('\n'))
                
                self.answer = list()
                for i in answer:
                    self.answer += i.split('\n')
                print(self.answer)
                
                authority = tuple(i.to_text() for i in begin.response.authority)
                self.authority = list()
                for i in authority:
                    self.authority += i.split('\n')

                additional = tuple(i.to_text() for i in begin.response.additional)
                self.additional = list()
                for i in additional:
                    self.additional += i.split('\n')
            except NXDOMAIN:
                self.YRerror = 'NXDOMAIN'
            except NoAnswer:
                self.YRerror = 'NoAnswer'
            except BaseException as e:
                self.error = e


    def querya(self,qname):
        from dns.resolver import Resolver
        self.dns = Resolver()
        self.dns.nameservers = "192.168.6.211"
        try:
            begin = self.dns.query(qname)
            self.ttl = begin.rrset.ttl
            self.answer = tuple(i.to_text() for i in begin.response.answer)
            self.result = self.answer[-1]
            print(self.result)
            self.short = tuple(''.join(i.split(' ', 4)[4:]) for i in self.result.split('\n'))
            print(self.short)
        except BaseException as e:
            self.error = e
            print(self.error)

