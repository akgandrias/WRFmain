import numpy as np
import ftplib
from pathlib import Path   
import os
import pygrib as pgr
import re
import datetime
from datetime import timedelta
from datetime import date
from datetime import datetime
import time
# -------------------------Downloading ECMWF data for processing----------------------


# Define the path of the harmonie data to be processed
treepath = "/root/Build_WRF/data/ecmwf/"
# treepath = "testdownload/"

# Clear that folder containing old ecmwf data first.
[f.unlink() for f in Path(treepath).glob("*") if f.is_file()] 


# Defining model run time from either 00:00, 06:00, 12:00 or 18:00. Get the latest available data.
current_time = datetime.utcnow()

if current_time.hour <= 6:
    model_run_time = datetime(current_time.year,current_time.month,current_time.day-1,18,0)

if current_time.hour > 6 and current_time.hour <= 12:
    model_run_time = datetime(current_time.year,current_time.month,current_time.day,0,0)

if current_time.hour > 12 and current_time.hour <= 18:
    model_run_time = datetime(current_time.year,current_time.month,current_time.day,6,0)

if current_time.hour > 18:
    model_run_time = datetime(current_time.year,current_time.month,current_time.day,12,0)

#Get the analysis data
M2Dname = 'M2D'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'00'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'001'
A2Dname = 'A2D'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'00'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'001'


#Add a list of required files to be checked before downloading the data
filelist = []
d01list = []
d02list = []

#Fix this before going live!!!!!!!!!!!!!! :)

A1Sname2 = 'A1S'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'00'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'011'
M1Sname2 = 'M1S'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'00'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'011'

#Forecast data from timestep 0
filelist.append(A1Sname2)
filelist.append(M1Sname2)

d01A1Sname2 = 'wrfout_d01_'+str(model_run_time.year)+'-'+str(model_run_time.month).zfill(2)+'-'+str(model_run_time.day).zfill(2)+'_'+str(model_run_time.hour).zfill(2)+':'+str(model_run_time.minute).zfill(2)+':'+str(model_run_time.second).zfill(2)
d02A1Sname2 = 'wrfout_d02_'+str(model_run_time.year)+'-'+str(model_run_time.month).zfill(2)+'-'+str(model_run_time.day).zfill(2)+'_'+str(model_run_time.hour).zfill(2)+':'+str(model_run_time.minute).zfill(2)+':'+str(model_run_time.second).zfill(2)

d01list.append(d01A1Sname2)
d02list.append(d02A1Sname2)


#---------------------------------------------------------#

#Analysis data
# filelist.append(M2Dname)
# filelist.append(A2Dname)
#Forecast data 54 hours ahead
simulation_time = 20
for x in range(1,simulation_time+1):
    
    model_timestep_date = model_run_time + timedelta(hours=x)
    M1Sname = 'M1S'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'00'+str(model_timestep_date.month).zfill(2)+str(model_timestep_date.day).zfill(2)+str(model_timestep_date.hour).zfill(2)+'001'
    A1Sname = 'A1S'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'00'+str(model_timestep_date.month).zfill(2)+str(model_timestep_date.day).zfill(2)+str(model_timestep_date.hour).zfill(2)+'001'
    filelist.append(M1Sname)
    filelist.append(A1Sname)

    d01A1Sname = 'wrfout_d01_'+str(model_timestep_date.year)+'-'+str(model_timestep_date.month).zfill(2)+'-'+str(model_timestep_date.day).zfill(2)+'_'+str(model_timestep_date.hour).zfill(2)+':'+str(model_timestep_date.minute).zfill(2)+':'+str(model_timestep_date.second).zfill(2)
    d02A1Sname = 'wrfout_d02_'+str(model_timestep_date.year)+'-'+str(model_timestep_date.month).zfill(2)+'-'+str(model_timestep_date.day).zfill(2)+'_'+str(model_timestep_date.hour).zfill(2)+':'+str(model_timestep_date.minute).zfill(2)+':'+str(model_timestep_date.second).zfill(2)
    d01list.append(d01A1Sname)
    d02list.append(d02A1Sname)


print(filelist)

d01name = 'd01name.txt'
d02name = 'd02name.txt'
file = open(d01name,'w')
for item in d01list:
	file.write(item+"\n")
file.close()            

file = open(d02name,'w')
for item in d02list:
	file.write(item+"\n")
file.close()            


            

# Get data from the FTP server
HOSTNAME = "212.55.53.90"
USERNAME = "dmi-ecmwf"
PASSWORD = "hdl3YLDD6bajQayY"
ftp_server = None


#Check if files in filelist are an element of the FTP server's filelist
list1 = []
for filename in filelist:
    if ftp_server is None:
        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

    if filename in ftp_server.nlst():
        list1.append(1)
    else:
        list1.append(0)

        
        
print(list1)
k=0
k1=0
while True:        
    
    # If all elements are True (1), all required files exist. Data will now be downloaded from the FTP server.

    if sum(list1) == len(list1): #Comparing sum by length. If they are equal, all cases are 1 (True)
        for filename in filelist:
