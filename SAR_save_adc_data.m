% close all; %clear;% clc;

addpath(genpath('.\'))
addpath("/Users/shanbhag/Documents/Research/berry-project/singlechip_raw_data_reader_example")

base_name = "haila";
date_ref = "0222";

paths = strsplit(pwd, '\');
home_dir = strjoin(paths(1:3),'\');
home_dir = sprintf("%s/switchdrive/berry-data", home_dir);
yourFolder = sprintf("%s/calibrated/%s_calibrated", home_dir, date_ref);
if ~exist(yourFolder, 'dir')
   mkdir(yourFolder)
end

exp_idx = 1;
num_x_stp = 18;
num_z_stp = 180;

for x = 0:num_x_stp-1
    for z = 0:num_z_stp-1
    try
        file_end = sprintf('exp%d_x%d_z%d', exp_idx,x,z);
        rawDataFileName = sprintf('%s/calibrated/%s_calibrated/raw_%s',home_dir,date_ref,file_end);
        radarCubeDataFileName = sprintf('%s/calibrated/%s_calibrated/rdc_%s.mat',home_dir,date_ref,file_end);
        if(isfile(fullfile(radarCubeDataFileName)))
            continue;
        end
        radarCubeDataFileName = radarCubeDataFileName(1:end-4);

        %% EDIT MMWAVE.JSON
        mmwave_filename = sprintf('%s/scripts/currfile.mmwave.json', pwd);
        jsonText_mmwave = fileread(mmwave_filename);
        jsonData_mmwave = jsondecode(jsonText_mmwave); 
        jsonData_mmwave.mmWaveDevices.rfConfig.rlFrameCfg_t.numFrames = 4;
        jsonData_mmwave.mmWaveDevices.rfConfig.rlFrameCfg_t.framePeriodicity_msec = 20;

        jsonText = jsonencode(jsonData_mmwave);
        % Write to a json file
        fid = fopen(mmwave_filename, 'w');
        fprintf(fid, '%s', jsonText);
        fclose(fid);
        
        %% EDIT SETUP.JSON
        setup_filename = sprintf("%s/scripts/currfile.setup.json", pwd);
        jsonText_setup = fileread(setup_filename);
        % Convert JSON formatted text to MATLAB data types (3x1 cell array in this example)
        jsonData_setup = jsondecode(jsonText_setup); 

        %overwrite location of the captured data to correct date
        dataFilePath = sprintf('%s/measured/%s',home_dir,date_ref);
        jsonData_setup.capturedFiles.fileBasePath = dataFilePath;

        % overwrite the raw file name
        jsonData_setup.capturedFiles.files.processedFileName = sprintf('%s_Raw_0.bin', file_end);
        jsonData_setup.capturedFiles.files.rawFileName = sprintf('%s_Raw_0.bin', file_end);

        % overwrite config used to correct computer
        configUsed = strrep(mmwave_filename,'\','\\');
        jsonData_setup.configUsed = configUsed;
        % Convert to JSON text
        jsonText = jsonencode(jsonData_setup);
        % Write to a json file
        fid = fopen(setup_filename, 'w');
        fprintf(fid, '%s', jsonText);
        fclose(fid);

        rawDataReader(setup_filename, rawDataFileName, radarCubeDataFileName, 0)    
    catch
        'here'
    end
    end
end
