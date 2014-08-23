#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Pavel Miroshnichenko"
__email__ = "facetheheat@icloud.com"

import sys
import subprocess
import re

#Create unsorted output from disk utility
#skips first 9 lines of the output
cmd = ["/usr/sbin/diskutil", "listFilesystems"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(output, error_output) = proc.communicate()
output = output.split('\n')[9:]

#Create list of filesystems
listFilesystems = []
for row in output:
    row = row.strip()
    match = re.search("\(or\)", row, re.I | re.S | re.M)
    if match or row == "":
        continue
    row = row.split('  ')
    if row[0] == 'Free Space':
        continue
    listFilesystems.append(row[0])

#Get size of the filesystem as argument in Blocks/Mb/Gb
if len(sys.argv) > 1:
    ds = sys.argv[1]
else:
    sys.exit('Usage: %s FILESIZE (Blocks/Mb/Gb) ' % sys.argv[0])

#Print the result to alfred window
result = ""
result += "<?xml version=\"1.0\"?><items>\n"
for fs in listFilesystems:
    if fs == 'MS-DOS' or fs == 'MS-DOS FAT32' or fs == 'MS-DOS FAT12' or fs == 'MS-DOS FAT16':
        fsIcon='icons/fat.png'
    elif fs == 'ExFAT':
        fsIcon='icons/exfat.png'
    elif fs == 'UFSD_NTFS' or fs == 'UFSD_NTFSCOMPR':
        fsIcon='icons/ntfs.png'
    elif fs == 'UFSD_EXTFS':
        fsIcon='icons/extfs.png'
    elif fs == 'HFS+' or fs == 'Journaled HFS+' or 'Case-sensitive HFS+' or 'Case-sensitive Journaled HFS+':
        fsIcon='icons/hfs.png'
    else:
        fsIcon='icons/default.png'
    result += "<item uid=\"%s\" arg=\"%s %s\"><title>%s - %s</title>\n" % (ds, ds, fs, ds, fs)
    result += "<subtitle>Create %s %s RAM Drive</subtitle>\n" % (ds, fs)
    result += "<icon>%s</icon><valid>yes</valid></item>\n" % fsIcon
result += "</items>"
print result
