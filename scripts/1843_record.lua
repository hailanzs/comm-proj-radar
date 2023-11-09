capture_directory               =   "0616"

--TODO: edit this path!! (to where you want to save it)
SAVE_DATA_PATH = "C:\\Users\\robin\\Documents\\Communication\\comm-proj-radar\\record\\" .. capture_file .. ".bin"

-- this line configures where to save the data: it saves it to SAVE_DATA_PATH in a *.bin
ar1.CaptureCardConfig_StartRecord(SAVE_DATA_PATH, 1)
-- this line starts the radar transmitting
ar1.StartFrame()

