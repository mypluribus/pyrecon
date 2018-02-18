#!/usr/bin/env python

##
##  DEPENDENCIES
##
##  dpkt
##
##      https://pypi.python.org/pypi/dpkt
##
##  dnslib
##
##      https://pypi.python.org/pypi/dnslib
##


class Args(object):
    ##
    ## Argument parser
    ##
    import argparse

    parser = argparse.ArgumentParser(description='Parsing DNS requests in Python')

    parser.add_argument(
        '--pcap', '-p', '--pcap',
        metavar='[PCAP]', 
        dest='pcap', 
        nargs=1, 
        required=True,
        default=None,
        help='PCAP File to parse'
    ) 

    def print_help(self):
        self.parser.print_help()
        return

    def parse(self):
        args = self.parser.parse_args()
        return args


def parse_dns(pcap_file):
    import os
    import socket
    import dpkt
    from dnslib import DNSRecord

    path = os.path.join(os.getcwd(), pcap_file)
    f = open(path)
    pcap = dpkt.pcap.Reader(f)

    hosts = None

    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type == 2048:
                ##
                ## IP Packet
                ##
                ip = eth.data
                ip_src = socket.inet_ntoa(ip.src)
                ip_dst = socket.inet_ntoa(ip.dst)
                if ip.p == 17:
                    ##
                    ## UDP
                    ##
                    udp = ip.data
                    if udp.dport == 53 or udp.sport == 53 and len(udp.data) > 0:
                        ##
                        ## DNS request or response
                        ##
                        dns = DNSRecord.parse(udp.data)

                        ##
                        ## DNS Query (also present in response)
                        ##

                        if dns.q:
                            query = {}
                            query['qname'] = str(dns.q.qname)

                            if hosts is None:
                                hosts = set({})

                            hosts.add(query['qname'].rstrip('.'))

                            query['qtype'] = dns.q.qtype
                            query['qclass'] = dns.q.qclass
                            print 'QUERY:%s:%s:%s:%s:%s'%(
                                ip_src, 
                                ip_dst, 
                                query['qname'], 
                                query['qtype'], 
                                query['qclass']
                            )


                        ##
                        ## DNS RESPONSE
                        ##

                        if dns.rr:
                            r = {}
                            for rr in dns.rr:
                                r['rname'] = str(rr.rname)
                                r['rtype'] = rr.rtype
                                r['rclass'] = rr.rclass
                                r['rttl'] = rr.ttl

                                ##
                                ## rdata contains IP or cname
                                ##
                                r['rdata'] = str(rr.rdata)

                                ##
                                ## 1 = A (Alias)
                                ## 5 = CN (CNAME)
                                ## 15 = MX (Mail Exchange)
                                ## 2 = NS (Name Server)
                                ##

                                if r['rtype'] == 5:
                                    print query['qname']
                                    print r['rdata']

                                print 'RESPONSE:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s'%(
                                    ip_src, 
                                    ip_dst, 
                                    query['qname'], 
                                    query['qtype'], 
                                    query['qclass'],
                                    r['rname'],
                                    r['rtype'],
                                    r['rclass'],
                                    r['rttl'],
                                    r['rdata']
                                )
                        
        except Exception, e:
            print e
            pass


    for host in hosts:
        print('HOST: %s'%host)



if __name__ == '__main__':

    a = Args()
    args = a.parse()

    if args.pcap:
        parse_dns(args.pcap[0])


