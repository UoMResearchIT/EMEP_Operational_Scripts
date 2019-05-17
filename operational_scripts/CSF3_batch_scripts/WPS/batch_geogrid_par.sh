#!/bin/bash --login
#$ -cwd
#$ -pe smp.pe 4

module load libs/gcc/netcdf/4.6.2
module load libs/gcc/jasper/2.0.14
module load libs/gcc/libpng/1.6.36
module load mpi/gcc/openmpi/3.1.4

# Minimalistic script for run the Unified EMEP model



# Run the model
mpiexec -np 4 ./geogrid.exe 2>&1 | tee geogrid.log

