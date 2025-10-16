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

class BasicCFNStack(unittest.TestCase):

    def setUp(self):
        """
        Gives me a Logger for Debugging
        """

        self.logger = logging.getLogger(__name__)

        self.default_render_data = dict(filename="example_stack.yaml",
                                        description="Unittest Stack",
                                        capabilities=[],
                                        parameters=[],
                                        tags=["test:value"],
                                        regions=["us-east-1"],
                                        profile="default")
        self.action_stack_args = dict(
            only_profiles=[],
            stackname=[],
            category=None,
            config=None,
            ## Moto's Parser doesn't handle yaml files so the test files all
            ## Need to not use CF Expansions (!Ref, !Sub, etc...) or it needs
            ## to be JSON formatted.
            stack="utest/example_stack_params-moto.json",
            # description=args.description,
            regions=["us-east-1"],
            capabilities=[],
            dynamic_tags=[],
            parameters=["ThingA:a", "ThingB:b"],
            profiles=["default"],
            delete=False)

        self.default_action_obj = cfnStack.ActionParser(
            **self.action_stack_args
        )


        self.logger = logging.getLogger("TestBackForth")

    @moto.mock_aws
    def test_obj_no_confirm(self):
        """
        for Each item in _abrn Run it
        """

        should_break = False

        this_result = cfnStack.ProcessStack(
            self.default_action_obj.action_stacks[0],
            confirm=False,
            live_add=self.default_action_obj.live_add
        )

        if this_result.return_status["fail"] is True:
            should_break = True

        result_row = this_result.return_table_row()

        self.assertEqual(len(result_row), 8, "Table Results too Short")
        self.assertFalse(result_row[-1], "Confirm is off f_triggered should be False")
        self.assertEqual(result_row[-2], "CONFIRM OFF", "Confirm is Off, result should respoect that")
        self.assertFalse(should_break, "This Shouldn't have Triggered a Break")



    @moto.mock_aws
    def test_obj_confirm(self):
        """
        for Each item in _abrn Run it
        """

        should_break = False

        this_result = cfnStack.ProcessStack(
            self.default_action_obj.action_stacks[0],
            confirm=True,
            live_add=self.default_action_obj.live_add
        )

        if this_result.return_status["fail"] is True:
            should_break = True

        result_row = this_result.return_table_row()

        self.assertEqual(len(result_row), 8, "Table Results too Short")
        self.assertFalse(result_row[-1], "Confirm is on f_triggered should be False")
        self.assertEqual(result_row[-2], "UPDATE SUCCESS", "Confirm is Off, result should respoect that")


    @moto.mock_aws
    def test_stack_delete(self):
        """
        for Each item in _abrn Run it
        """

        should_break = False

        this_result = cfnStack.ProcessStack(
            self.default_action_obj.action_stacks[0],
            confirm=True,
            live_add=self.default_action_obj.live_add
        )

        if this_result.return_status["fail"] is True:
            should_break = True

        delete_action_stack_args = self.action_stack_args

        delete_action_stack_args["delete"] = True

        delete_action_obj = cfnStack.ActionParser(
            **delete_action_stack_args
        )

        should_break = False

        this_result = cfnStack.ProcessStack(
            delete_action_obj.action_stacks[0],
            confirm=True,
            live_add=delete_action_obj.live_add
        )

        if this_result.return_status["fail"] is True:
            should_break = True

        result_row = this_result.return_table_row()

        self.assertEqual(len(result_row), 8, "Table Results too Short")
        self.assertFalse(result_row[-1], "Confirm is on f_triggered should be False")
        self.assertEqual(result_row[-2], "Deleted", "Confirm is Off, result should respoect that")





