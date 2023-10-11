-- capture_directory               =   "0616"
-- capture_file                    =   "exp1_x119"

--TODO: edit this path!!
SAVE_DATA_PATH = "C:\\Users\\SENS.C011437\\OneDrive - epfl.ch\\berry-data\\measured\\" .. capture_directory .. "\\" .. capture_file .. ".bin"

ar1.CaptureCardConfig_StartRecord(SAVE_DATA_PATH, 1)
ar1.StartFrame()

