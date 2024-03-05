# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import model


class CutadaptLogsFmt(model.TextFileFormat):
    def _validate(self, n_records=None):
        with open(str(self), "r") as file:
            # Read the content of the file
            file_content = file.read()

            # Check if the first line starts with the expected string
            if file_content.startswith("This is cutadapt"):

                # Check if "=== Summary ===" is present at least once
                if "=== Summary ===" in file_content:
                    pass
                else:
                    # Handle the case when "=== Summary ===" is not present
                    print(
                        "Validation failed. '=== Summary ===' "
                        "is not present in the file."
                    )
            else:
                # Handle the case when the first line does not start with
                # the expected string
                print(
                    "Validation failed. The first line does not start "
                    "with 'This is cutadapt'."
                )

    def _validate_(self, level):
        self._validate()


class CutadaptLogsDirectoryFormat(model.DirectoryFormat):
    kmer_json = model.File(r".+\.log$", format=CutadaptLogsFmt)
