import os
from realtime_streaming.radar import radar

def main():
    # initialize radar
    radar1 = radar()

    # create folders for saving data
    exp_path = r'' # put the folder you want to save data to (full path)
    exp_name = r'' # name of the file you want to save
    print(os.path.join(exp_path, r"exp%d_x0_Raw0.bin" % exp_name))

    if os.path.isfile((os.path.join(exp_path, r"exp%d_x0_Raw_0.bin" % exp_name))):
        print("You have files created already so you might overwrite data!")
        return
    
    if not os.path.isdir(exp_path):
        os.mkdir(exp_path)

    # capture data and process it
    radar1.mmwave_capture(exp_path, exp_name)

if __name__ == "__main__":

    main()

