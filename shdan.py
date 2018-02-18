#!/usr/bin/env python

##
##  DEPENDENCIES
##
##  shodan
##
##      https://pypi.python.org/pypi/shodan
##      download ... extract
##      python setup.py install
##

class Args(object):
    ##
    ## Argument parser
    ##
    import argparse

    parser = argparse.ArgumentParser(description='Parsing Shodan info by hostname in Python')

    parser.add_argument(
        '--hostsfile', '--hosts',
        metavar='[HOSTS]', 
        dest='hosts', 
        nargs=1, 
        required=True,
        default=None,
        help='Hosts File to parse'
    ) 

    def print_help(self):
        self.parser.print_help()
        return

    def parse(self):
        args = self.parser.parse_args()
        return args


def parse_shodan(hosts):
    import os
    import re
    import time
    from shodan import Shodan
    SHODAN_API_KEY = "API-KEY-HERE"
    api = Shodan(SHODAN_API_KEY)

    info = {}
    path = os.path.join(os.getcwd(), hosts)
    with open(path, 'r') as f:
        for line in f:
            l = line.strip()
            try:
                results = api.search(l)

                for r in results['matches']:

                    if 'hostnames' in r.keys():
                        print 'HOSTS: %s : %s'%(r['ip_str'], r['hostnames'])

                    for m in r['data'].split('\n'):
                        match = re.match('^Server: (.*)$', m)
                        if match:
                            ##
                            ## <ip>:<server striing>
                            ##
                            print 'SERVER: %s:%s'%(r['ip_str'], match.group(1))

            except Exception, e:
                ##
                ## connection timeouts cause exeptions
                ##
                pass

            ##
            ## shodan API is limited to 1 req per second
            ##
            time.sleep(2)


if __name__ == '__main__':

    a = Args()
    args = a.parse()

    if args.hosts:
        parse_shodan(args.hosts[0])

