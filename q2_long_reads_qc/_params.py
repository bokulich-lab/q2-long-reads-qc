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
from qiime2.plugin import Int, Range

# stats
stats_single_inputs = {"sequences": SampleData[SequencesWithQuality]}
stats_single_input_descriptions = {"sequences": "Single-end sequences to be analyzed."}
stats_paired_inputs = {"sequences": SampleData[PairedEndSequencesWithQuality]}
stats_paired_input_descriptions = {"sequences": "Paired-end sequences to be analyzed."}

# trim_single
trim_single_inputs = {
    "query_reads": SampleData[SequencesWithQuality],
}
trim_single_outputs = [("filtered_query_reads", SampleData[SequencesWithQuality])]
trim_single_parameters = {
    "threads": Int % Range(1, None),
    "quality": Int % Range(0, None),
    "maxqual": Int % Range(0, None),
    "minlength": Int % Range(1, None),
    "maxlength": Int % Range(1, None),
    "headcrop": Int % Range(0, None),
    "tailcrop": Int % Range(0, None),
}
trim_single_input_descriptions = {
    "query_reads": "Single-end sequences to be trimmed.",
}
trim_single_output_descriptions = {
    "filtered_query_reads": "The resulting trimmed sequences.",
}
trim_single_parameter_descriptions = {
    "threads": "Number of threads.",
    "quality": "Sets a minimum Phred average quality score.",
    "maxqual": "Sets a maximum Phred average quality score.",
    "minlength": "Sets a minimum read length.",
    "maxlength": "Sets a maximum read length.",
    "headcrop": "Trim N nucleotides from the start of a read.",
    "tailcrop": "Trim N nucleotides from the end of a read.",
}

# trim_paired
trim_paired_inputs = {"query_reads": SampleData[PairedEndSequencesWithQuality]}
trim_paired_outputs = [("filtered_query_reads", SampleData[SequencesWithQuality])]
trim_paired_parameters = {
    "threads": Int % Range(1, None),
    "quality": Int % Range(0, None),
    "maxqual": Int % Range(0, None),
    "minlength": Int % Range(1, None),
    "maxlength": Int % Range(1, None),
    "headcrop": Int % Range(0, None),
    "tailcrop": Int % Range(0, None),
}
trim_paired_input_descriptions = {"query_reads": "Paired-end sequences to be trimmed."}
trim_paired_output_descriptions = {
    "filtered_query_reads": "The resulting trimmed sequences."
}
trim_paired_parameter_descriptions = {
    "threads": "Number of threads.",
    "quality": "Sets a minimum Phred average quality score.",
    "maxqual": "Sets a maximum Phred average quality score.",
    "minlength": "Sets a minimum read length.",
    "maxlength": "Sets a maximum read length.",
    "headcrop": "Trim N nucleotides from the start of a read.",
    "tailcrop": "Trim N nucleotides from the end of a read.",
}
