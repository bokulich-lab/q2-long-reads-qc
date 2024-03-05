import os
import subprocess
import unittest
from unittest.mock import call, patch

import q2_16S_qc._utils
import q2_16S_qc.quality_control


class TestRunFastQC(unittest.TestCase):
    @patch("subprocess.run")
    @patch("os.listdir")
    def test_run_fastqc(self, mock_listdir, mock_run_command):
        # Setup
        sequences_path = "/path/to/sequences"
        tmp_path = "/path/to/tmp"
        # Mock os.listdir to return a list of files
        mock_listdir.return_value = [
            "file1.fastq.gz",
            "file2.fastq.gz",
            "other_file.txt",
        ]

        # Expected command calls adjusted to match the actual behavior
        expected_calls = [
            call(
                [
                    "fastqc",
                    f"{sequences_path}/file1.fastq.gz",
                    "-o",
                    tmp_path,
                ],
                check=True,
            ),  # Adjusted to match actual call
            call(
                [
                    "fastqc",
                    f"{sequences_path}/file2.fastq.gz",
                    "-o",
                    tmp_path,
                ],
                check=True,
            ),  # Adjusted to match actual call
        ]

        # Action
        q2_16S_qc.quality_control._run_fastqc(sequences_path, tmp_path)

        # Assert
        mock_listdir.assert_called_once_with(sequences_path)
        mock_run_command.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_run_command.call_count, 2)

    @patch("subprocess.run")
    @patch("os.listdir")
    def test_run_fastqc_with_error(self, mock_listdir, mock_run_command):
        # Setup to test error handling
        sequences_path = "/path/to/sequences"
        tmp_path = "/path/to/tmp"
        mock_listdir.return_value = ["bad_file.fastq.gz"]
        mock_run_command.side_effect = subprocess.CalledProcessError(1, "fastqc")

        # Action and Assert
        with self.assertRaises(Exception):
            q2_16S_qc.quality_control._run_fastqc(sequences_path, tmp_path)

        # Ensure the error was raised due to the subprocess.CalledProcessError
        mock_run_command.assert_called()


class TestExtractCutadaptLogs(unittest.TestCase):
    @patch("shutil.copyfile")
    @patch("os.listdir")
    def test_extract_cutadapt_logs(self, mock_listdir, mock_copyfile):
        # Setup
        cutadapt_reports_path = "/path/to/cutadapt/reports"
        tmp_path = "/path/to/tmp"
        # Mock os.listdir to return a list of files, including .log files and others
        mock_listdir.return_value = ["cutadapt1.log", "cutadapt2.log", "other_file.txt"]

        # Expected copy calls
        expected_calls = [
            call(
                os.path.join(cutadapt_reports_path, "cutadapt1.log"),
                os.path.join(tmp_path, "cutadapt1.log"),
            ),
            call(
                os.path.join(cutadapt_reports_path, "cutadapt2.log"),
                os.path.join(tmp_path, "cutadapt2.log"),
            ),
        ]

        # Action
        q2_16S_qc.quality_control._extract_cutadapt_logs(
            cutadapt_reports_path, tmp_path
        )  # Adjust according to your module's structure

        # Assert
        mock_listdir.assert_called_once_with(cutadapt_reports_path)
        mock_copyfile.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_copyfile.call_count, 2)


class TestRunMultiQC(unittest.TestCase):
    @patch("subprocess.run")
    def test_run_multiqc_success(self, mock_run_command):
        # Setup
        tmp_path = "/path/to/tmp"

        # Expected command
        expected_cmd = ["multiqc", str(tmp_path), "-o", str(tmp_path)]

        # Action
        q2_16S_qc.quality_control._run_multiqc(tmp_path)

        # Assert
        mock_run_command.assert_called_once_with(expected_cmd, check=True)

    @patch("subprocess.run")
    def test_run_multiqc_failure(self, mock_run_command):
        # Setup
        tmp_path = "/path/to/tmp"
        mock_run_command.side_effect = subprocess.CalledProcessError(1, "multiqc")

        # Action and Assert
        with self.assertRaises(Exception) as context:
            q2_16S_qc.quality_control._run_multiqc(tmp_path)

        # Ensure the exception was raised due to the subprocess.CalledProcessError
        self.assertTrue(
            "An error was encountered while running multiqc" in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
