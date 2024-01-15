import argparse
from crawler import sub_comment_crawler

import config


def main():
    # define command line params ...
    parser = argparse.ArgumentParser(description='Bili sub-comments crawler program.')
    parser.add_argument('-i', type=str, help='Input file)', default=config.INPUT_CSV_NAME)
    parser.add_argument('-o', type=str, help='Output file name', default=config.OUTPUT_CSV_NAME)
    parser.add_argument('-cookie', type=str, help='Bili cookie', default=config.COOKIE)

    args = parser.parse_args()

    sub_comment_crawler(args.i, args.o, args.cookie)

if __name__ == '__main__':
    main()