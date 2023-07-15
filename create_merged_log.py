import os
import sys

import json
import argparse

import time
from datetime import datetime


def merged_log(path_a: str, path_b: str, path_merged: str) -> None:

    log_a = open(f'{path_a}', 'r')
    log_b = open(f'{path_b}', 'r')

    # create start lines
    log_a_value = json.loads(next(log_a, '-1'))
    log_b_value = json.loads(next(log_b, '-1'))

    # prepare log_merged file to write logs
    with open(f'{path_merged}', 'w') as file:
        file.write('')

    log_merged = open(f'{path_merged}', 'a')

    while True:

        log_a_timestamp = int(datetime.strptime(log_a_value['timestamp'],
                                                '%Y-%m-%d %H:%M:%S').timestamp()) if log_a_value != -1 else -1
        log_b_timestamp = int(datetime.strptime(log_b_value['timestamp'],
                                                '%Y-%m-%d %H:%M:%S').timestamp()) if log_b_value != -1 else -1

        # compare two logs via unix_timestamp
        if log_a_timestamp > log_b_timestamp:

            # if logs have different filesize
            if log_b_timestamp == -1:

                log_merged.write(f"{json.dumps(log_a_value)}\n")
                log_a_value = json.loads(next(log_a, '-1'))
            else:
                log_merged.write(f"{json.dumps(log_b_value)}\n")
                log_b_value = json.loads(next(log_b, '-1'))

        elif log_a_timestamp == log_b_timestamp:

            # check only one var cause they are equals
            if log_a_timestamp == -1:
                break

            log_merged.write(f"{json.dumps(log_a_value)}\n")
            log_merged.write(f"{json.dumps(log_b_value)}\n")

            log_a_value = json.loads(next(log_a, '-1'))
            log_b_value = json.loads(next(log_b, '-1'))

        else:
            # if logs have different filesize
            if log_a_timestamp == -1:

                log_merged.write(f"{json.dumps(log_b_value)}\n")
                log_b_value = json.loads(next(log_b, '-1'))
            else:
                log_merged.write(f"{json.dumps(log_a_value)}\n")
                log_a_value = json.loads(next(log_a, '-1'))

    log_a.close()
    log_b.close()
    log_merged.close()


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser()
    parser.add_argument('log_a',
                        help='type path to log_a',
                        type=os.path.abspath,
                        )
    parser.add_argument('log_b',
                        help='type path to log_b',
                        type=os.path.abspath,
                        )
    parser.add_argument('-o',
                        '--output',
                        help='type output path (log_merged)',
                        type=os.path.abspath,
                        )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    try:
        start_time = time.time()
        merged_log(path_a=args.log_a,
                   path_b=args.log_b,
                   path_merged=args.output,
                   )
        print(f'Success! Time: {round(time.time() - start_time, 2)} sec. Saved to {args.output}')
    except Exception as e:
        print(e)
