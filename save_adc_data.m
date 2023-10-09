

addpath(genpath('.\'))
% TODO:  add the path to "singlechip_raw_data_reader_example", which should be in
% the TI folder somewhere
addpath("/Users/shanbhag/Documents/Research/berry-project/singlechip_raw_data_reader_example");

% TODO: put the filename of your experiment here
filename = "1";
% TODO: put the path to the project folder
home_dir = "";
% TODO: put the name of the captured data folder
capture_data_dir = "";

% make sure this has the paths of the processed data you want
rawDataFileName = sprintf('%s/%s/raw_%s',home_dir, capture_data_dir, filename);
radarCubeDataFileName = sprintf('%s/%s/rdc_%s.mat',home_dir, capture_data_dir, filename);
radarCubeDataFileName = radarCubeDataFileName(1:end-4);

%% EDIT MMWAVE.JSON
mmwave_filename = sprintf('%s/chirp1.mmwave.json', home_dir);
jsonText_mmwave = fileread(mmwave_filename);
jsonData_mmwave = jsondecode(jsonText_mmwave); 

jsonText = jsonencode(jsonData_mmwave);
% Write to a json file
fid = fopen(mmwave_filename, 'w');
fprintf(fid, '%s', jsonText);
fclose(fid);

%% EDIT SETUP.JSON
setup_filename = sprintf("%s/chirp1.setup.json", pwd);
jsonText_setup = fileread(setup_filename);
% Convert JSON formatted text to MATLAB data types (3x1 cell array in this example)
jsonData_setup = jsondecode(jsonText_setup); 

%TODO: make sure the captured data folder is corred below (replace "measured") 
% this overwrite location of the captured data to correct date
dataFilePath = sprintf('%s/measured/%s',home_dir,filename);
jsonData_setup.capturedFiles.fileBasePath = dataFilePath;

% overwrite the raw file name
jsonData_setup.capturedFiles.files.processedFileName = sprintf('%s_Raw_0.bin', filename);
jsonData_setup.capturedFiles.files.rawFileName = sprintf('%s_Raw_0.bin', filename);

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