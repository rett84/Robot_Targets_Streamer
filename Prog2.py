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

    def __init__(self, server_address, port):
        threading.Thread.__init__(self)

        #declare instance variables       
        self.server_address = server_address
        self.port = port
        #self.size_r = size_r
        #self.array_r = array_r
        #self.size_s = size_s
        #self.array_s = array_s

         # Create a TCP/IP socket
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock1.connect((self.server_address, self.port))
#        self.sock1.setblocking(0)
#        self.sock1.settimeout(.1)
        print('connecting to', self.server_address, ' port ', self.port )
       

    def run(self):

        while 1:
            receive_data(self.sock1)
            send_data(self.sock1)



class ThreadedMoveRobot(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        #declare instance variables       
        #self.in_data_0 = in_data_0
        #self.out_data_0 = out_data_0
        #self.robot_pose_0 = robot_pose_0
       

    def run(self):

        while 1:
            move_robot()



# Function Definitions

def receive_data(sockp = socket):

        global from_plc     
        buf = 182 * 4
        data = sockp.recv(buf)
        qty_str = str(182) + 'f'
        data_arr = struct.unpack(qty_str, data)
        from_plc = data_arr




def send_data(sockp = socket):

    global to_plc
    data_arr = []*7

    for i in to_plc:
        data_arr.append(i)
        data = struct.pack('f', i)
        sockp.sendall(data)



def move_robot():

        #global to_plc
        #global from_plc
        global pose_i
        global vetor
        global index_exec

        
      
       # print ('Received', repr(from_plc))

        #if from_plc[180]==0:

        #    to_plc[0] = 2

        #elif from_plc[180]==1:
            
        if from_plc[181] == (index_exec+1):

            for i in range(0,30):
                vetor.x = from_plc[i] 
                vetor.y = from_plc[i+30] 
                vetor.z = from_plc[i+60] 
                vetor.rx = from_plc[i+90]  
                vetor.ry = from_plc[i+120]           
                vetor.rz = from_plc[i+150] 

          # #     print (repr(vetor.x), repr(vetor.y), repr(vetor.z))
                print (repr(from_plc[i]), repr(from_plc[i+30]), repr(from_plc[i+60]))
               

                pose_n1 = pose_i.Offset(from_plc[i],from_plc[i+30],from_plc[i+60])
           #     print(Pose_2_TxyzRxyz(robot.Pose()))
                
                #if vetor.x != 0 and vetor.y != 0 and vetor.z != 0:
                robot.MoveL(pose_n1)
            index_exec = index_exec + 1
                
            #to_plc[0] = 1
            to_plc[1] = index_exec
            
        
# End of Definitions


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

robot.setZoneData(100) # Set the rounding parameter (Also known as: CNT, APO/C_DIS, ZoneData, Blending radius, cornering, ...)
robot.setSpeed(1) # Set linear speed in mm/s

# Declare variables
to_plc = [0]*7
from_plc = [0]*182
pose_i = pose_ref
vetor = Vector()
index_exec = 0

# Create new threads
thread1 = ThreadedClient('192.168.40.1', 49151)
thread2 = ThreadedMoveRobot()



# Start new Threads
thread1.start()
thread2.start()

