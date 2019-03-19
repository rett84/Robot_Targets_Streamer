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
import _thread

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

#def receive_data(size, array, sockp = socket):

#    buf = size * 4
#    data = sockp.recv(buf)
#    qty_str = str(size) + 'f'
#    data_arr = struct.unpack(qty_str, data)

#    for i in data_arr:
#        array.append(i)


#def send_data(size, array, sockp = socket):

#    data_arr = []

#    for i in array:
#        data_arr.append(i)
#        data = struct.pack('f', i)
#        sockp.sendall(data)


def s_r_data(size_r, array_r, size_s, array_s, sockp = socket):

    while 1:
    #    data_arr_r = []
        data_arr_s = []


        #receive
        buf = size_r * 4
        amount_expected = buf
    
 
        amount_received = 0
        while amount_received < amount_expected:
            data_r = sockp.recv(buf)
            amount_received += len(data_r)

        qty_str_r = str(size_r) + 'f'
        data_arr_r = struct.unpack(qty_str_r, data_r)

        array_r = data_arr_r

    
        #for i in data_arr_r:
        #    array_r.append(i)

        #send

        for j in array_s:
            data_arr_s.append(j)
            data_s = struct.pack('f', j)
            sockp.sendall(data_s)






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

#declare vetor class
vetor = Vector()

to_plc = [0]*7
from_plc = [0]*182
index = 0


while 1:

    try:

        _thread.start_new_thread(s_r_data,(182, from_plc, 7, to_plc ,sock1))

    #    print ('Received', repr(from_plc))

    #    if from_plc[180]==0:

    #        to_plc[0] = 2


    #    if from_plc[180]==1:


    #        for i in range(0,30):
    #            vetor.x = from_plc[i] 
    #        #     print(vetor.x)

    #            vetor.y = from_plc[i+29] 
    #        #      print(vetor.y)


    #            vetor.z = from_plc[i+59] 
    #        #      print(vetor.z)


    #            vetor.rx = from_plc[i+89] 
    #        #      print(vetor.rx)

 
    #            vetor.ry = from_plc[i+119] 
    #    #        print(vetor.ry)
            
    #            vetor.rz = from_plc[i+149] 
    #        #       print(vetor.rz)


    #            pose_n1 = pose_i.Offset(vetor.x,vetor.y, vetor.z).RelTool(0,0,0,vetor.rx,vetor.ry, vetor.rz)
    #            robot.MoveL(pose_n1)

    #        index = index + 1
    #        to_plc[0] = 1
            
        

    ##    finally:
    #    #print('closing socket')
    ##    sock1.close()
    except:
        print ("Error: unable to start thread")
 


    




    #    # Done, stop program execution
    #    #quit()