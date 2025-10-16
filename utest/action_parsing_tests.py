#!/usr/bin/env python3

"""
Let's Test Basic, Funamental Usability of ABRN
"""

import unittest
import logging
import importlib.resources

import jinja2
import yaml
import moto

import cfnStack

class BasicActionTuple(unittest.TestCase):

    def setUp(self):
        """
        Gives me a Logger for Debugging
        """

        self.logger = logging.getLogger(__name__)

        self.logger = logging.getLogger("TestBackForth")

    def test_obj(self):
        """
        for Each item in _abrn Run it
        """

        action_obj = cfnStack.ActionParser(
            only_profiles=[],
            stackname=[],
            category="utest/utest_stack",
            config=None,
            stack=None,
            #description=args.description,
            regions=["us-east-1"],
            capabilities=[],
            dynamic_tags=[],
            parameters=[],
            profiles=[],
            delete=False,
        )

        self.logger.debug(action_obj.action_stacks)


        self.assertEqual(len(action_obj.action_stacks), 1)

        the_stack = action_obj.action_stacks[0]

        self.assertEqual(the_stack["stack"], "ssm-0-test")
        self.assertEqual(the_stack["region"], "us-east-1")
        self.assertEqual(the_stack["profile"], "unnamedsec")

        yaml_parse_error = None

        try:
            stack_config_read = yaml.safe_load(the_stack["stack_config_json"])
        except Exception as e:
            yaml_parse_error = e

        self.assertIsNone(yaml_parse_error)

    @moto.mock_aws
    def test_regions_all(self):
        """
        for Each item in _abrn Run it
        """

        action_obj = cfnStack.ActionParser(
            only_profiles=[],
            stackname=[],
            category=None,
            config=None,
            stack="utest/example_stack.yaml",
            # description=args.description,
            regions=["all"],
            capabilities=[],
            dynamic_tags=[],
            parameters=[],
            profiles=["default"],
            delete=False,
        )

        #self.logger.debug(action_obj.action_stacks)

        self.assertGreater(len(action_obj.action_stacks), 30, "Should be many regions and many stacks")

    @moto.mock_aws
    def test_regions_all_altservice(self):
        """
        for Each item in _abrn Run it
        """

        action_obj = cfnStack.ActionParser(
            only_profiles=[],
            stackname=[],
            category=None,
            config=None,
            stack="utest/example_stack.yaml",
            # description=args.description,
            regions=["all:s3"],
            capabilities=[],
            dynamic_tags=[],
            parameters=[],
            profiles=["default"],
            delete=False,
        )

        #self.logger.debug(action_obj.action_stacks)

        self.assertGreater(len(action_obj.action_stacks), 30, "Should be many regions and many stacks")

    @moto.mock_aws
    def test_dynamic_params(self):
        """
        for Each item in _abrn Run it
        """

        action_obj = cfnStack.ActionParser(
            only_profiles=[],
            stackname=[],
            category=None,
            config=None,
            stack="utest/example_stack_params.yaml",
            # description=args.description,
            regions=["us-east-1"],
            capabilities=[],
            dynamic_tags=[],
            parameters=["ThingA:valuea", {"Key": "ThingB", "Value": "valueb"}],
            profiles=["default"],
            delete=False,
        )

        self.logger.debug("Action Stacks Params Test {}".format(action_obj.live_add))

        self.assertEqual(len(action_obj.live_add["parameters"].keys()), 2, "Should be Two Parameters")
