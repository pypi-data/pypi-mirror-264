#!/usr/bin/env python

"""Tests for `airflow_bootstrap_utils` package."""


import unittest
from click.testing import CliRunner

from airflow_bootstrap_utils import airflow_bootstrap_utils
from airflow_bootstrap_utils import cli


class TestAirflow_bootstrap_utils(unittest.TestCase):
    """Tests for `airflow_bootstrap_utils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'airflow_bootstrap_utils.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
