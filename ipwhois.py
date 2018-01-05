#!/usr/bin/env python

##
## Team Cymru ASN lookup
##

##
## Team Cymru is not suggesting that the only netcat
## variant that works w/ their IP->ASN lookup is
## the GNU version ... I've tested w/ ncat and nc, no worky
##
## ... for what it's worth, I wouldn't use global variables 
##     if this weren't such a simple one-off
##
global NCMD
NCMD = 'netcat'

class Args(object):
    ##
    ## Argument parser
    ##
    import argparse

    parser = argparse.ArgumentParser(description='Use Python to query Team Cymru whois service')

    parser.add_argument(
        '--ipfile', '-i', '-ipfile',
        metavar='[IPFILE]', 
        dest='ipfile', 
        nargs=1, 
        required=True,
        default=None,
        help='File containing IP addresses'
    ) 

    def print_help(self):
        self.parser.print_help()
        return

    def parse(self):
        args = self.parser.parse_args()
        return args



def parse_whois(ipfile):

    import os
    import subprocess

    ##
    ## Effectively run the command:
    ##
    ##  netcat whois.cymru.com 43 < list01 | sort -n > list02 
    ##

    cmd = [
        NCMD,
        'whois.cymru.com', 
        '43'
    ]

    path = os.path.join(os.getcwd(), ipfile)
    with open(path, 'r') as f:
        input = f.read()

        try:
            pipe = subprocess.Popen(
                cmd, 
                shell=False,
                cwd=None,
                stdout = subprocess.PIPE,
                stdin = subprocess.PIPE,
                stderr = subprocess.PIPE
            )

            (out, error) = pipe.communicate(input)

            print('OUT: %s, ERR: %s'%(out, error))

        except Exception, e:
            print(e)

if __name__ == '__main__':

    a = Args()
    args = a.parse()

    if args.ipfile:
        parse_whois(args.ipfile[0])


