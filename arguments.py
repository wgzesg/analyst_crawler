import argparse
from ast import arg

def get_parser():
    parser = argparse.ArgumentParser(description='Crawl researcher reports')
    parser.add_argument('-u', '--url',
                        help='stock report collection url')
    parser.add_argument('-o',  '--out',
                        help='output json file name')
    return parser