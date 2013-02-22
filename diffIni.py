#!/usr/bin/env python

import os
import re
import subprocess
import logging
import optparse
from ConfigParser import ConfigParser

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def main():
    usage = "usage: %prog [-h|--help] -i|--ini file -d|--dist file"
    parser = optparse.OptionParser(usage, version="%prog 0.1")
    parser.add_option("-i", "--ini", dest="origin",
                      help="Votre fichier INI", metavar="FILE")
    parser.add_option("-d", "--dist", dest="dist",
                      help="Votre fichier modele (.dist)", metavar="FILE")
    options, args = parser.parse_args()
    if not options.origin or not options.dist :
      parser.error("incorrect number of arguments")

    parser = ConfigParser()
    parser.optionxform = str
    parser.read(options.origin)
    sections = parser.sections()
    items = parser.items(sections[0])
    keysA = []
    for key, val in items: keysA.append(key)
    keysA = set(keysA)

    parser = ConfigParser()
    parser.optionxform = str
    parser.read(options.dist)
    sections = parser.sections()
    items = parser.items(sections[0])
    keysB = []
    for key, val in items: keysB.append(key)
    keysB = set(keysB)
 
    print bcolors.WARNING + "\nClefs obsoletes:\n" + bcolors.ENDC
    obsolets = keysA - keysB
    for key in obsolets : print "\t" + key
    print bcolors.OKGREEN + "\nNouvelles clefs:\n" + bcolors.ENDC
    news = keysB - keysA
    for key in news : print "\t" + bcolors.OKBLUE + key + bcolors.ENDC + " : " + parser.get(sections[0], key)
    print "\n"

if __name__ == "__main__":
    main()
