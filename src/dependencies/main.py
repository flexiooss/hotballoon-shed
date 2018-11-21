#!/usr/bin/python

import re
import sys, getopt
from packageHandler import getDependancies, builtDependanciesModules, postJson, process


def main(argv):
    inputfile = ''
    url = ''
    repository_id = ''

    try:
        opts, args = getopt.getopt(argv, "hi:u:r:", ["help", "ifile=", "url=", "repository_id="])
    except getopt.GetoptError:
        print 'packageHandler.py -i <inputfile> -u <url> -r <repository_id>'
        sys.exit(2)

    for opt, arg in opts:
        arg = re.sub('[\s+]', '', arg)
        if opt in ("-h", "--help"):
            print 'packageHandler.py -i <inputfile> -u <url> -r <repository_id>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-r", "--repository_id"):
            repository_id = arg

    process(inputfile, url, repository_id)


if __name__ == "__main__":
    main(sys.argv[1:])
