from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import pygrib as pgr
from PIL import Image
import datetime
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import os




#Moving the d01 data
with open('d01name.txt', 'r') as f:
    Lines = f.readlines()
    dirname = Lines[0][11:30]
    os.mkdir(dirname)
    os.mkdir(dirname+'/data')
    os.mkdir(dirname+'/data/d01')
    os.mkdir(dirname+'/data/d02')

    for line in Lines:
        wrf_out_file = line[0:30]
        if os.path.isfile(str(wrf_out_file))==True:
            os.rename(wrf_out_file, '/root/Automatization/'+dirname+'/data/d01/'+wrf_out_file)


#Moving the d02 data
with open('d02name.txt', 'r') as f:
    
    Lines = f.readlines()
    for line in Lines:
        wrf_out_file = line[0:30]
        if os.path.isfile(str(wrf_out_file))==True:
            os.rename(wrf_out_file, '/root/Automatization/'+dirname+'/data/d02/'+wrf_out_file)

userpath = '/home/wrfmain/Documents/wrfoutput/'
os.mkdir(userpath)
os.rename(dirname,userpath+dirname)
