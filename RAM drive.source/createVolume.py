#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re
import sys
import argparse
import os
import plistlib
import StringIO
from xml.parsers.expat import ExpatError
from subprocess import Popen, PIPE

INFO_FIELD_MAP = {
    'DeviceNode':       {'name': 'Device', 'value': lambda x: str(x)},
    'FilesystemName':   {'name': 'Filesystem', 'value': lambda x: str(x)},
    'UsedSpace':        {'name': 'Used', 'value': lambda x: x/1024},
    'UsedPercent':      {'name': 'Percent', 'value': lambda x: x/1024},
    'FreeSpace':        {'name': 'Free', 'value': lambda x: x/1024},
    'TotalSize':        {'name': 'Sizd', 'value': lambda x: x/1024},
    'VolumeName':       {'name': 'Volume Name', 'value': lambda x: str(x)},
    'VolumeUUID':       {'name': 'UUID', 'value': lambda x: str(x)},
}
INFO_FIELD_ORDER = [
    'DeviceNode',
    'VolumeName',
    'FilesystemName',
    'VolumeUUID',
    'UsedSpace',
    'FreeSpace',
    'TotalSize'
]

class DiskUtilError(Exception):
    pass

class DiskInfo(dict):
    def __init__(self, device):
        if not os.access(device, os.R_OK):
            raise DiskUtilError('Device not readable: %s' % device)

        cmd = ['diskutil', 'info', '-plist', device]
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = p.communicate()
        try:
            plist = StringIO.StringIO(stdout)
            self.update(plistlib.readPlist(plist))
        except ExpatError, emsg:
            raise DiskUtilError('Error parsing plist: %s' % stdout)

        if self.has_key('TotalSize') and self.has_key('FreeSpace'):
            self['UsedSpace'] = self.TotalSize - self.FreeSpace
            self['UsedPercent'] = int(round(1-(float(self.FreeSpace) / float(self.TotalSize))))

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError

    def keys(self):
        """
        Return keys as sorted list
        """
        return sorted(dict.keys(self))

    def items(self):
        """
        Return (key, value) sorted by key
        """
        return [(k, self[k]) for k in self.keys()]

    def values(self):
        """
        Return values sorted by key
        """
        return [self[k] for k in self.keys()]


def createVolume(inputSize, inputFilesystem):
    filesystemsList = listFilesystems()
    if inputFilesystem.strip() not in filesystemsList:
        print "%s does not appear to be a valid file system format" % inputFilesystem
        sys.exit(1)

    getSize = inputSize.lower()
    value = re.findall('\d+', getSize)
    digitValue = lambda nums: int(''.join(str(i) for i in value))

    if getSize.isdigit():
        getSize = ("ram://%s") % getSize
    elif re.findall('m', getSize):
        getSize = ("ram://%s") % str(digitValue(value) * 2048)
    elif re.findall('g', getSize):
        getSize = ("ram://%s") % str(digitValue(value) * 1024 * 2048)
    else:
        print "Not found"
        sys.exit('Unable to convert %s' % inputSize )

    cmd_create = ["/usr/bin/hdiutil", "attach", "-nomount", getSize]
    proc = subprocess.Popen(cmd_create, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, error_output) = proc.communicate()
    blockDevice = output.split('\n')
    blockDevice = " ".join(blockDevice).strip()

    cmd_format = ["/usr/sbin/diskutil", "eraseVolume", inputFilesystem.strip(), "VOLINRAM", blockDevice]
    #subprocess.call(cmd_format)
    proc = subprocess.Popen(cmd_format, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, error_output) = proc.communicate()

    print DiskInfo(blockDevice).MountPoint
    return DiskInfo(blockDevice).MountPoint


def listFilesystems():
    cmd_list_fs = ["/usr/sbin/diskutil", "listFilesystems"]
    proc = subprocess.Popen(cmd_list_fs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
    return listFilesystems

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--volumeSize', action="store", help='Enter volumeSize')
    parser.add_argument('--filesystemType', action="store", help='Enter filesystemType')
    parser.parse_args()
    volumeSize = parser.parse_args().volumeSize
    filesystemType = parser.parse_args().filesystemType
    createVolume(volumeSize, filesystemType)


if __name__ == '__main__':
    main()
