#!/usr/bin/env python

##
##  DEPENDENCIES
##
##  pywhois
##
##      pip install python-whois
##

class Args(object):
    ##
    ## Argument parser
    ##
    import argparse

    parser = argparse.ArgumentParser(description='Parsing whois by hostname in Python')

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


def parse_hostwhois(hosts):
    import os
    import whois

    path = os.path.join(os.getcwd(), hosts)
    with open(path, 'r') as f:
        for line in f:

            try:
                w = whois.whois(line.strip().lower())

                updated_date =  w['updated_date']
                status = w['status']
                name = w['name']
                dnssec = w['dnssec']
                city = w['city']
                expiration_date = w['expiration_date']
                zipcode = w['zipcode']
                domain_name = w['domain_name']
                country = w['country']
                whois_server = w['whois_server']
                state = w['state']
                registrar = w['registrar']
                referral_url = w['referral_url']
                address = w['address']
                name_servers = w['name_servers']
                org = w['org']
                creation_date = w['creation_date']
                emails = w['emails']

                print('%s : %s : %s'%(emails, name, name_servers))

            except Exception, e:
                pass


if __name__ == '__main__':

    a = Args()
    args = a.parse()

    if args.hosts:
        parse_hostwhois(args.hosts[0])

