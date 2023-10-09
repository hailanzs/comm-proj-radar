
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy
import scipy.io as sio

if __name__ == "__main__":
    # TODO: put path to the data captured folder
    datapath = r"/Users/shanbhag/Documents/School/comm-proj-radars"
    # TODO: put experiment name
    filename = r"1"

    # load the data
    bin_data = sio.loadmat(os.path.join(datapath,"rdc_" + filename + '.mat'))
    raw_data = np.array(bin_data['data_raw'])

    print("You captured %d frames, for %d TX, %d Rx, and %d adc samples" % raw_data.shape)

    rfft = scipy.fft.fft(raw_data, axis=3)
    print(rfft.shape)

    plt.plot(abs(np.squeeze(np.sum(rfft,axis=(0,2,1)))))
    plt.show()
