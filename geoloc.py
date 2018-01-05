#!/usr/bin/env python

##
##  DEPENDENCIES
##
##  geoip2
##
##      pip install geoip2
##
##  maxmind GeoLiteCity
##      http://www.maxmind.com/
##      download ... decompress
##

class Args(object):
    ##
    ## Argument parser
    ##
    import argparse

    parser = argparse.ArgumentParser(description='Use Python to Geolocate IP addresses')

    parser.add_argument(
        '--ipfile', '-i', '-ipfile',
        metavar='[IPFILE]', 
        dest='ipfile', 
        nargs=1, 
        required=True,
        default=None,
        help='File containing IP addresses'
    ) 

    parser.add_argument(
        '--geodb', '-g', '-geodb',
        metavar='[GEODB]', 
        dest='geodb', 
        nargs=1, 
        required=True,
        default=None,
        help='GeoIP Database'
    ) 

    def print_help(self):
        self.parser.print_help()
        return

    def parse(self):
        args = self.parser.parse_args()
        return args


def parse_geoip(ipfile, geodb):
    import os
    import geoip2.database

    geopath = os.path.join(os.getcwd(), geodb)
    reader = geoip2.database.Reader(geopath)

    ippath = os.path.join(os.getcwd(), ipfile)
    with open(ippath, 'r') as f:
        for ip in f:
            try:
                rec = reader.city(ip.strip())
                lat = rec.location.latitude
                lon = rec.location.longitude
                print('%s:%s:%s'%(ip.strip(), lat, lon))
            except Exception, e:
                pass


if __name__ == '__main__':

    a = Args()
    args = a.parse()

    if args.ipfile:
        ipfile = args.ipfile[0]
    else:
        ipfile = False

    if args.geodb:
        geodb = args.geodb[0]
    else:
        geodb = False

    if ipfile and geodb:
        parse_geoip(ipfile, geodb)



