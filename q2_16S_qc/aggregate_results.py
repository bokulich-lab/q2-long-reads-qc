# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import shutil
import subprocess
import tempfile
from distutils.dir_util import copy_tree

import pkg_resources
import q2templates
from q2_types.per_sample_sequences import SingleLanePerSamplePairedEndFastqDirFmt

from q2_16S_qc._utils import run_command
from q2_16S_qc.types._format import CutadaptLogsDirectoryFormat


# Run FastQC on sequence files in the specified directory
def _run_fastqc(sequences_path, tmp):
    contents = os.listdir(sequences_path)
    matching_files = [f for f in contents if f.endswith(".fastq.gz")]

    for file_name in matching_files:
        # Construct FastQC command
        fastqc_cmd = [
            "fastqc",
            str(sequences_path) + "/" + str(file_name),
            "-o",
            str(tmp),
        ]

        try:
            # Run FastQC command
            run_command(fastqc_cmd, verbose=True)
        except subprocess.CalledProcessError as e:
            raise Exception(
                "An error was encountered while running fastqc, "
                f"(return code {e.returncode}), please inspect "
                "stdout and stderr to learn more."
            )


# Extract Cutadapt log files and copy them to a temporary directory
def _extract_cutadapt_logs(cutadapt_reports_path, tmp):
    cutadapt_reports_contents = os.listdir(cutadapt_reports_path)
    matching_files = [
        file for file in cutadapt_reports_contents if file.endswith(".log")
    ]

    for file_name in matching_files:
        source_path = os.path.join(cutadapt_reports_path, file_name)
        destination_path = os.path.join(tmp, file_name)

        try:
            # Copy the file to the tmp directory
            shutil.copyfile(source_path, destination_path)
            print(f"Successfully copied {file_name} to {tmp}")
        except Exception as e:
            print(f"Error copying {file_name}: {e}")


# Run MultiQC on the specified directory containing analysis results
def _run_multiqc(tmp):
    multiqc_cmd = ["multiqc", str(tmp), "-o", str(tmp)]

    try:
        run_command(multiqc_cmd, verbose=True)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running multiqc, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )


def aggregate_results(
    output_dir: str,
    sequences: SingleLanePerSamplePairedEndFastqDirFmt,
    cutadapt_reports: CutadaptLogsDirectoryFormat = None,
):
    with tempfile.TemporaryDirectory() as tmp:
        # Run FastQC on the input sequences and store results in the temporary directory
        _run_fastqc(sequences.path, tmp)

        # Extract cutadapt logs and store in the temporary directory
        if cutadapt_reports is not None:
            _extract_cutadapt_logs(cutadapt_reports.path, tmp)

        # Run MultiQC on the temporary directory to aggregate results
        _run_multiqc(tmp)

        # Copy MultiQC templates to the output directory
        TEMPLATES = pkg_resources.resource_filename("q2_16S_qc", "assets")
        copy_tree(os.path.join(TEMPLATES, "multiqc"), output_dir)

        # Copy MultiQC data from the temporary directory to the output directory
        copy_tree(tmp, os.path.join(output_dir, "multiqc_data"))

        # Generate an index.html file for MultiQC in the output directory
        context = {"tabs": [{"title": "MultiQC", "url": "index.html"}]}
        index = os.path.join(TEMPLATES, "multiqc", "index.html")
        templates = [index]
        q2templates.render(templates, output_dir, context=context)
