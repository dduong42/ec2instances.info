#!/usr/bin/env python

import argparse
import json
import sys


EC2_REGIONS = [
    'ap-south-1',
    'us-east-1',
    'ap-northeast-1',
    'sa-east-1',
    'ap-northeast-2',
    'ap-southeast-1',
    'eu-west-2',
    'ca-central-1',
    'ap-southeast-2',
    'us-west-2',
    'us-gov-west-1',
    'us-west-1',
    'eu-central-1',
    'eu-west-1',
    'us-east-2',
]
PERIODS = [
     'yrTerm1Standard.partialUpfront',
     'yrTerm1Standard.allUpfront',
     'yrTerm3Standard.allUpfront',
     'yrTerm3Standard.partialUpfront',
     'yrTerm1Standard.noUpfront',
]


parser = argparse.ArgumentParser(
    description='Print ec2 pricing. Pricing data must be sent to stdin.')
parser.add_argument(
    '-r',
    '--region',
    choices=EC2_REGIONS,
    metavar='REGION',
    required=True,
)
parser.add_argument(
    '--system',
    choices=['linux', 'mswin', 'mswinSQL', 'mswinSQLWeb'],
    required=True,
)
parser.add_argument(
    '--strategy',
    choices=['ondemand', 'reserved'],
    required=True,
)
parser.add_argument(
    '-p',
    '--period',
    choices=PERIODS,
    metavar='PERIOD',
    help='Required if the strategy is `ondemand`',
)


def print_price(instance,
                region,
                system,
                strategy,
                period):
    itype = instance['instance_type']
    price = instance['pricing'][region][system][strategy]
    if strategy == 'reserved':
        price = price[period]
    print(itype, price)


def main():
    args = parser.parse_args()
    instances = json.load(sys.stdin)
    for instance in instances:
        try:
            print_price(instance,
                        args.region,
                        args.system,
                        args.strategy,
                        args.period)
        except KeyError:
            pass


if __name__ == '__main__':
    main()
