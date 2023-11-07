import sys
import argparse
import socket
import numpy as np
import time
import cv2
from read_files import read_files

# import mmwave as mm
# from mmwave.dataloader import DCA1000, adc
import os
from socket_slave_horizontal import RESET, START, LAMBDA_4, VELOCITY
from radar import radar

class master_socket_class():
    def __init__(self):
        self.conn_active = False

    def wait_for_conn(self, PORT):
        HOST = ''  # accept connection from all IP
        # assuming only 1 socket is needed
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(30)
        self.s.bind((HOST, PORT))
        self.s.listen(1)
        self.conn, self.addr_slave = self.s.accept()

    def send_robot_cmd(self, mesg):
        self.conn_active = True
        mesg_encded = str(mesg).encode('utf-8')
        self.conn.send(mesg_encded)
        ACK = self.conn.recv(4)

def main(opt):
    TCP_port = 50007
    # estabilish a socket connection with the slave PC and initialize the radar
    # initialize socket and radar
    master_socket = master_socket_class()
    radar1 = radar()

    # create folders for saving data
    home_dir = os.path.expanduser('~')
    exp_path = os.path.join(home_dir, r'OneDrive - epfl.ch\berry-data\measured', '%s' % opt.date)
    print(os.path.join(exp_path, r"exp%d_x0_Raw0.bin" % opt.expIdx))
    if os.path.isfile((os.path.join(exp_path, r"exp%d_x0_Raw_0.bin" % opt.expIdx))):
        print("You have files created already so synchronization will be an issue!")
        return
    if not os.path.isdir(exp_path):
        os.mkdir(exp_path)

    # reset the arm to the starting position
    print("Waiting for connection with Robot PC estabilished")
    master_socket.wait_for_conn(TCP_port)
    print("Connection with Robot PC estabilished")
    master_socket.send_robot_cmd("%s,%d,%f,%d" % (str(opt.date), opt.expIdx, time.time(), opt.x_stps))
    time.sleep(1)
    master_socket.send_robot_cmd(str(RESET))
    time.sleep(10)
    if False:
        time.sleep(10)
    if False: # if want to take picture of setup prior, set True
        camera = cv2.VideoCapture(1)
        for i in range(2):
            return_value, image = camera.read()
            cv2.imwrite(os.path.join(exp_path, str(opt.expIdx) + ".jpg"), image)
        del(camera)

    # return
    stp_size = opt.x_stps // 2
    reind = np.array([0], dtype=int)
    for i in np.concatenate((np.arange(0,stp_size,2),np.arange(1,stp_size,2))):
        if i%2 == 1:
            reind = np.concatenate((reind,np.arange(i,opt.x_stps,stp_size)[::-1]))
        else:
            reind = np.concatenate((reind,np.arange(i,opt.x_stps,stp_size)))
    reind = np.concatenate((reind,np.array([reind[-1]])))
    reind[0] = reind[1]
    print(reind)
    # capture data and process it
    for x in reind[1:-1]: 
        cmd = START + x
        print(str(cmd) + "," + str(opt.z_stps))
        robot_cmd = str(cmd) + "," + str(reind[np.where(reind[1:-1]==x)[0][0]+2]+START) + "," + str(opt.z_stps)
        print(robot_cmd)
        radar1.mmwave_capture(opt.date, opt.expIdx, x)
        time.sleep(0.1)
        master_socket.send_robot_cmd(robot_cmd + "," + str(time.time()) + "," + "X")
        sleep_time = opt.z_stps * LAMBDA_4 * 1e3 / VELOCITY # calculate z axis time
        sleep_time += 4 #5 # x axis time is 2s always
        if False:
            if x % 4 == 1:
                sleep_time += 4
        sleep_time *= 1.2
        print(sleep_time)
        time.sleep(sleep_time)

    # master_socket.send_robot_cmd(str(RESET))
    # time.sleep(1)
    read_files(opt.date, opt.expIdx)

def Options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=str, default='0414', help='What exp idx.')
    parser.add_argument('--x_stps', type=int, default=1, help='How many steps in the x direction.')
    parser.add_argument('--expIdx', type=int, default=1, help='Which exp we are doing now.')
    parser.add_argument('--z_stps', type=int, default=1, help='How many steps in the z direction.')
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    opt = Options()
    main(opt)

