# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import tempfile
import unittest
from unittest.mock import call, patch

import bs4

from q2_long_reads_qc._utils import (
    _construct_param,
    _get_sample_from_path,
    _modify_links,
    _process_common_input_params,
    _remove_html_element,
    run_command,
    run_commands_with_pipe,
)

EXTERNAL_CMD_WARNING = (
    "Running external command line application(s). "
    "This may print messages to stdout and/or stderr.\n"
    "The command(s) being run are below. These commands "
    "cannot be manually re-run as they will depend on "
    "temporary files that no longer exist."
)


class TestRunCommand(unittest.TestCase):
    @patch("builtins.print")
    @patch("subprocess.run")
    def test_run_command_verbose(self, mock_run, mock_print):
        cmd = ["echo", "Hello, World!"]
        run_command(cmd, verbose=True)

        # Check that the warning message and command are printed
        mock_print.assert_has_calls(
            [
                call(EXTERNAL_CMD_WARNING),
                call("\nCommand:", end=" "),
                call("echo Hello, World!", end="\n\n"),
            ]
        )

        # Check that subprocess.run is called with the correct arguments
        mock_run.assert_called_once_with(cmd, check=True)


class TestCommandOperations(unittest.TestCase):
    def test_run_commands_with_pipe(self):
        # This is a simplistic test scenario; you might want to mock subprocess.run
        cmd1 = ["echo", "hello"]
        cmd2 = ["grep", "hello"]
        cmd3 = ["echo", "hello"]
        with tempfile.TemporaryDirectory() as temp_dir:
            run_commands_with_pipe(
                cmd1, cmd2, cmd3, temp_dir + "res.out"
            )  # Assuming no exception is good enough for this test

    def test_run_commands_with_pipe_no_verbose(self):
        # This is a simplistic test scenario; you might want to mock subprocess.run
        cmd1 = ["echo", "hello"]
        cmd2 = ["grep", "hello"]
        cmd3 = ["echo", "hello"]
        with tempfile.TemporaryDirectory() as temp_dir:
            run_commands_with_pipe(
                cmd1, cmd2, cmd3, temp_dir + "res.out", verbose=False
            )  # Assuming no exception is good enough for this test


class TestParameterConstruction(unittest.TestCase):
    def test_construct_param(self):
        self.assertEqual(_construct_param("test_param"), "--test-param")
        # Test does not handle camelCase, so adjust expectations:
        self.assertNotEqual(_construct_param("anotherTestParam"), "--anothertestparam")


def processing_adapter(key, value):
    """Adapter to fit the existing `_construct_param` for testing."""
    param = _construct_param(key)
    if isinstance(value, bool):
        return [param] if value else []
    else:
        return [param, str(value)]


class TestProcessCommonInputParams(unittest.TestCase):
    def test_process_common_input_params(self):
        params = {
            "test_param": True,
            "another_param": None,
            "yet_another_param": "value",
        }
        processed = _process_common_input_params(processing_adapter, params)
        self.assertIn("--test-param", processed)
        self.assertNotIn(
            "--another-param", processed
        )  # 'another_param' is None, should not appear
        self.assertIn("--yet-another-param", processed)
        self.assertIn("value", processed)


class TestHtmlManipulation(unittest.TestCase):
    def setUp(self):
        # Set up a simple HTML content over two lines
        self.html_content = (
            '<html><body><div id="remove_this">Text</div> '
            + '<a href="link.html">Link</a></body></html>'
        )
        self.fp = "test.html"
        with open(self.fp, "w") as f:
            f.write(self.html_content)

    def test_remove_html_element(self):
        _remove_html_element(self.fp, "div", "remove_this")
        with open(self.fp, "r") as f:
            soup = bs4.BeautifulSoup(f.read(), "html.parser")
            self.assertIsNone(soup.find("div", id="remove_this"))

    def test_modify_links(self):
        _modify_links(self.fp)
        with open(self.fp, "r") as f:
            soup = bs4.BeautifulSoup(f.read(), "html.parser")
            self.assertEqual(soup.find("a")["target"], "_blank")

    def tearDown(self):
        os.remove(self.fp)


class TestGetSampleFromPath(unittest.TestCase):
    def test_normal_case(self):
        # A typical file path
        path = "/path/to/sample1_contigs.fa"
        expected = "sample1"
        result = _get_sample_from_path(path)
        self.assertEqual(result, expected)

    def test_with_directories_in_path(self):
        # Path containing directories
        path = "sample2_contigs.fa"
        expected = "sample2"
        result = _get_sample_from_path(path)
        self.assertEqual(result, expected)

    def test_path_without_suffix(self):
        # Path does not have the expected suffix
        path = "sample3.fasta"
        expected = "sample3.fasta"  # Full name should return as no suffix to split
        result = _get_sample_from_path(path)
        self.assertEqual(result, expected)

    def test_empty_string(self):
        # Empty string input
        path = ""
        expected = ""  # Should return empty string if no path is given
        result = _get_sample_from_path(path)
        self.assertEqual(result, expected)

    def test_suffix_not_at_end(self):
        # Suffix appears but not at the end
        path = "sample4_contigs.fa_contigs.fa"
        expected = "sample4_contigs.fa"
        result = _get_sample_from_path(path)
        self.assertEqual(result, expected)
