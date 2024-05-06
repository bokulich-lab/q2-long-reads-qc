# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Citations, Plugin

import q2_long_reads_qc
from q2_long_reads_qc import __version__
from q2_long_reads_qc._params import (
    stats_paired_input_descriptions,
    stats_paired_inputs,
    stats_single_input_descriptions,
    stats_single_inputs,
    trim_paired_input_descriptions,
    trim_paired_inputs,
    trim_paired_output_descriptions,
    trim_paired_outputs,
    trim_paired_parameter_descriptions,
    trim_paired_parameters,
    trim_single_input_descriptions,
    trim_single_inputs,
    trim_single_output_descriptions,
    trim_single_outputs,
    trim_single_parameter_descriptions,
    trim_single_parameters,
)

citations = Citations.load("citations.bib", package="q2_long_reads_qc")

plugin = Plugin(
    name="long_reads_qc",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-long-reads-qc",
    package="q2_long_reads_qc",
    description=(
        "QIIME2 plugin utilizing FastQC and MultiQC for comprehensive quality "
        "control analysis of 16S sequences, generating easy-to-interpret "
        "reports as QIIME2 vizualization."
    ),
    short_description="QIIME2 plugin for quality control of long sequences.",
)

plugin.visualizers.register_function(
    function=q2_long_reads_qc.stats_single,
    inputs=stats_single_inputs,
    parameters="",
    input_descriptions=stats_single_input_descriptions,
    parameter_descriptions={},
    name="Quality control statistics using NanoPlot for long single-end reads.",
    description="Quality control statistics using NanoPlot for long single-end reads.",
    citations=[citations["Nanopack2"]],
)

plugin.visualizers.register_function(
    function=q2_long_reads_qc.stats_paired,
    inputs=stats_paired_inputs,
    parameters="",
    input_descriptions=stats_paired_input_descriptions,
    parameter_descriptions={},
    name="Quality control statistics using NanoPlot for long paired-end reads.",
    description="Quality control statistics using NanoPlot for long paired-end reads.",
    citations=[citations["Nanopack2"]],
)


plugin.methods.register_function(
    function=q2_long_reads_qc.trim_single,
    inputs=trim_single_inputs,
    outputs=trim_single_outputs,
    parameters=trim_single_parameters,
    input_descriptions=trim_single_input_descriptions,
    output_descriptions=trim_single_output_descriptions,
    parameter_descriptions=trim_single_parameter_descriptions,
    name="Filtering and trimming long reads using Chopper.",
    description="Filtering and trimming long reads using Chopper.",
    citations=[citations["Nanopack2"]],
)

plugin.methods.register_function(
    function=q2_long_reads_qc.trim_paired,
    inputs=trim_paired_inputs,
    outputs=trim_paired_outputs,
    parameters=trim_paired_parameters,
    input_descriptions=trim_paired_input_descriptions,
    output_descriptions=trim_paired_output_descriptions,
    parameter_descriptions=trim_paired_parameter_descriptions,
    name="Filtering and trimming long reads using Chopper.",
    description="Filtering and trimming long reads using Chopper.",
    citations=[citations["Nanopack2"]],
)
