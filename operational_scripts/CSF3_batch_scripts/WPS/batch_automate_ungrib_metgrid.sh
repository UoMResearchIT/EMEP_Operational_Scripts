#!/bin/bash --login
#$ -cwd
#$ -pe smp.pe 8

module load libs/gcc/netcdf/4.6.2
module load libs/gcc/jasper/2.0.14
module load libs/gcc/libpng/1.6.36
module load mpi/gcc/openmpi/3.1.4

## set date ranges for processing (hardcoded one month at a time for now)
YEAR='2018'
MONTHS=( '01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12' )
DAY_START='01'
DAYS_END=( '31' '28' '31' '30' '31' '30' '31' '31' '30' '31' '30' '31' )

## standard settings for access paths
CWD=$(pwd)

GRIB_DIR=${CWD}/met_data/${YEAR}_data
NAMELIST_SOURCE_DIR=${CWD}/namelists/templates
NAMELIST_DIR=${CWD}/namelists

SFC_GRIB_DIR=${CWD}/WPS_UNGRIB_SFC
ATM_GRIB_DIR=${CWD}/WPS_UNGRIB_ATM

EMEP_MET_DIR=${CWD}/WPS_METGRID_50km
UK_MET_DIR=${CWD}/WPS_METGRID_3km


## namelist file names
NAMELIST_FILES=( 'namelist.wps.ungrib_sfc' 'namelist.wps.ungrib_atm' \
				'namelist.wps.emep_50km' 'namelist.wps.emep_uk3km' )




## loop through the months (hardcoded limits for the moment)
for count in {0..11}
do
	# pull out month & end day
	MONTH=${MONTHS[count]}
	DAY_END=${DAYS_END[count]}

	# copy the namelist files, setting date information
	for namefile in ${NAMELIST_FILES[@]}
	do
		sed -e "s|%%YRST%%|${YEAR}|g" \
			-e "s|%%MONST%%|${MONTH}|g" \
			-e "s|%%DAYST%%|${DAY_START}|g" \
			-e "s|%%YREND%%|${YEAR}|g" \
			-e "s|%%MONEND%%|${MONTH}|g" \
			-e "s|%%DAYEND%%|${DAY_END}|g" \
			${NAMELIST_SOURCE_DIR}/${namefile}.template \
			 > ${NAMELIST_DIR}/${namefile}
	done


	## ungrib work, for surface data
	cd ${SFC_GRIB_DIR}
	# link to data
	./link_grib.csh ${GRIB_DIR}/sfc_${YEAR}${MONTH}*
	# link to surface namelist file
	ln -sf ${NAMELIST_DIR}/namelist.wps.ungrib_sfc namelist.wps
	# ungrib surface data
	./ungrib.exe 2>&1 | tee ungrib.sfc.${MONTH}.log &

	## ungrib work, for atmospheric data
	cd ${ATM_GRIB_DIR}
	# link to data
	./link_grib.csh ${GRIB_DIR}/pl_${YEAR}${MONTH}*
	# link to surface namelist file
	ln -sf ${NAMELIST_DIR}/namelist.wps.ungrib_atm namelist.wps
	# ungrib surface data
	./ungrib.exe 2>&1 | tee ungrib.atm.${MONTH}.log &

	wait # wait for the two ungrib processes to finish


	## metgrid work, 50km EMEP grid
	cd ${EMEP_MET_DIR}
	# link the namelist
	ln -sf ${NAMELIST_DIR}/namelist.wps.emep_50km namelist.wps
	# link to the met data
	ln -sf ${SFC_GRIB_DIR}/SFCFILE* .
	ln -sf ${ATM_GRIB_DIR}/ATMFILE* .
	# run metgrid
	mpiexec -np 4 ./metgrid.exe 2>&1 | tee metgrid.${MONTH}.log  &

	## metgrid work, 3km EMEP grid
	cd ${UK_MET_DIR}
	# link the namelist
	ln -sf ${NAMELIST_DIR}/namelist.wps.emep_uk3km namelist.wps
	# link to the met data
	ln -sf ${SFC_GRIB_DIR}/SFCFILE* .
	ln -sf ${ATM_GRIB_DIR}/ATMFILE* .
	# run metgrid
	mpiexec -np 4 ./metgrid.exe 2>&1 | tee metgrid.${MONTH}.log  &

	wait # wait for the two met grid processes to finish
		
	## tidy up once we've finished
	cd $CWD
	rm ${EMEP_MET_DIR}/SFCFILE* ${EMEP_MET_DIR}/ATMFILE*
	rm ${UK_MET_DIR}/SFCFILE* ${UK_MET_DIR}/ATMFILE*
	rm ${SFC_GRIB_DIR}/SFCFILE* ${ATM_GRIB_DIR}/ATMFILE*

done