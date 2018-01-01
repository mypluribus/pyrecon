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

class Args(object):
    ##
    ## Argument parser
    ##
    import argparse

    parser = argparse.ArgumentParser(description='Python PCAP parsing')

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


def parse_pcap(pcap_file):

    path = os.path.join(os.getcwd(), pcap_file)
    try:
        with open(path, 'r') as f:
            pcap = dpkt.pcap.Reader(f)

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

                        ##
                        ## <frag ID>:<src IP>:<dst IP>
                        ##
                        print '%s:%s:%s'%(ip.id, ip_src, ip_dst) 

                except Exception, e:
                    pass

    except Exception, e:
        pass


if __name__ == '__main__':

    import os
    import socket
    import dpkt

    a = Args()
    args = a.parse()

    if args.pcap:
        parse_pcap(args.pcap[0])