#             connect(filename,treepath)
            with open(filename, 'wb') as file:
                finished = False
                while (not finished):
                    if ftp_server is None:
                        print("Connecting...")
                        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

                    try:
                        rest = file.tell()
                        if rest == 0:
                            rest = None
                            print("Starting new transfer...")
                        else:
                            print(f"Resuming transfer from {rest}...")
                        ftp_server.retrbinary(f"RETR {filename}", file.write, rest=rest)
                        os.rename(filename, treepath+filename)
                        print("Done")
                        finished = True
                    except Exception as e:
                        
                        #Break script with no data if less than 2 hours until next simulation.
                        if datetime.utcnow().hour > model_run_time.hour+10:
                            print(f"Failed to get the required data before time limit was up. Time is now {datetime.utcnow().hour} utc, which is past {model_run_time.hour+10} utc")
                            break
                        sec = 10
                        ftp_server = None
                        print(f"Transfer failed: {e}, will retry in {sec} seconds...")
                        time.sleep(sec)
        break
    
    # At least one element is False. Therefore not all the files exist. Run FTP commands again
    else:
        print('Oh well...')
        time.sleep(60) # wait 1 minute before checking again
        
        #Break script with no data if less than 2 hours until next simulation.
        if datetime.utcnow().hour > model_run_time.hour+10:
            print(f"Failed to get the required data before time limit was up. Time is now {datetime.utcnow().hour} utc, which is past {model_run_time.hour+10} utc")
            break

#####-----Filter out the large-domain data from the sl dataset----#
A1Sname2 = 'A1S'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'00'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'011'
grbs = pgr.open(treepath+A1Sname2)
grbout = open(treepath+'sl'+A1Sname2,'wb')
for grb in grbs:
    if grb['latitudeOfLastGridPointInDegrees'] == 57.5:
        grbout.write(grb.tostring())

grbout.close

for x in range(1,simulation_time+1):
    
    model_timestep_date = model_run_time + timedelta(hours=x)
    A1Sname = 'A1S'+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'00'+str(model_timestep_date.month).zfill(2)+str(model_timestep_date.day).zfill(2)+str(model_timestep_date.hour).zfill(2)+'001'
    grbs = pgr.open(treepath+A1Sname)
    grbout = open(treepath+'sl'+A1Sname,'wb')
    for grb in grbs:
        if grb['latitudeOfLastGridPointInDegrees'] == 57.5:
            grbout.write(grb.tostring())

    grbout.close

#Only running fron 01 to 02, not the full run yet.
#model_run_time = model_run_time
model_end_time = model_run_time + timedelta(days=0, hours=simulation_time)
print(model_run_time)
print(model_end_time)


#Define the length of this simulation in days, hours, minutes, seconds (for when editing the namelist.input file)
# rundays = 
runhours = simulation_time

with open('/root/Automatization/namelist.wps', 'r') as f:
    data = f.readlines()

for i in range(len(data)):
    if 'start_date' in data[i]:
        data[i] = " start_date = '"+str(model_run_time.year)+"-"+str(model_run_time.month).zfill(2)+"-"+str(model_run_time.day).zfill(2)+"_"+str(model_run_time.hour).zfill(2)+":"+str(model_run_time.minute).zfill(2)+":"+str(model_run_time.second).zfill(2)+"','"+str(model_run_time.year)+"-"+str(model_run_time.month).zfill(2)+"-"+str(model_run_time.day).zfill(2)+"_"+str(model_run_time.hour).zfill(2)+":"+str(model_run_time.minute).zfill(2)+":"+str(model_run_time.second).zfill(2)+"',\n"
    elif 'end_date' in data[i]:
        data[i] = " end_date   = '"+str(model_end_time.year)+"-"+str(model_end_time.month).zfill(2)+"-"+str(model_end_time.day).zfill(2)+"_"+str(model_end_time.hour).zfill(2)+":"+str(model_end_time.minute).zfill(2)+":"+str(model_end_time.second).zfill(2)+"','"+str(model_end_time.year)+"-"+str(model_end_time.month).zfill(2)+"-"+str(model_end_time.day).zfill(2)+"_"+str(model_end_time.hour).zfill(2)+":"+str(model_end_time.minute).zfill(2)+":"+str(model_end_time.second).zfill(2)+"',\n"
    elif 'prefix' in data[i]:
        data[i] = " prefix = 'FILEsl',\n"

with open('/root/Automatization/namelist.wps', 'w') as f:
    f.writelines(data)

with open('/root/Automatization/namelist.input', 'r') as f:
    data = f.readlines()

for i in range(len(data)):
    if 'start_year' in data[i]:
        data[i] = " start_year = "+str(model_run_time.year)+","+str(model_run_time.year)+",\n"
    elif 'start_month' in data[i]:
        data[i] = " start_month   = "+str(model_run_time.month)+","+str(model_run_time.month)+",\n"
    elif 'start_day' in data[i]:
        data[i] = " start_day   = "+str(model_run_time.day)+","+str(model_run_time.day)+",\n"
    elif 'start_hour' in data[i]:
        data[i] = " start_hour   = "+str(model_run_time.hour)+","+str(model_run_time.hour)+",\n"

    # elif 'run_days' in data[i]:
    #     data[i] = " run_days = "+rundays+",\n"

    elif 'run_hours' in data[i]:
        data[i] = " run_hours = "+str(runhours)+",\n"


    # elif 'run_minutes' in data[i]:


    # elif 'run_seconds' in data[i]:
        
        
    elif 'end_year' in data[i]:
        data[i] = " end_year   = "+str(model_end_time.year)+","+str(model_end_time.year)+",\n"
    elif 'end_month' in data[i]:
        data[i] = " end_month   = "+str(model_end_time.month)+","+str(model_end_time.month)+",\n"
    elif 'end_day' in data[i]:
        data[i] = " end_day   = "+str(model_end_time.day)+","+str(model_end_time.day)+",\n"
    elif 'end_hour' in data[i]:
        data[i] = " end_hour   = "+str(model_end_time.hour)+","+str(model_end_time.hour)+",\n"
    
with open('/root/Automatization/namelist.input', 'w') as f:
    f.writelines(data)
