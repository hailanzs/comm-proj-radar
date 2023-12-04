from multiprocessing import Process, Queue
import logging
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
import matplotlib.pyplot as plt
import numpy as np
import streaming._realtime_streaming as rtstream
import streaming.radar as radar
import os

rtt_path = r'C:\ti\mmwave_studio_02_01_01_00\mmWaveStudio\Clients\RtttNetClientController\RtttNetClientAPI.dll'
# create folders for saving data
home_dir = r'C:\Users\robin\Documents\EPFL\BA5\Comm_project\comm-proj-radar' # home directory path (of the project folder, full path)
exp_path = os.path.join(home_dir, r'record') # put the folder you want to save data to (full path)
exp_name = r'' # name of the file you want to save (no .bin) in this case this is a dummy file that you will dump data bc TI makes us
config_lua_script = r'2' # relative path to the lua scripts for continuous it in is the home dir(ex. scripts/1843_config_streaming.lua)
record_lua_script =r'scripts/1843_record.lua' # relative path to the lua scripts for recording it in is the home dir(ex. scripts/1843_record.lua)

# initialize the radar class, this runs .lua scripts from mmWaveStudio and captures data
radar1 = radar(home_dir, rtt_path, config_lua_script)

# check if you are maybbe accidently overwriting a file
if os.path.isfile((os.path.join(exp_path, r"%s.bin" % exp_name))):
    print("You have files created already so you might overwrite data!")
else:
    if not os.path.isdir(exp_path):
        os.mkdir(exp_path)

    # capture data and process it
    radar1.mmwave_capture(exp_name, exp_path,record_lua_script)

# To edit the plots and how they show up go to streaming._realtime_streaming.py
# Here we will run the plotting code to see data in realtime
rtstream.stream(1, radar1)



