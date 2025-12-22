# q2-long-reads-qc
QIIME2 plugin that utilizes Chopper and NanoPlot for quality control analysis of long sequences, generating easy-to-interpret stats as QIIME2 vizualization and allows trimming based on various filters.

## Installation
We provide three options for installing q2-long-reads-qc via conda environment files, depending on your preferred QIIME2 distribution. The environment files can be found in the `environment-files/` directory of this repository:

#### 1: Tiny distribution
Use the environment file `q2-long-reads-qc-qiime2-tiny-2025.10.yml` to create a new conda environment based on the tiny distro.

```shell
conda env create -n long-reads-env -f q2-long-reads-qc-qiime2-tiny-2025.10.yml
conda activate q2-long-reads-tiny
```


#### 2: Amplicon distribution
Use the environment file `q2-long-reads-qc-qiime2-amplicon-2025.10.yml` to create a new conda environment. 

```shell
conda env create -n long-reads-env -f q2-long-reads-qc-qiime2-amplicon-2025.10.yml
conda activate q2-long-reads-amplicon
```

#### 3: Moshpit distribution
Use the environment file `q2-long-reads-qc-qiime2-moshpit-2025.10.yml` to create a new conda environment based on the moshpit distro. 

```shell
conda env create -n long-reads-env -f q2-long-reads-qc-qiime2-moshpit-2025.10.yml
conda activate q2-long-reads-moshpit
```


### Execute

####  trime-single
##### Trim 20 nucleotides from the start of each read
```
qiime long-reads-qc trim --i-query-reads reads.qza --p-headcrop 20 --verbose --o-filtered-query-reads filtered.qza
```

#### stat
##### Generate a visualization of statistics for the input sequences
```
qiime long-reads-qc stats --i-sequences paired_reads.qza --o-visualization viz.qzv
```



##### [Qiime2 view](https://view.qiime2.org/) can be used to view the result visualization






<br>
<br>

We have added a new semantic type for the cutadapt log files named "CutadaptLogs".
```
qiime tools import --type 'CutadaptLogs' --input-path dir_with_cutadapt_log_files --output-path cutadapt_logs.qza
```
