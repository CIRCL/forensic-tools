#!/usr/bin/python
#
#   evloginout.py  Create timeline when user logs in out based on eventlogs   
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
import argparse
import textwrap
from unidecode import unidecode

class EvtxHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.currentdate = ""
        self.eventid= -1
        self.inEventID = False
        self.buf = []
        self.inData = False
        self.ubuf = []
        self.inTargetUserName = False
        self.targetUserName = ""
    
        self.inTargetLogonId = False
        self.lbuf = []
        self.targetLogonId = ""

        self.inLogonType = False
        self.tbuf = []
        self.logonType = -1
        #Eventlogs are stored in this array
        self.timeline = []
        self.counter = 0

    def startElement(self, name, attrs):
        if name == "Event":
            #A new event is there reset all old states
            self.buf = []
            self.eventid = -1 
            self.currentdate = ""
            self.inData = False
            self.inTargetUserName = False
            self.ubuf = []
            self.targetUserName = ""
            self.inTargetLogonId = False
            self.lbuf = []
            self.logonType = -1
            self.inLogonType = False
            self.targetLogonId = ""

        if name == "EventID":
            self.inEventID = True

        if name == "TimeCreated":
            for (k,v) in attrs.items():
                #FIMXE always take the last one
                self.currentdate = v

        if name == "Data":
            for (k,v) in attrs.items():
                if v=="TargetUserName":
                    self.inTargetUserName = True
                if v == "TargetLogonId":
                    self.inTargetLogonId = True
                if v == "LogonType":
                    self.inLogonType = True

    def characters(self,content):
        if self.inEventID:
            self.buf.append(unidecode(content))
        if self.inTargetUserName:
            self.ubuf.append(unidecode(content))
        if self.inTargetLogonId:
            self.lbuf.append(unidecode(content))
        if self.inLogonType:
            self.tbuf.append(unidecode(content))

    def endElement(self,name):
        if name == "EventID":
            self.inEventID = False
            a = ''.join(self.buf)
            #Recover event id
            self.eventid = int(a)
            #Reset buffer
            self.buf = []

        if name == "Data":
            if self.inTargetUserName:
                self.targetUserName = ''.join(self.ubuf)
                self.ubuf = []
                self.inTargetUserName = False
            if self.inTargetLogonId:
                self.targetLogonId = ''.join(self.lbuf)
                self.lbuf = []
                self.inTargetLogonId = False
            if self.inLogonType:
                self.logonType = int(''.join(self.tbuf))
                self.tbuf = []
                self.inLogonType = False

        if name == "Event":
            logon = self.eventid
            if self.eventid == 4624:
                logon = "Success"
            if self.eventid == 4625:
                logon = "Failed"
            if self.eventid == 4634:
                logon = "Log off"

            if self.currentdate != "" and self.targetUserName != "" and self.targetLogonId != "" and self.eventid >=0 and self.logonType >=0:
                self.counter = self.counter + 1
                self.timeline.append({"date":self.currentdate, "targetUserName": self.targetUserName, "eventid":self.eventid, "targetLogonId":self.targetLogonId, "logonTypeself":self.logonType}) 
                print self.counter, "&", self.currentdate, "&", self.targetUserName, "&",logon,"&",self.targetLogonId, "&",self.logonType, "\\\\"

cli = argparse.ArgumentParser(description='Create  a timeline of logins and logouts baseed on System event files', 
epilog=textwrap.dedent('''
DESCRIPTION 
Takes the output of evtxdump.pl and create a latex table of logins and logouts.
The output is written on standard output.
'''))

cli.add_argument('--filename', type=str, nargs=1, required=True,
        help="Filename created by evtxdump.pl. The filename - specifies standard input")

args = cli.parse_args()
parser = xml.sax.make_parser()
obj = EvtxHandler()
parser.setContentHandler(obj)
#By default stdout is used
f=sys.stdin
if args.filename[0] != '-':
    f = open(args.filename[0],"r")
parser.parse(f)
