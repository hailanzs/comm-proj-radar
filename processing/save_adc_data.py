import os
import json
import processing.singlechip_raw_data_reader_example as TI

######################################################################################################
def save_adc_data(filename, home_dir, capture_data_dir, json_filename, args):
    # If you have changed any chirp parameters then you need to load the args:
    # args = [num_tx, num_rx, adc_samples, chirp_loops, tx_en, rx_en]
    num_tx = args[0]
    num_rx = args[1]
    adc_samples = args[2]
    end_chirp = num_tx - 1
    chirp_loops = args[3]
    tx_en = args[4]
    rx_en = args[5]

    # Make sure this has the paths of the processed data you want
    rawDataFileName = os.path.join(home_dir, capture_data_dir, f'raw_{filename}')
    print(rawDataFileName)
    radarCubeDataFileName = os.path.join(home_dir, capture_data_dir, f'rdc_{filename}')
    print(radarCubeDataFileName)

    # Edit MMWAVE.JSON
    mmwave_filename = os.path.join(home_dir, '%s.mmwave.json' % json_filename)
    with open(mmwave_filename, 'r') as mmwave_file:
        jsonData_mmwave = json.load(mmwave_file)

    jsonData_mmwave['mmWaveDevices']['rfConfig']['rlChanCfg_t']['rxChannelEn'] = rx_en 
    jsonData_mmwave['mmWaveDevices']['rfConfig']['rlChanCfg_t']['txChannelEn'] = tx_en 
    jsonData_mmwave['mmWaveDevices']['rfConfig']['rlFrameCfg_t']['chirpEndIdx'] = end_chirp
    jsonData_mmwave['mmWaveDevices']['rfConfig']['rlFrameCfg_t']['chirpStartIdx'] = 0
    jsonData_mmwave['mmWaveDevices']['rfConfig']['rlProfiles']['rlProfileCfg_t']['numAdcSamples'] = adc_samples
    jsonData_mmwave['mmWaveDevices']['rfConfig']['rlFrameCfg_t']['numLoops'] = chirp_loops 

    jsonText_mmwave = json.dumps(jsonData_mmwave, indent=4)
    with open(mmwave_filename, 'w') as mmwave_file:
        mmwave_file.write(jsonText_mmwave)

    # Edit SETUP.JSON
    setup_filename = os.path.join(os.getcwd(), '%s.setup.json' % json_filename)
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


#################### helper ########################3
def read_lua(lua_file):
    with open(lua_file, 'r') as file:
        data = file.readlines()
    for i,line in enumerate(data):
        if("CHIRP_LOOPS =" in line):
            chirp_loops = int(line[13:line.find('-')].strip())
        if("NUM_RX =" in line):
            num_rx = int(line[9:line.find('-')].strip())
        if("NUM_TX =" in line):
            num_tx = int(line[9:line.find('-')].strip())
        if("ADC_SAMPLES =" in line):
            samples_per_chirp = int(line[14:line.find('-')].strip())
        if("PERIODICITY = " in line):
            periodicity = float(line[14:line.find('-')].strip())
        if("NUM_FRAMES = " in line):
            num_frames= float(line[12:line.find('-')].strip())


    return num_tx, num_rx, samples_per_chirp, chirp_loops