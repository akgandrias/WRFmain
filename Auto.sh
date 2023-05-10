#!/bin/bash

rm -r /home/wrfmain/Documents/wrfoutput/
rm /root/Automatization/wrfout_d0*
rm /root/Build_WRF/WRF-4.4-ARW/run/wrfout_d0*

#-------This is the WPS part of the script!--------#

#Get the lates data from the ECMWF server
python3 /root/Automatization/get-ecmwf-data.py

#Move the edited namelists into the WPS and WRF directories
cp /root/Automatization/namelist.wps /root/Build_WRF/WPS-4.4/
cp /root/Automatization/namelist.input /root/Build_WRF/WRF-4.4-ARW/run/

#Run Geogrid (only needed the first time, but takes no time to initialize)
cd /root/Build_WRF/WPS-4.4/
./geogrid.exe

#Remove old Ungrib and Metgrid files
rm /root/Build_WRF/WPS-4.4/FILEsl*
rm /root/Build_WRF/WPS-4.4/FILEml*
rm /root/Build_WRF/WPS-4.4/PRES:*
rm /root/Build_WRF/WPS-4.4/met_em.d*

#Assign the surface Vtable in the WPS before running Ungrib for surface parameters
cp /root/Automatization/Vtable.sl /root/Build_WRF/WPS-4.4/Vtable
./link_grib.csh /root/Build_WRF/data/ecmwf/slA1S*
./ungrib.exe


#Run ungrib with model-level parameters
cd /root/Automatization/
python3 /root/Automatization/edit-ml-namelist-wps.py
cp /root/Automatization/Vtable.ml /root/Build_WRF/WPS-4.4/Vtable
cd /root/Build_WRF/WPS-4.4/
./link_grib.csh /root/Build_WRF/data/ecmwf/M1S*
./ungrib.exe

#Interpolate with calc_ecmwf_p.exe
cp /root/Automatization/ecmwf_coeffs /root/Build_WRF/WPS-4.4/
./util/calc_ecmwf_p.exe

#Run Metgrid
./metgrid.exe

#---------------------------------------------------------#
#-------This is the WRF (easy) part of the script!--------#

cd /root/Build_WRF/WRF-4.4-ARW/run/

#Removing old met_em links
rm /root/Build_WRF/WRF-4.4-ARW/run/met_em.d0*

ln -sf /root/Build_WRF/WPS-4.4/met_em* .

mpirun -np 30 ./real.exe

mpirun -np 30 ./wrf.exe

#End in the Automatization folder
cd /root/Automatization/

#Post-processing

mv /root/Build_WRF/WRF-4.4-ARW/run/wrfout_d0* /root/Automatization/

#python3 /root/Automatization/wrfgraphics.py
python3 mv-wrfout-data.py
