#!/usr/bin/python3

#import packages
import os as os #docs: https://docs.python.org/3.4/library/os.html
import argparse #docs: https://docs.python.org/3.4/library/argparse.html













#MAIN
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='''
    Push new XML file to top of database stack and re-index old files for backup
    ''')

    #add definitions for arguments with help screen descriptions (see docs)
    parser.add_argument('path',
                        nargs='?',
                        default=os.getcwd(),
                        help='indicate directory to clean (default to working dir)')

    args = parser.parse_args() #parse the arguments passed to script
    newXMLpath = args.path
    print(newXMLpath)
