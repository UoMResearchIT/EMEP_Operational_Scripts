#!/bin/bash --login
#$ -cwd
#$ -pe mpi-24-ib.pe 96

module load libs/gcc/netcdf/4.6.2
module load mpi/gcc/openmpi/3.1.3

# Minimalistic script for run the Unified EMEP model
GRID=EECCA
NLEV=20lev

pwd

#export PMIX_DEBUG=100

# Run the model
mpiexec --mca btl ^vader -np 96 ../exec_code/emepctm
#mpiexec -mca mpi_show_mca_params all -np 2 ../exec_code/Unimod_extra
#mpiexec -np 2 ../exec_code/Unimod_extra

#sync
