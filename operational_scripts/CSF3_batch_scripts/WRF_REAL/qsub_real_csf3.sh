#!/bin/bash --login
#$ -cwd
#$ -pe smp.pe 6
#$ -l short

#module load use.own
module load mpi/gcc/openmpi/3.1.3
module load libs/gcc/netcdf/4.6.2
# loading the netcdf module should load the hdf5 and zlib libraries too - we will check to make sure
module list

rm rsl.error.* rsl.out.*

time mpirun --mca btl ^vader -np 6 ./real.exe

