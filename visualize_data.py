
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy
import scipy.io as sio
import processing.save_adc_data as sd

if __name__ == "__main__":

    # TODO: Put the *name* of your .bin file here (excluding the .bin)
    filename = r"1"

    # TODO: Put the *path* to the project folder
    home_dir = r"/Users/shanbhag/Documents/School/comm-proj-radars"

    # TODO: Put the path (relative to home_dir) of the captured data folder
    capture_data_dir = r"recoreded_data"

    # TODO: Put the path (relative to home_dir) and name of the JSON files (exlude the .setup.json and .mmwave.json)
    json_filename = r"scripts/chirp1"

    ############################# reformat the data #############################

    if not os.path.exists(os.path.join(home_dir,"rdc_" + filename + '.mat')):
        sd.save_adc_data(filename, home_dir, capture_data_dir, json_filename)

    ################################# load data #################################
    bin_data = sio.loadmat(os.path.join(home_dir,"rdc_" + filename + '.mat'))
    raw_data = np.array(bin_data['data_raw'])

    print("You captured %d frames, for %d TX, %d Rx, and %d adc samples" % raw_data.shape)

    ############################### process data! ################################

    # Range FFT
    rfft = scipy.fft.fft(raw_data, axis=3)

    # Plot the Range FFT
    plt.plot(abs(np.squeeze(np.sum(rfft,axis=(0,2,1)))))
    plt.show()
