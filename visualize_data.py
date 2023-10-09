import _process_data as processing

import numpy as np
import matplotlib.pyplot as plt
import os
import mat73

if __name__ == "__main__":
    # TODO: put path to the data captured folder
    datapath = r"/Users/shanbhag/Documents/School/comm-proj-radars"
    # TODO: put experiment name
    filename = r"rdc_exp1_x121"

    # load the data
    bin_data = mat73.loadmat(os.path.join(datapath,filename + '.mat'))
    raw_data = np.array(bin_data['radarCube']['data_raw'])

    print("You captured %d frames, for %d TX, %d Rx, and %d adc samples" % raw_data.shape)

    # process data
    rfft = processing.process_raw_data(raw_data)

    # visualize data
    print(rfft.shape)
    plt.plot(abs(np.squeeze(np.sum(rfft,axis=(0,1,2)))))
    plt.show()
