#!/bin/bash --login
#$ -cwd

module load use.own
module load priv_libs/gcc/netcdf/4.6.2
module load priv_libs/gcc/jasper/2.0.14
module load priv_libs/gcc/libpng/1.6.36

# Minimalistic script for run the Unified EMEP model



# Run the model
./ungrib.exe 2>&1 | tee ungrib.log

