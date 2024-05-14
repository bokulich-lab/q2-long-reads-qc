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
from qiime2.plugin import Int, Range, TypeMatch

T = TypeMatch([SequencesWithQuality, PairedEndSequencesWithQuality])

# stats
stats_inputs = {"sequences": SampleData[T]}
stats_input_descriptions = {"sequences": "Sequences to be analyzed."}

# trim
trim_inputs = {"query_reads": SampleData[T]}
trim_outputs = [("filtered_query_reads", SampleData[T])]
trim_parameters = {
    "threads": Int % Range(1, None),
    "quality": Int % Range(0, None),
    "maxqual": Int % Range(0, None),
    "minlength": Int % Range(1, None),
    "maxlength": Int % Range(1, None),
    "headcrop": Int % Range(0, None),
    "tailcrop": Int % Range(0, None),
}
trim_input_descriptions = {"query_reads": "Sequences to be trimmed."}
trim_output_descriptions = {"filtered_query_reads": "The resulting trimmed sequences."}
trim_parameter_descriptions = {
    "threads": "Number of threads.",
    "quality": "Sets a minimum Phred average quality score.",
    "maxqual": "Sets a maximum Phred average quality score.",
    "minlength": "Sets a minimum read length.",
    "maxlength": "Sets a maximum read length.",
    "headcrop": "Trim N nucleotides from the start of a read.",
    "tailcrop": "Trim N nucleotides from the end of a read.",
}
