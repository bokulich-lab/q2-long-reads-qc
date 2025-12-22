# ----------------------------------------------------------------------------
# Copyright (c) 2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import subprocess

EXTERNAL_CMD_WARNING = (
    "Running external command line application(s). "
    "This may print messages to stdout and/or stderr.\n"
    "The command(s) being run are below. These commands "
    "cannot be manually re-run as they will depend on "
    "temporary files that no longer exist."
)


def run_command(cmd, verbose=True):
    if verbose:
        print(EXTERNAL_CMD_WARNING)
        print("\nCommand:", end=" ")
        print(" ".join(cmd), end="\n\n")
    subprocess.run(cmd, check=True)


def run_commands_with_pipe(cmd1, cmd2, cmd3, outfile_path, verbose=True):
    """Runs two consecutive commands using a pipe"""
    if verbose:
        print(EXTERNAL_CMD_WARNING)
        print("\nCommand:", end=" ")
        cmd_str = " | ".join(" ".join(cmd) for cmd in (cmd1, cmd2, cmd3))
        print(cmd_str, end="\n\n")

    # Start the first command
    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    # Pipe the output of cmd1 to cmd2
    p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits

    # Pipe output of cmd2 to cmd3, but manage the output file ourselves
    with open(outfile_path, "wb") as outfile:
        p3 = subprocess.Popen(cmd3, stdin=p2.stdout, stdout=outfile)
        p2.stdout.close()  # Allow p2 to receive a SIGPIPE if p3 exits

    # Wait for the processes to complete
    p1.wait()
    p2.wait()
    p3.wait()
