# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import tempfile
import unittest
from unittest.mock import call, patch

from q2_long_reads_qc._utils import (
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
        # This is a simplistic test scenario; you might want to mock
        # subprocess.run
        cmd1 = ["echo", "hello"]
        cmd2 = ["grep", "hello"]
        cmd3 = ["echo", "hello"]
        with tempfile.TemporaryDirectory() as temp_dir:
            run_commands_with_pipe(
                cmd1, cmd2, cmd3, temp_dir + "res.out"
            )  # Assuming no exception is good enough for this test

    def test_run_commands_with_pipe_no_verbose(self):
        # This is a simplistic test scenario; you might want to mock
        # subprocess.run
        cmd1 = ["echo", "hello"]
        cmd2 = ["grep", "hello"]
        cmd3 = ["echo", "hello"]
        with tempfile.TemporaryDirectory() as temp_dir:
            run_commands_with_pipe(
                cmd1, cmd2, cmd3, temp_dir + "res.out", verbose=False
            )  # Assuming no exception is good enough for this test


if __name__ == "__main__":
    unittest.main()
