#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re
import sys

cmd = ["/usr/sbin/diskutil", "listFilesystems"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(output, error_output) = proc.communicate()
output = output.split('\n')[9:]

listFilesystems = []
for row in output:
  row = row.strip()
  match = re.search("\(or\)", row, re.I | re.S | re.M)
  if match or row == "" or row[0] == "Free Space":
    continue
  row = row.split('  ')
  #print row[0]
  listFilesystems.append(row[0])

ds = sys.argv[1]

result = ""
result += "<?xml version=\"1.0\"?><items>\n"
for fs in listFilesystems:
  result += "<item uid=\"%s\" arg=\"%s %s\"><title>%s - %s</title>\n" % (ds, ds, fs, ds, fs)
  result += "<subtitle>Choose filesystem to format RAMdirve</subtitle>\n"
  result += "<icon>icon.png</icon><valid>yes</valid></item>\n"
result += "</items>"

print result