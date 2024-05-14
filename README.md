# q2-long-reads-qc
QIIME2 plugin that utilizes Chopper and NanoPlot for quality control analysis of long sequences, generating easy-to-interpret stats as QIIME2 vizualization and allows trimming based on various filters.

### Create q2-long-reads-qc environment
```
mamba create -yn q2-long-reads-qc \
    -c conda-forge -c bioconda -c https://packages.qiime2.org/qiime2/2023.7/community/staged/ -c defaults \
    q2cli q2templates q2-types bs4 multiqc fastqc gzip nanoplot chopper

```

### Activate q2-long-reads-qc environment
```
conda activate q2-long-reads-qc
```


```
make dev
qiime dev refresh-cache
```

### Download Data
Download data [here](https://polybox.ethz.ch/index.php/s/xDYeOuxtTdypIXQ)


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
