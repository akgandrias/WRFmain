#!/bin/bash

#This script initializes the entire PC and sets it up for WRF and WPS

#Change timezone to UTC
timedatectl set-timezone UTC

#Update Ubuntu 20.04
apt-get update -y
apt-get upgrade -y

#Install the standard packages for this system
apt install openssh-server
systemctl status ssh
apt install xrdp -y
apt install git -y
apt install python3 -y
apt install pip -y


#Installing Python3 Libraries with pip
# pip install numpy matplotlib pandas ftplib pathlib rasterio Basemap os pygrib re datetime time
pip install numpy matplotlib pandas pathlib rasterio Basemap pygrib datetime

#Start installing WRF
#mkdir home/wrf/github-files/
#cd /home/wrf/github-files

# The install script is based on Bakamotas' automatic WRF installation script
# You can clone the repo here: git clone https://github.com/bakamotokatas/WRF-Install-Script
cd WRF-Install-Script/
sudo bash WRF4.4_Install.bash -arw

#Adding SRTM-topography to WRF
wget https://www2.mmm.ucar.edu/wrf/src/wps_files/topo_srtm_3s.tar.gz
tar -zxvf topo_srtm_3s.tar.gz
mv topo_srtm_3s /root/Build_WRF/WPS_GEOG/
rm topo_srtm_3s.tar.gz



# git clone --recurse-submodules https://github.com/wrf-model/WRF
# git clone https://github.com/wrf-model/WPS
# apt install csh gfortran m4 mpich libhdf5-mpich-dev libpng-dev libnetcdff-dev netcdf-bin ncl-ncarg build-essential


# wget https://www.ece.uvic.ca/~frodo/jasper/software/jasper-1.900.29.tar.gz
# tar xvf jasper-1.900.29.tar.gz 
# cd jasper-1.900.29/
# ./configure --prefix=/opt/jasper-1.900.29
# make
# make install

# cd /home/wrf/WRF/
# export NETCDF=/usr
# export NETCDF_classic=1
# ./wrf/WRF/configure 34 1

# 34
# 1
