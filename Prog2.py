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
import threading
import class1
from threading import Lock, Thread
lock = Lock()



to_plc = [0]*7
from_plc = [0]*182
index = 0


# Class Definitions

class Vector:
    def __init__(self, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0):
        self.x = x
        self.y = y
        self.z = z
        self.rx = rx
        self.ry = ry
        self.rz = rz
 

class ThreadedClient(threading.Thread):

    def __init__(self, server_address, port, size_r, array_r, size_s, array_s):
        threading.Thread.__init__(self)

        #declare instance variables       
        self.server_address = server_address
        self.port = port
        self.size_r = size_r
        self.array_r = array_r
        self.size_s = size_s
        self.array_s = array_s

         # Create a TCP/IP socket
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock1.connect((self.server_address, self.port))
#        self.sock1.setblocking(0)
#        self.sock1.settimeout(.1)
        print('connecting to', self.server_address, ' port ', self.port )
       

    def run(self):

        while 1:
            receive_data(self.size_r, self.array_r, self.sock1)
            send_data(self.size_s, self.array_s, self.sock1)



class ThreadedMoveRobot(threading.Thread):

    def __init__(self, in_data_0, out_data_0, vetor_0, robot_pose_0):
        threading.Thread.__init__(self)

        #declare instance variables       
        self.in_data_0 = in_data_0
        self.out_data_0 = out_data_0
        self.vetor_0 = vetor_0
        self.robot_pose_0 = robot_pose_0
       

    def run(self):

        while 1:
            move_robot(self.in_data_0, self.out_data_0, self.vetor_0, self.robot_pose_0)



# Function Definitions

def receive_data(size, array, sockp = socket):


       
        buf = size * 4
        data = sockp.recv(buf)
        qty_str = str(size) + 'f'
        array = struct.unpack(qty_str, data)
        
        print ('Received', repr(array))


def send_data(size, array, sockp = socket):



    data_arr = []*size

    for i in array:
        data_arr.append(i)
        data = struct.pack('f', i)
        sockp.sendall(data)



def move_robot(in_data_1, out_data_1, vetor_1, robot_pose_1):



        if in_data_1[180]==0:

            out_data_1[0] = 2


        elif from_plc[180]==1:


            for i in range(0,30):
                vetor_1.x = in_data_1[i] 
            #     print(vetor.x)

                vetor_1.y = in_data_1[i+29] 
            #      print(vetor.y)


                vetor_1.z = in_data_1[i+59] 
            #      print(vetor.z)


                vetor_1.rx = in_data_1[i+89] 
            #      print(vetor.rx)

 
                vetor_1.ry = in_data_1[i+119] 
        #        print(vetor.ry)
            
                vetor_1.rz = in_data_1[i+149] 
            #       print(vetor.rz)


                pose_n1 = robot_pose_1.Offset(vetor_1.x,vetor_1.y, vetor_1.z).RelTool(0,0,0,vetor_1.rx,vetor_1.ry, vetor_1.rz)
            #    robot.MoveL(pose_n1)

            index = index + 1
            out_data_1[0] = 1
            
        

#    ##    finally:
#    #    #print('closing socket')
#    ##    sock1.close()
#    except:
#        print ("Error: unable to start thread")
 


    




#    #    # Done, stop program execution
#    #    #quit()










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






#declare vetor class
vetor = Vector()



# Create new threads

thread1 = ThreadedClient('192.168.40.1', 49151, 182, from_plc, 7, to_plc)
thread2 = ThreadedMoveRobot(from_plc, to_plc, vetor, pose_i)



# Start new Threads
thread1.start()
thread2.start()



#while 1:

#    try:



#    #    print ('Received', repr(from_plc))

#    #    if from_plc[180]==0:

#    #        to_plc[0] = 2


#    #    if from_plc[180]==1:


#    #        for i in range(0,30):
#    #            vetor.x = from_plc[i] 
#    #        #     print(vetor.x)

#    #            vetor.y = from_plc[i+29] 
#    #        #      print(vetor.y)


#    #            vetor.z = from_plc[i+59] 
#    #        #      print(vetor.z)


#    #            vetor.rx = from_plc[i+89] 
#    #        #      print(vetor.rx)

 
#    #            vetor.ry = from_plc[i+119] 
#    #    #        print(vetor.ry)
            
#    #            vetor.rz = from_plc[i+149] 
#    #        #       print(vetor.rz)


#    #            pose_n1 = pose_i.Offset(vetor.x,vetor.y, vetor.z).RelTool(0,0,0,vetor.rx,vetor.ry, vetor.rz)
#    #            robot.MoveL(pose_n1)

#    #        index = index + 1
#    #        to_plc[0] = 1
            
        

#    ##    finally:
#    #    #print('closing socket')
#    ##    sock1.close()
#    except:
#        print ("Error: unable to start thread")
 


    




#    #    # Done, stop program execution
#    #    #quit()