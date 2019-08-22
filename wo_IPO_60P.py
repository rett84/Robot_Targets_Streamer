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
import signal
import atexit
#import class1
from threading import Lock, Thread
lock = Lock()
from time import sleep  





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
        try:
            self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock1.connect((self.server_address, self.port))
    #        self.sock1.setblocking(0)
            self.sock1.settimeout(180)
            print('connecting to', self.server_address, ' port ', self.port )

        except socket.error as socketerror:
            connected = False
            print("Error: ", socketerror)
            while not connected:
                try:
                    self.sock1.connect((self.server_address, self.port))
                    connected = True
                except socket.error as socketerror:
                    print("Error: ", socketerror)
                    sleep( 10 )
        #finally:
        #    self.sock1.close()

    def run(self):
        print('Connected' )
        while 1:
            receive_data(self.sock1)
            send_data(self.sock1)
            #atexit.register(handle_exit)
#            self.sock1.shutdown(socket.SHUT_RDWR)


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

def handle_exit(sockp = socket):
        sockp.close()

def receive_data(sockp = socket):

        global from_plc     
        buf = 363 * 4
        data = sockp.recv(buf)
        qty_str = str(363) + 'f'
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
 #       global vetor
        global index_exec
        global line_decoded
        global r_speed
        k = 0       
        #r_speed = from_plc[362]
        step = from_plc[362]
        #robot.setSpeed(r_speed)

        vetor = []
      
       # print ('Received', repr(from_plc))

            
        if from_plc[361] == (index_exec+1):# and from_plc[362] < 2:

            for i in range(0,60):

                
                vetor.append(Vector(from_plc[i], from_plc[i+60], from_plc[i+120], from_plc[i+180], from_plc[i+240], from_plc[i+300]))
              
                if i ==30:
                    index_exec = index_exec + 1             
                    #to_plc[0] = 1
                    to_plc[1] = index_exec

                 
            for i in vetor:

                line_decoded = line_decoded + 1
                to_plc[5] = line_decoded
                to_plc[4] = k
                print (repr(i.x), repr(i.y), repr(i.z), repr(i.rx), repr(i.ry), repr(i.rz))
               
                #pose_n1 = pose_i.Offset(i.x,i.y,i.z).RelTool(0,0,0,i.rx, i.ry, i.rz) #motoman, abb
                #pose_n1 = TxyzRxyz_2_Pose([i.x, i.y, i.z, ((i.rx*pi)/180), ((i.ry*pi)/180), ((i.rz*pi)/180)])
                #pose_n2  = Pose_2_KUKA(pose_n1)
                pose_n1 = pose_i.Offset(i.x,i.y,i.z)*rotz(i.rz*pi/180)*roty(i.ry*pi/180)*rotx(i.rx*pi/180) #kuka
                #pose_n1 = transl(i.x,i.y,i.z)*rotz(i.rz*pi/180)*roty(i.ry*pi/180)*rotx(i.rx*pi/180)  


                # get the current robot joints
                #robot_joints = robot.Joints()

                
            
                # get the robot position from the joints (calculate forward kinematics)
                #robot_position = robot.SolveFK(robot_joints)


                #new_robot_position = transl([i.x,i.y,i.z])*rotx(i.rx*pi/180)*roty(i.ry*pi/180)*rotz(i.rz*pi/180)*robot_position      


                # calculate the new robot joints
                #pose_n1 = robot.SolveIK(new_robot_position)
  
                robot.MoveL(pose_n1)
                k = k+1

                if step ==3 and k>=59:
                    to_plc[1] = 0 #index_exec
                    to_plc[4] = 0 #line_decoded
                    to_plc[5] = 0 #k
                    index_exec = 0
                    line_decoded = 0
                    k = 0


              

          
            #index_exec = index_exec + 1             
            #to_plc[0] = 1
            #to_plc[1] = index_exec


        if from_plc[361] == 99999999:#move robot to home position
             robot.MoveL(pose_ref)
        
# End of Definitions


 # Initialize the RoboDK API
RDK = Robolink()

#RDK.setRunMode(RUNMODE_RUN_ROBOT)





# Promt the user to select a robot (if only one robot is available it will select that robot automatically)
#robot = RDK.ItemUserPick('Select a robot', ITEM_TYPE_ROBOT)

robot = RDK.AddFile(r'C:\RoboDK\Library\KUKA-KR-16-2.robot')
#robot = RDK.Item('KUKA KR 16 2')
#RDK.setWindowState(0)
#robot = RDK.Item('',ITEM_TYPE_ROBOT)

# Turn rendering ON before starting the simulation
#RDK.Render(True) 

# Turn Off automatic rendering (faster)
#RDK.Render(False) 


# Abort if the user hits Cancel
#if not robot.Valid():
#    quit()

# Retrieve the robot reference frame
reference = robot.Parent()

# Use the robot base frame as the active reference
robot.setPoseFrame(reference)


# Connect to the robot using default connetion parameters

#success = robot.Connect()

#status, status_msg = robot.ConnectedState()

#if status != ROBOTCOM_READY:

#    # Stop if the connection did not succeed

#    raise Exception("Failed to connect: " + status_msg)

 

# #Set to run the robot commands on the robot



## Note: This is set automatically if we use

#robot.Connect() #through the API
#robot.ConnectionParams()
#robot.setJoints([0,-20,-115,0,-90,0])
#robot.setJoints([0,0,0,0,0,180])

# get the current orientation of the robot (with respect to the active reference frame and tool frame)
pose_ref = robot.Pose() #home position

#pos_ref = pose_ref.Pos()

print(Pose_2_TxyzRxyz(pose_ref))

robot.setZoneData(100) # Set the rounding parameter (Also known as: CNT, APO/C_DIS, ZoneData, Blending radius, cornering, ...)
robot.setSpeed(50) # Set linear speed in mm/s

# Declare variables
to_plc = [0]*7
from_plc = [0]*363
pose_i = pose_ref
#vetor = [Vector()]*30

index_exec = 0
line_decoded = 0
r_speed = 0
# Create new threads
thread1 = ThreadedClient('192.168.40.1', 49151)
thread2 = ThreadedMoveRobot()



# Start new Threads
thread1.start()
thread2.start()