import numpy as np
import time

import matplotlib.pyplot as plt
from mmwave.dataloader import DCA1000, adc
import scipy
import os
import clr

# helper functions
def replace_filename(file1, date, expIdx, x):
    with open(file1, 'r') as file:
        data = file.readlines()
    data[0] = 'capture_directory               =   "%s"\n' % date
    data[1] = 'capture_file                    =   "exp%d_x%d"\n' % (expIdx,x) 

    with open(file1, 'w') as file:
        file.writelines(data)

# radar class:
# initiates connection with mmWave Studio
# measures data
# can do processing if required later on
class radar():
    def __init__(self):
        self.captured = False
        self.chirp_loops = 1
        self.num_rx = 4
        self.num_tx = 2
        self.samples_per_chirp = 128 
        self.periodicity = 20
        self.homedirectory = os.path.expanduser('~')
        self.homedirectory = os.path.join(self.homedirectory,'Documents','berry-project')
        self.file1 = open(os.path.join(self.homedirectory,'scripts','1843_setup_1.lua'), 'r')
        Lines = self.file1.readlines()
        for line in Lines:
            if("CHIRP_LOOPS =" in line):
                self.chirp_loops = int(line[13:line.find('-')].strip())
            if("NUM_RX =" in line):
                self.num_rx = int(line[9:line.find('-')].strip())
            if("NUM_TX =" in line):
                self.num_tx = int(line[9:line.find('-')].strip())
            if("ADC_SAMPLES =" in line):
                self.samples_per_chirp = int(line[14:line.find('-')].strip())
            if("PERIODICITY = " in line):
                self.periodicity = float(line[14:line.find('-')].strip())

        self.data_rate = int(1 / (self.periodicity * 0.001) / 2)
        self.freq_plot_len = self.data_rate  // 2
        self.range_plot_len = self.samples_per_chirp
        self.power_dict = dict()
        self.RtttNetClientAPI = self.Init_RSTD_Connection( r'C:\ti\mmwave_studio_02_01_01_00\mmWaveStudio\Clients\RtttNetClientController\RtttNetClientAPI.dll')
    
    
    def Init_RSTD_Connection(self, RSTD_DLL_Path):
        RSTD_Assembly = clr.AddReference(RSTD_DLL_Path)
        import RtttNetClientAPI
        try:
            RtttNetClientAPI.RtttNetClient.IsConnected()
            Init_RSTD_Connection = 0
        except:
            Init_RSTD_Connection = 1
        if Init_RSTD_Connection:
            print('Initializing RSTD client')
            ErrStatus = RtttNetClientAPI.RtttNetClient.Init()
            if not ErrStatus == 0:
                print('Unable to initialize NetClient DLL')
                return
            print('Connecting to RSTD client')
            ErrStatus = RtttNetClientAPI.RtttNetClient.Connect('127.0.0.1',2777)
            if not ErrStatus == 0:
                print('Unable to connect to mmWaveStudio')
                print('Reopen port in mmWaveStudio. Type RSTD.NetClose() followed by RSTD.NetStart()')
                return
            time.sleep(1)

        print('Sending test message to RSTD')
        Lua_String = r'WriteToLog("Running script from MATLAB\\n", "green")'
        ErrStatus = RtttNetClientAPI.RtttNetClient.SendCommand(Lua_String)
        if not ErrStatus == (0, None):
            print ('mmWaveStudio Connection Failed')
        else:
            print('Test message success')
        return RtttNetClientAPI

    def mmwave_capture(self, date, expIdx, x):
        file1 = os.path.join(self.homedirectory,'scripts','1843_run.lua')
        file2 = file1.replace("\\", "\\\\\\\\") 
        Lua_String = 'dofile("'+ file2 + '")'
        # update the lua file with new location to save the data
        replace_filename(file1, date, expIdx, x)
        ErrStatus = self.RtttNetClientAPI.RtttNetClient.SendCommand(Lua_String)
        if not ErrStatus == (0, None):
            print ('The frame did not get collected :(')
        else:
            print('Frame collected!')
