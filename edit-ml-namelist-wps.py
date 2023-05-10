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

with open('/root/Build_WRF/WPS-4.4/namelist.wps', 'r') as f:
    data = f.readlines()

for i in range(len(data)):
    if  'prefix' in data[i]:
        data[i] = " prefix = 'FILEml',\n"

with open('/root/Build_WRF/WPS-4.4/namelist.wps', 'w') as f:
    f.writelines(data)
