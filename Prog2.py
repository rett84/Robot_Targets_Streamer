# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
# Note: It is not required to keep a copy of this file, your python script is saved with the station
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox

import socket
import sys
import struct
import pickle

# Class Definitions

class Vector:
    def __init__(self, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0):
        self.x = x
        self.y = y
        self.z = z
        self.rx = rx
        self.ry = ry
        self.rz = rz
 

# Function Definitions

def receive_data(size, array, sockp = socket):

    buf = size * 4
    data = sockp.recv(buf)
    qty_str = str(size) + 'f'
    data_arr = struct.unpack(qty_str, data)

    for i in data_arr:
        array.append(i)


def send_data(size, array, sockp = socket):

    data_arr = []

    for i in array:
        data_arr.append(i)
        data = struct.pack('f', i)
        sockp.sendall(data)



# Initialize the RoboDK API
RDK = Robolink()


# turn off auto rendering (faster)
RDK.Render(False) 



# Promt the user to select a robot (if only one robot is available it will select that robot automatically)
robot = RDK.ItemUserPick('Select a robot', ITEM_TYPE_ROBOT)




# Turn rendering ON before starting the simulation
RDK.Render(True) 


# Abort if the user hits Cancel
if not robot.Valid():
    quit()

# Retrieve the robot reference frame
reference = robot.Parent()

# Use the robot base frame as the active reference
robot.setPoseFrame(reference)

# get the current orientation of the robot (with respect to the active reference frame and tool frame)
pose_ref = robot.Pose()

#pos_ref = pose_ref.Pos()

print(Pose_2_TxyzRxyz(pose_ref))

pose_i = pose_ref




# Create a TCP/IP socket
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.40.1', 49151)
print('connecting to {} port {}'.format(*server_address))

sock1.connect(server_address)

while True:

    try:

        coord = []
        send_values = []

        receive_data(182, coord , sock1)
        print ('Received', repr(coord))


         #declare vetor class
        vetor = [Vector()]*30

        print (coord[180])

        if coord[181]==0:

            send_values = [2]


        if coord[180]==1:
            for i in range(0,30):
                vetor[i].x = coord[i] 
                print(vetor[i].x)

            for i in range(31,60):
                vetor[i].y = coord[i] 
                print(vetor[i].y)

            for i in range(61,90):
                vetor[i].z = coord[i] 
                print(vetor[i].z)

            for i in range(91,120):
                vetor[i].rx = coord[i] 
                print(vetor[i].rx)

            for i in range(121,150):
                vetor[i].ry = coord[i] 
                print(vetor[i].ry)
            
            for i in range(151,180):
                vetor[i].rz = coord[i] 
                print(vetor[i].rz)



    #    receive_data(181, coord , sock1)
        send_data(7, send_values, sock1)
        


    finally:
       print('closing socket')
    #    sock1.close()
    
 




    #pose_n1 = pose_i.Offset(vetor.x,vetor.y, vetor.z).RelTool(0,0,0,vetor.rx,vetor.ry, vetor.rz)


    #robot.MoveL(pose_n1)




    # Done, stop program execution
    #quit()