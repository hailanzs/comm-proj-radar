import os
import json
import singlechip_raw_data_reader_example as TI

# TODO: Put the filename of your experiment here
filename = "1"

# TODO: Put the path to the project folder
home_dir = "/Users/shanbhag/Documents/School/comm-proj-radars"

# TODO: Put the name of the captured data folder
capture_data_dir = ""

# Make sure this has the paths of the processed data you want
rawDataFileName = os.path.join(home_dir, capture_data_dir, f'raw_{filename}')
radarCubeDataFileName = os.path.join(home_dir, capture_data_dir, f'rdc_{filename}')

# Edit MMWAVE.JSON
mmwave_filename = os.path.join(home_dir, 'chirp1.mmwave.json')
with open(mmwave_filename, 'r') as mmwave_file:
    jsonData_mmwave = json.load(mmwave_file)

jsonText_mmwave = json.dumps(jsonData_mmwave, indent=4)
with open(mmwave_filename, 'w') as mmwave_file:
    mmwave_file.write(jsonText_mmwave)

# Edit SETUP.JSON
setup_filename = os.path.join(os.getcwd(), 'chirp1.setup.json')
with open(setup_filename, 'r') as setup_file:
    jsonData_setup = json.load(setup_file)

# This overwrites the location of the captured data to the correct date
dataFilePath = os.path.join(home_dir, capture_data_dir)
jsonData_setup['capturedFiles']['fileBasePath'] = dataFilePath

# Overwrite the raw file name
jsonData_setup['capturedFiles']['files']['processedFileName'] = f'{filename}_Raw_0.bin'
jsonData_setup['capturedFiles']['files']['rawFileName'] = f'{filename}_Raw_0.bin'

# Overwrite config used to correct computer
configUsed = mmwave_filename.replace('\\', '\\\\')
jsonData_setup['configUsed'] = configUsed

# Convert to JSON text
jsonText_setup = json.dumps(jsonData_setup, indent=4)
with open(setup_filename, 'w') as setup_file:
    setup_file.write(jsonText_setup)

# Call rawDataReader (You'll need to have the rawDataReader function defined or imported)
TI.rawDataReader(setup_filename, rawDataFileName, radarCubeDataFileName)
