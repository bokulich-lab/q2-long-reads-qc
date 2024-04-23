# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import subprocess

import pandas as pd
import qiime2.util
import yaml
from q2_types.per_sample_sequences import (
    FastqManifestFormat,
    SingleLanePerSampleSingleEndFastqDirFmt,
    YamlFormat,
)
from q2_types.per_sample_sequences._transformer import (
    _parse_and_validate_manifest_partial,
)

from q2_long_reads_qc._utils import run_commands_with_pipe


# Constructs the command for the 'chopper' tool based on provided trimming parameters.
def construct_chopper_command(
    quality: int,
    maxqual: int,
    minlength: int,
    maxlength: int,
    headcrop: int,
    tailcrop: int,
    threads: int,
) -> list:
    return [
        "chopper",
        "--quality",
        str(quality),
        "--maxqual",
        str(maxqual),
        "--minlength",
        str(minlength),
        "--maxlength",
        str(maxlength),
        "--headcrop",
        str(headcrop),
        "--tailcrop",
        str(tailcrop),
        "--threads",
        str(threads),
    ]


def build_filtered_out_dir(input_reads, filtered_seqs):
    # Parse the input manifest to get a DataFrame of reads
    with input_reads.manifest.view(FastqManifestFormat).open() as fh:
        input_manifest = _parse_and_validate_manifest_partial(
            fh, single_end=True, absolute=False
        )
        # Filter the input manifest DataFrame for forward reads
        output_df = input_manifest[input_manifest.direction == "forward"]

    print("output_df:", output_df)

    # Initialize the output manifest
    output_manifest = FastqManifestFormat()
    # Copy input manifest to output manifest
    with output_manifest.open() as fh:
        output_df.to_csv(fh, index=False)

    # Initialize the result object to store filtered reads
    result = SingleLanePerSampleSingleEndFastqDirFmt()
    # Write the output manifest to the result object
    result.manifest.write_data(output_manifest, FastqManifestFormat)
    # Duplicate each filtered sequence file to the result object's directory
    for _, _, filename, _ in output_df.itertuples():
        qiime2.util.duplicate(
            str(filtered_seqs.path / filename), str(result.path / filename)
        )

    # Create metadata about the phred offset
    metadata = YamlFormat()
    metadata.path.write_text(yaml.dump({"phred-offset": 33}))
    # Attach metadata to the result
    result.metadata.write_data(metadata, YamlFormat)

    return result


def chop(
    query_reads: SingleLanePerSampleSingleEndFastqDirFmt,
    threads: int = 4,
    quality: int = 0,
    maxqual: int = 1000,
    minlength: int = 1,
    maxlength: int = 2147483647,
    headcrop: int = 0,
    tailcrop: int = 0,
) -> SingleLanePerSampleSingleEndFastqDirFmt:

    # Initialize directory format for filtered sequences
    filtered_seqs = SingleLanePerSampleSingleEndFastqDirFmt()

    # Import data from the manifest file to a df
    input_df = query_reads.manifest.view(pd.DataFrame)

    # Iterate over each forward read in the DataFrame
    for _, fwd in input_df.itertuples():
        res = str(filtered_seqs.path / os.path.basename(fwd))

        unzip_cmd = ["gunzip", "-c", str(fwd)]
        chopper_cmd = construct_chopper_command(
            quality, maxqual, minlength, maxlength, headcrop, tailcrop, threads
        )

        zip_cmd = ["gzip"]

        try:
            # Execute samtools fastq
            run_commands_with_pipe(unzip_cmd, chopper_cmd, zip_cmd, str(res))
        except subprocess.CalledProcessError as e:
            raise Exception(
                f"An error was encountered while using chopper, "
                f"(return code {e.returncode}), please inspect "
                "stdout and stderr to learn more."
            )

    result = build_filtered_out_dir(query_reads, filtered_seqs)

    return result
