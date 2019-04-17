#!/bin/bash --login
#$ -cwd

module load tools/env/proxy2
module load use.own
module load priv_libs/python/ecmwfiapi/1.5.0

./download.py 2>&1 | tee log_download.txt
