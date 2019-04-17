#!/bin/bash --login
#$ -cwd
#$ -pe smp.pe 4

module load use.own
module load priv_libs/gcc/netcdf/4.6.2
module load priv_libs/gcc/jasper/2.0.14
module load priv_libs/gcc/libpng/1.6.36
module load mpi/gcc/openmpi/3.1.3

# Minimalistic script for run the Unified EMEP model



# Run the model
mpiexec --mca btl ^vader -np 4 ./geogrid.exe 2>&1 | tee geogrid.log

