#!/usr/bin/env python

class Args(object):
    ##
    ## Argument parser
    ##
    import argparse

    parser = argparse.ArgumentParser(description='Use Python to write a KML file for Google Earth')

    parser.add_argument(
        '--geodata', '-g', '-geodata',
        metavar='[GEODATA]', 
        dest='geodata', 
        nargs=1, 
        required=True,
        default=None,
        help='File containing IP:LAT:LON'
    ) 

    parser.add_argument(
        '--outfile', '-o', '-outfile',
        metavar='[OUTFILE]', 
        dest='outfile', 
        nargs=1, 
        required=True,
        default=None,
        help='Output file'
    ) 

    def print_help(self):
        self.parser.print_help()
        return

    def parse(self):
        args = self.parser.parse_args()
        return args


def write_kml(geodata, outfile):
    import os

    header = '''<?xml version='1.0' encoding='UTF-8'?>
    <kml xmlns='http://earth.google.com/kml/2.0'>
    <Folder><name>Recon Demo KML Output</name>'''

    footer = '''</Folder></kml>'''

    geopath = os.path.join(os.getcwd(), geodata)

    with open(os.path.join(os.getcwd(), outfile), 'wt') as f:
        f.write(header)
        with open(geopath, 'r') as g:
            for line in g:
                l = line.split(':')
                ip = l[0].strip()
                lat = l[1].strip()
                lon = l[2].strip()

                cdata = """
            <![CDATA[
                IP: %s<br>
                <b>GPS Coordinates</b><br>
                Avg lat/lon: %s, %s
            ]]>""" %(ip, lat, lon)

                fullstr = """
    <Placemark>
        <name>%s</name>
        <description>%s</description>
        <visibility>1</visibility>
        <open>0</open>

        <LookAt>
            <longitude>%s</longitude>
            <latitude>%s</latitude>
            <range>100</range>
            <tilt>54</tilt>
            <heading>-35</heading>
        </LookAt>

        <Point>
            <altitudeMode>clampedToGround</altitudeMode>
            <extrude>0</extrude>
            <tessellate>0</tessellate>
            <coordinates>%s,%s,0</coordinates>
        </Point>
    </Placemark>\n"""%(ip,cdata,lon,lat,lon,lat)

                f.write(fullstr)

        f.write(footer)



if __name__ == '__main__':

    a = Args()
    args = a.parse()

    if args.geodata:
        geodata = args.geodata[0]
    else:
        geodata = False

    if args.outfile:
        outfile = args.outfile[0]
    else:
        outfile = False

    if geodata and outfile:
        write_kml(geodata, outfile)
