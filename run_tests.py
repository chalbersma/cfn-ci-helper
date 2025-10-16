#!/usr/bin/env python3

import unittest
import logging
import argparse

import utest

def get_argparse():
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="append_const", help="Verbosity Controls",
                        const=1, default=[])

    parser.add_argument("-c", "--config", help="Configuration File", default="config.yaml")
    parser.add_argument("-j", "--just", help="Just this Test", default=None)

    return parser



if __name__ == "__main__":

    parser = get_argparse()
    args = parser.parse_args()

    VERBOSE = len(args.verbose)

    EXTRA_MODULES = ["boto3", "urllib3", "botocore", "s3transfer"]
    extra_level = logging.ERROR

    if VERBOSE == 0:
        logging.basicConfig(level=logging.ERROR)
        extra_level = logging.ERROR
    elif VERBOSE == 1:
        logging.basicConfig(level=logging.WARNING)
        extra_level = logging.ERROR
    elif VERBOSE == 2:
        logging.basicConfig(level=logging.INFO)
        extra_level = logging.WARNING
    elif VERBOSE == 3:
        logging.basicConfig(level=logging.DEBUG)
        extra_level = logging.INFO
    elif VERBOSE >= 4:
        logging.basicConfig(level=logging.DEBUG)
        extra_level = logging.DEBUG


    for mod in EXTRA_MODULES:
        logging.getLogger(mod).setLevel(extra_level)

    logger = logging.getLogger("run_tests.py")

    loader = unittest.TestLoader()
    all_suite = loader.loadTestsFromModule(utest)


    runner = unittest.TextTestRunner()

    if args.just is None:
        runner.run(all_suite)
    else:
        if args.just not in utest.SOPTS.keys():
            raise ValueError("Test of {} not defined.".format(args.just))

        specific_test = utest.SOPTS[args.just]

        suite = unittest.defaultTestLoader.loadTestsFromTestCase(specific_test)
        runner.run(suite)
