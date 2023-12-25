from numpy.lib.function_base import unwrap
from mmwave.dataloader import DCA1000
import numpy as np
import time
from scipy.fftpack import fft
import processing.utility as utility

#######################################################
########## 1843 CODE#############################
########################################################
def producer_real_time_1843(q, index, lua_file):
    num_rx, num_tx, samples_per_chirp, periodicity, num_frames, chirp_loops, data_rate, freq_plot_len, range_plot_len = utility.read_radar_params(lua_file) 
    total = np.zeros(shape=(500, 512), dtype=np.complex128)
    dca = DCA1000()
    dca.sensor_config(chirps=3, chirp_loops=1, num_rx=4, num_samples=512)
    prev_time = time.time()
    while True:
        adc_data = dca.read()
        org_data = dca.organize(raw_frame=adc_data, num_chirps=num_tx*chirp_loops,
        num_rx=num_rx, num_samples=samples_per_chirp, num_frames=1, model='1843')
        x = 0

        x = np.sum(org_data, axis=(0, 1))
        x -= np.mean(x, axis=-1, keepdims=True)
        fx = fft(x, axis=-1)

        afx = np.squeeze(np.abs(fx))

        total[0:-1, :] = total[1:, :]
        total[-1:, :] = fx

        now = time.time()
        if now - prev_time > 0.1:
            q.put(["rfft", afx])
            prev_time = now