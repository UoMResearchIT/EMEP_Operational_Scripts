#!/bin/bash --login
#$ -cwd

module load libs/gcc/netcdf/4.6.2
module load libs/gcc/jasper/2.0.14
module load libs/gcc/libpng/1.6.36

# Minimalistic script for run the Unified EMEP model



# Run the model
./ungrib.exe 2>&1 | tee ungrib.log

