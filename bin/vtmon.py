#!/usr/bin/python
#
#   vtmon - Monitor a set of hashes to measure AV detection time   
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


import simplejson
import urllib
import urllib2
import pprint
import argparse
import textwrap
import os
import time
import syslog

url = "https://www.virustotal.com/vtapi/v2/file/report"
delay = 1


cli = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='Monitor a set of hashes at Virustotal',
        epilog=textwrap.dedent('''
        
        DESCRIPTION 

        Read all hases from the file specified by filename and do a lookup of 
        each hash at Virustotal.  The raw json documents are stored in the 
        folder results. The API key for accessing the API of virustotal should
        be specified with the key option. Errors are sent to syslog.
        '''))
cli.add_argument('--filename',  type=str, nargs=1, required=True,
        help='Filename with hashes')
cli.add_argument('--key', type=str, nargs=1, required=True,
        help='API key for accessing Virustotal')
cli.add_argument('--results', type=str, nargs=1, required=True,
        help = 'Directory where the raw json documents should be stored')

args = cli.parse_args()

#Format to store results
#result_dir/hash/year/month/day
try:
    key = args.key[0]
    key = key.replace('\n', '')
    f = open(args.filename[0],'r')
    for line in f.readlines():
        line = line.replace("\n","")
        ts = time.strftime("/%Y/%m/%d")
        res = args.results[0] + "/" + line + ts

        if os.path.exists(res) == False:
            os.makedirs(res)

        parameters = {"resource": line,
                  "apikey": key}

        fn = res + '/' + time.strftime("%Y%m%d%H%M%S")+".json"
        if os.path.exists(fn) == False:
            data = urllib.urlencode(parameters)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            json = response.read()
            g = open(fn,"w")
            g.write(json)
            g.close()
        else:
            syslog.syslog("Failed to store results. Filename already exists.")
        time.sleep(delay)
    f.close()
except OSError,e:
    syslog.syslog(str(e))
except IOError,e:
    syslog.syslog(str(e))

