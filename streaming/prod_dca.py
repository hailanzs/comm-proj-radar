from random import sample

from numpy.lib.function_base import unwrap
import mmwave as mm
from mmwave.dataloader import DCA1000, adc
import scipy
import matplotlib.pyplot as plt
import numpy as np
import time
import scipy.io as sio
import os
from datetime import datetime
import radar
# import cmath

## TODO: run mmWave studio and Lua code in background using python

########################################################
########## 1843 CODE#############################
########################################################
def producer_real_time_1843(q, index):
    
    print('')
    print("num tx: ", num_tx)
    print("num rx: ", num_rx)
    print("samples_per_chirp: ", samples_per_chirp)
    print("chirp_loops: ", chirp_loops) 
    print("PERIODICITY: ", periodicity) 
    print("NUM_FRAMES: ", NUM_FRAMES) 
    print("freq_plot_len: ", freq_plot_len) 
    print("range_plot_len: ", range_plot_len) 
    second_p = 0
    second_p_plot = 0
    frm_ctr = 0
    total = np.zeros(shape=(NUM_FRAMES, samples_per_chirp), dtype=np.complex128)
    unwrapped_phase = np.zeros(shape=(NUM_FRAMES), dtype=np.complex128)
    freq_spec = 0
    dca = DCA1000()
    dca.sensor_config(chirps=num_tx, chirp_loops=chirp_loops, num_rx=num_rx, num_samples=samples_per_chirp)
    prev_time = time.time()
    initial_time = time.time()
    while True:
        adc_data = dca.read()
        org_data = dca.organize(raw_frame=adc_data, num_chirps=num_tx*chirp_loops,
         num_rx=num_rx, num_samples=samples_per_chirp, num_frames=1, model='1843')
        frm_ctr+=1
        x = 0

        x = np.sum(org_data, axis=(0, 1))
        x -= np.mean(x, axis=-1, keepdims=True)
        fx = scipy.fft.fft(x, axis=-1)

        afx = np.squeeze(np.abs(fx))

        total[0:-chirp_loops, :] = total[chirp_loops:, :]
        total[-chirp_loops:, :] = fx
        # noramlized_total = total - total[0, 0, :]
        max_idx = np.argmax(np.sum(np.abs(total[3:]),axis=0))
        # print(max_idx)
        unwrapped_phase = np.unwrap(np.angle(total[:, max_idx]), axis=0)
        # print(max_idx+6)
        # if not PLOT_FFT:
        #     unwrapped_phase = scipy.signal.convolve(unwrapped_phase, arr, mode='valid', method='auto')
        # a, b = scipy.signal.butter(5, Wn=10, fs=500, btype='highpass')
        # unwrapped_phase = scipy.signal.lfilter(a,b,unwrapped_phase)
        unwrapped_phase_plot = scipy.signal.convolve(unwrapped_phase, arr, mode='valid', method='auto')
        unwrapped_phase_plot += second_p_plot - unwrapped_phase_plot[0]
        second_p_plot = unwrapped_phase_plot[1] 

        unwrapped_phase += second_p - unwrapped_phase[0]
        second_p = unwrapped_phase[1] 

        if PLOT_FFT:
            freq_spec = unwrapped_phase - np.mean(unwrapped_phase)
            # freq_spec = np.abs(scipy.fft.fft(freq_spec,data_rate))
            a,freq_spec = scipy.signal.welch(freq_spec,500)
            # freq_spec = np.log10(freq_spec)
            # freq_spec /= np.max(freq_spec)
        freq_spec = freq_spec[0:freq_plot_len]
        now = time.time()
        if now - prev_time > 0.1:
            q.put(["fft", afx])
            q.put(["freq", freq_spec])
            prev_time = now
