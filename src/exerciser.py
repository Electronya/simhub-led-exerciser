#!/usr/bin/env python

import argparse

import simhub as sh


def main() -> None:
    """
    Application main.
    """
    parser = argparse.ArgumentParser(prog='SimHub LED Exerciser',
                                     description='SimHub LED protocol packet generator.')   # noqa: E501
    parser.add_argument('port', help='The serial port device to use,')
    parser.add_argument('command',
                        choices=['unlock', 'proto', 'count', 'generate'],
                        help='The SimHub protocol exerciser command.')
    parser.add_argument('-c', '--count', type=int,
                        help='The LED count for the generation.')
    parser.add_argument('-i', '--iterations', type=int,
                        help='The number of iteration of data generation.')
    args = parser.parse_args()
    try:
        if args.command == 'unlock':
            print(sh.unlockUpload(args.port))
        elif args.command == 'proto':
            print(sh.getProtoVersion(args.port))
        elif args.command == 'count':
            print(sh.getLedCount(args.port))
        elif args.command == 'generate':
            if args.count is None and args.iterations is None:
                parser.print_help()
            else:
                sh.generatedLedData(args.port, args.count, args.iterations)
    except Exception as e:
        parser.error(str(e))


if __name__ == "__main__":
    main()
