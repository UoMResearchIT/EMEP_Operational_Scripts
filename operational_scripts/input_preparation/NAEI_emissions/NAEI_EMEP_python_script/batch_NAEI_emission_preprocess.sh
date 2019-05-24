#!/bin/bash --login
#$ -cwd

module load apps/anaconda3/5.2.0/bin
source activate spyder

python NAEI_EMEP_preparation.py

