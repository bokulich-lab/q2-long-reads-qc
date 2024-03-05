# q2-16S-qc
QIIME2 plugin utilizing FastQC and MultiQC for quality control analysis of 16S sequences, generating easy-to-interpret reports as QIIME2 vizualization.

#### Create q2-16S-qc environment
```
mamba create -yn q2-16S-qc \
    -c conda-forge -c bioconda -c https://packages.qiime2.org/qiime2/2023.7/community/staged/ -c defaults \
    q2cli q2templates q2-types bs4 multiqc fastqc

```

#### Activate q2-16S-qc environment
```
mamba activate q2-16S-qc
```


```
make dev
qiime dev refresh-cache
```

#### Download Data
Download data [here](https://polybox.ethz.ch/index.php/s/xDYeOuxtTdypIXQ)


#### Execute
```
qiime 16S-qc aggregate-results --i-sequences paired_reads.qza --i-cutadapt-reports cutadapt_logs.qza --verbose --o-visualization viz
```

##### [Qiime2 view](https://view.qiime2.org/) can be used to view the result visualization

<br>

We have added a new semantic type for the cutadapt log files named "CutadaptLogs".
```
qiime tools import --type 'CutadaptLogs' --input-path dir_with_cutadapt_log_files --output-path cutadapt_logs.qza
```
