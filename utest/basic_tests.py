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


        self.logger = logging.getLogger("TestBackForth")

    @moto.mock_aws
    def test_obj(self):
        """
        for Each item in _abrn Run it
        """

        with importlib.resources.path(cfnStack, "default_stack.yaml.jinja") as stack_template_path:
            with open(stack_template_path, "r") as stack_template_fobj:
                stack_template_str = stack_template_fobj.read()

                config_template = jinja2.Environment(loader=jinja2.BaseLoader,
                                                     autoescape=jinja2.select_autoescape(
                                                         enabled_extensions=('html', 'xml'),
                                                         default_for_string=False
                                                     )).from_string(stack_template_str)

                config_rendered = config_template.render(**self.default_render_data)

                self.logger.debug("Live Rendered: {}".format(config_rendered))

                category_configs = yaml.safe_load(config_rendered)

                self.logger.debug("configs: {}".format(category_configs))

        self.assertEqual(1, 1, "Test")
