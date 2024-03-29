;
; script for ensuring that the NAEI emission file metadata conforms with the
;  metadata expected by EMEP
;


;
;  Source variable metadata (as generated by anthro_emiss):
;
;	float E_pm25_sec09(Time, emissions_zdim_stag, south_north, west_east) ;
;		E_pm25_sec09:MemoryOrder = "XYZ" ;
;		E_pm25_sec09:description = "EMISSIONS" ;
;		E_pm25_sec09:units = "ug m^-2 s^-1" ;
;		E_pm25_sec09:stagger = "Z" ;
;		E_pm25_sec09:FieldType = 104 ;
;
;
;  Changes / additions needed:
;
;      species='pm25' (or 'co','sox',etc) (match according to emission variable)
;      sector=[1..13]  (match according to final secXX string)
;      units='mg/m2/year'
;      factor=3.1536e4 (convert from ug/m2/s to mg/m2/year)
;      country_ISO='GB'  (fixed value for all data)
;
;  Changes / additions needed for global attributes:
; 
;      periodicity = 'yearly'
;      projection = 'native'
;


begin

sourcedir = "output/"
datafile = "wrf_emissions_d03.nc"


;var_list = (/"voc","co","nh3","nox","sox","pm25","pmco"/)



FILE=addfile(sourcedir+datafile,"w")


;; add global attributes to the file

globalAtt = True
globalAtt@periodicity = "yearly"
globalAtt@projection  = "native"

fileattdef(FILE,globalAtt)


;; loop through all variables - process only emission variables

variable_list = getfilevarnames(FILE)

varAtt = True
varAtt@country_ISO = "GB"
varAtt@units       = "mg/m2/year"

do ii = 0,dimsizes(variable_list)-1
	vname = variable_list(ii)
	vlist := str_split(vname,"_")
	vardata := FILE->$vname$
	
	if(vlist(0).eq."E")
		print("processing variable: "+vname)
		
		;; copy variable name to species name (a lot of assumptions here...)
		varAtt@species     = vlist(1)
		
		;; determine sector value to set
		if(vlist(2).eq."point")
			varAtt@sector = 13  ;; set mixed point sources to "other" for the moment
		else
			varAtt@sector = toint(str_sub_str(vlist(2),"sec","")) ;; strip "sec" from the front of sector string, and convert to integers
		end if
		
		;; check to see what scaling factor we should be using
		currunit = vardata@units
			
		if(currunit .eq. "ug m^-2 s^-1")
			varAtt@factor      = 3.1536e4
			varAtt@oldunits    = currunit
		else
			print("unsupported unit: "+currunit)
			varAtt@factor      = -9999.9
			varAtt@oldunits    = currunit
		end if
		
		;; apply attributes to the file variable
		filevarattdef(FILE,vname,varAtt)
		
	else
		print("not processing variable: "+vname)
	end if

end do



end



