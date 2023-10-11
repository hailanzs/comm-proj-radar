

addpath(genpath('.\'))
% add the path to "singlechip_raw_data_reader_example", which should be in
% the TI folder somewhere
addpath("/Users/shanbhag/Documents/Research/berry-project/singlechip_raw_data_reader_example")


rawDataReader(setup_filename, rawDataFileName, radarCubeDataFileName, 0)