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

from q2_16S_qc._utils import run_command
from q2_16S_qc.types._format import CutadaptLogsDirectoryFormat


# Run Nanoplot on sequence files in the specified directory
def _run_nanoplot(sequences_path, tmp):
    contents = os.listdir(sequences_path)
    matching_files = [f for f in contents if f.endswith(".fastq.gz")]
    # Create a list of full paths for each matching file
    full_paths = [os.path.join(sequences_path, f) for f in matching_files]

    # Construct Nanoplot command
    nanoplot_cmd = [
        "NanoPlot",
        "--fastq",
    ]

    nanoplot_cmd += full_paths

    nanoplot_cmd += [
        "-o",
        str(tmp),
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


def stats(
    output_dir: str,
    sequences: SingleLanePerSamplePairedEndFastqDirFmt,
    cutadapt_reports: CutadaptLogsDirectoryFormat = None,
):
    with tempfile.TemporaryDirectory() as tmp:
        _run_nanoplot(sequences.path, tmp)

        # Copy Nanoplot templates to the output directory
        TEMPLATES = pkg_resources.resource_filename("q2_16S_qc", "assets")
        copy_tree(os.path.join(TEMPLATES, "nanoplot"), output_dir)

        # Copy MultiQC data from the temporary directory to the output directory
        copy_tree(tmp, os.path.join(output_dir, "nanoplot_data"))

        # Generate an index.html file for MultiQC in the output directory
        context = {"tabs": [{"title": "Nanoplot", "url": "index.html"}]}
        index = os.path.join(TEMPLATES, "nanoplot", "index.html")
        templates = [index]
        q2templates.render(templates, output_dir, context=context)
