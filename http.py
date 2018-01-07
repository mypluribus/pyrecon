#!/usr/bin/env python

##
##  DEPENDENCIES
##
##  dpkt
##
##      http://code.google.com/p/dpkt
##      download ... decompress
##      python setup.py install
##

global PORTLIST
PORTLIST = [8080,80]

class Args(object):
    ##
    ## Argument parser
    ##
    import argparse

    parser = argparse.ArgumentParser(description='Python HTTP parsing')

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


def parse_http(pcap_file):
    import os
    import socket
    import dpkt

    path = os.path.join(os.getcwd(), pcap_file)
    f = open(path)
    pcap = dpkt.pcap.Reader(f)

    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type == 2048:
                    ##
                    ## IP Packet
                    ##
                    ip = eth.data

                    if ip.p == 6:
                        ##
                        ## TCP
                        ##
                        ip_src = socket.inet_ntoa(ip.src)
                        ip_dst = socket.inet_ntoa(ip.dst)
                        tcp = ip.data
                        if tcp.dport in PORTLIST and len(tcp.data) > 0:
                            ##
                            ## HTTP traffic
                            ##
                            try:
                                http = dpkt.http.Request(tcp.data)
                                ##
                                ## <src ip>:<dst ip>:<requested host>:<requested uri>
                                ##
                                host = str(http.headers['host'])
                                uri = str(http.uri)
                                print '%s:%s:%s:%s'%(ip_src, ip_dst, host, uri)

                            except Exception, e:
                                pass

        except Exception, e:
            pass



if __name__ == '__main__':
    a = Args()
    args = a.parse()

    if args.pcap:
        parse_http(args.pcap[0])

