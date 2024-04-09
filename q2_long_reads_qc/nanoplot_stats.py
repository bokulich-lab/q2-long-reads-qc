# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import subprocess
import tempfile
from distutils.dir_util import copy_tree

import pkg_resources
import q2templates
from q2_types.per_sample_sequences import SingleLanePerSamplePairedEndFastqDirFmt

from q2_long_reads_qc._utils import run_command


# Run NanoPlot on sequence files in the specified directory
def _run_nanoplot(sequences_path, output_dir):
    # Gather all matching fastq.gz files in the directory
    matching_files = [
        file for file in os.listdir(sequences_path) if file.endswith(".fastq.gz")
    ]

    # Check if no matching files were found
    if not matching_files:
        raise FileNotFoundError(
            f"No .fastq.gz files found in the directory {sequences_path}"
        )

    # Construct the full command for NanoPlot with paths and output directory
    nanoplot_cmd = [
        "NanoPlot",
        "--fastq",
        *[os.path.join(sequences_path, file) for file in matching_files],
        "-o",
        output_dir,
    ]

    try:
        # Run Nanoplot command
        run_command(nanoplot_cmd, verbose=True)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running nanoplot, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )


def nanoplot_stats(
    output_dir: str,
    sequences: SingleLanePerSamplePairedEndFastqDirFmt,
):
    with tempfile.TemporaryDirectory() as tmp:
        _run_nanoplot(sequences.path, tmp)

        # Copy Nanoplot templates to the output directory
        TEMPLATES = pkg_resources.resource_filename("q2_long_reads_qc", "assets")
        copy_tree(os.path.join(TEMPLATES, "nanoplot"), output_dir)

        # Copy Nanoplot data from the temporary directory to the output directory
        copy_tree(tmp, os.path.join(output_dir, "nanoplot_data"))

        # Generate an index.html file for Nanoplot in the output directory
        context = {"tabs": [{"title": "Nanoplot", "url": "index.html"}]}
        index = os.path.join(TEMPLATES, "nanoplot", "index.html")
        templates = [index]
        q2templates.render(templates, output_dir, context=context)
