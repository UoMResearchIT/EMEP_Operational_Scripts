#!/bin/bash

module load tools/env/proxy2

# Ammonia
wget http://naei.beis.gov.uk/mapping/mapping_2016/21.zip
# Carbon Monoxide
wget http://naei.beis.gov.uk/mapping/mapping_2016/4.zip
# NOx
wget http://naei.beis.gov.uk/mapping/mapping_2016/6.zip
# NMVOC
wget http://naei.beis.gov.uk/mapping/mapping_2016/9.zip
# SO2
wget http://naei.beis.gov.uk/mapping/mapping_2016/8.zip
# CH4
wget http://naei.beis.gov.uk/mapping/mapping_2016/3.zip
# hydrogen chloride (HCl)
wget http://naei.beis.gov.uk/mapping/mapping_2016/14.zip


# PM 0.1
wget http://naei.beis.gov.uk/mapping/mapping_2016/124.zip
# PM 1
wget http://naei.beis.gov.uk/mapping/mapping_2016/123.zip
# PM2.5
wget http://naei.beis.gov.uk/mapping/mapping_2016/PM25.zip
# PM 10
wget http://naei.beis.gov.uk/mapping/mapping_2016/24.zip

# point sources (all)
wget http://naei.beis.gov.uk/mapping/mapping_2016/NAEIPointsSources_2016.xlsx

