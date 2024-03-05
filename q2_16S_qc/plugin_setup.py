# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from q2_types.per_sample_sequences import (
    PairedEndSequencesWithQuality,
    SequencesWithQuality,
)
from q2_types.sample_data import SampleData
from qiime2.plugin import Citations, Plugin

import q2_16S_qc
from q2_16S_qc import __version__
from q2_16S_qc.types._format import CutadaptLogsDirectoryFormat, CutadaptLogsFmt
from q2_16S_qc.types._type import CutadaptLogs

citations = Citations.load("citations.bib", package="q2_16S_qc")


plugin = Plugin(
    name="16S_qc",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-16S-qc",
    package="q2_16S_qc",
    description=(
        "QIIME2 plugin utilizing FastQC and MultiQC for comprehensive quality "
        "control analysis of 16S sequences, generating easy-to-interpret "
        "reports as QIIME2 vizualization."
    ),
    short_description="QIIME2 plugin for quality control of 16S sequences.",
)

plugin.register_formats(CutadaptLogsDirectoryFormat, CutadaptLogsFmt)
plugin.register_semantic_types(CutadaptLogs)
plugin.register_semantic_type_to_format(
    CutadaptLogs, artifact_format=CutadaptLogsDirectoryFormat
)

plugin.visualizers.register_function(
    function=q2_16S_qc.aggregate_results,
    inputs={
        "sequences": SampleData[SequencesWithQuality | PairedEndSequencesWithQuality],
        "cutadapt_reports": CutadaptLogs,
    },
    parameters="",
    input_descriptions={
        "sequences": "Fastq input sequences.",
        "cutadapt_reports": "Cutadapt reports.",
    },
    parameter_descriptions={},
    name="Quality control.",
    description="Quality control of 16S sequences for nf-16S-pipe.",
    citations=[citations["MultiQC"]],
)
