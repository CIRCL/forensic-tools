#
#   scm-timeline Create timeline from windows services that are started/stopped   
#
#   Copyright (C) 2015  Gerard Wagener
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import xml.sax
import sys
from unidecode import unidecode
import argparse
import sys

class Parser(xml.sax.ContentHandler):
    def __init__(self):
        self.currentdate = ""
        self.isSCM = False
        self.msg = []
        self.hasdata = False

    def startElement(self, name, attrs):
        if name == "TimeCreated":
             for (k,v) in attrs.items():
                self.currentdate = v
        if name == "Provider":
            for (k,v) in attrs.items():
                if k.startswith("EventSourceName"):
                    if v.startswith("Service Control Manager"):
                        self.isSCM = True 
        if name == "Data":
            for (k,v) in attrs.items():
                self.hasdata = True

    def characters(self,content):
        if self.isSCM == True and self.hasdata == True:
            if len(content) > 1:
                self.msg.append(unidecode(content))
                self.hasdata =  True

    def endElement(self,name):
        if name == "Event":
            if len(self.msg) > 1:
                print self.currentdate,"|"," ".join(self.msg)
            #Reset states
            self.currentdate = ""
            self.isSCM = False
            self.msg = []
            self.hasdata = False 
        if name == "Data":
            self.hasdata = False

cli = argparse.ArgumentParser(description='Take XML ouput from evtxdump.pl and create  a timeline of events when which services started / stopped. The System event file should be parsed prior with evtxdump.pl.')
cli.add_argument('--filename', type=str, nargs=1, help='Filename that should be processed')

args = cli.parse_args()

if args.filename is None:
    sys.stderr.write("An XML export done by evtxdump.pl of Sytem.evtx must be specified\n")
    sys.exit(1)

parser = xml.sax.make_parser()
parser.setContentHandler(Parser())
parser.parse(open(args.filename[0],"r"))
