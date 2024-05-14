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
    stats_input_descriptions,
    stats_inputs,
    trim_input_descriptions,
    trim_inputs,
    trim_output_descriptions,
    trim_outputs,
    trim_parameter_descriptions,
    trim_parameters,
)

citations = Citations.load("citations.bib", package="q2_long_reads_qc")

plugin = Plugin(
    name="long_reads_qc",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-long-reads-qc",
    package="q2_long_reads_qc",
    description=(
        "QIIME2 plugin that utilizes Chopper and NanoPlot for quality "
        "control analysis of long sequences, generating easy-to-interpret "
        "stats as QIIME2 vizualization and allows trimming based "
        "on various filters."
    ),
    short_description="QIIME2 plugin for quality control of long sequences.",
)

plugin.visualizers.register_function(
    function=q2_long_reads_qc.stats,
    inputs=stats_inputs,
    parameters="",
    input_descriptions=stats_input_descriptions,
    parameter_descriptions={},
    name="Quality control statistics of long sequences.",
    description="Quality control statistics of long sequences using NanoPlot.",
    citations=[citations["Nanopack2"]],
)

plugin.methods.register_function(
    function=q2_long_reads_qc.trim,
    inputs=trim_inputs,
    outputs=trim_outputs,
    parameters=trim_parameters,
    input_descriptions=trim_input_descriptions,
    output_descriptions=trim_output_descriptions,
    parameter_descriptions=trim_parameter_descriptions,
    name="Trim long sequences.",
    description="Trim long demultiplexed sequences using Chopper tool.",
    citations=[citations["Nanopack2"]],
)
