# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
from PositionFrame import PositionFrame
from ControlButtons import ControlButtons
from NotificationsFrame import NotificationFrame
from StatusBar import StatusBar
from SerialArmController import SerialArmController
from datetime import datetime   #For log file formatting
import os.path
import webbrowser

class Testing(Tk.Frame):
	def __init__(self, master, **kwargs):
        '''
        The constructor for the Application class

        :param master: the Tk parent widget
        '''
        super().__init__(master, **kwargs)
        # need the status bar to give to the arm controller
        self.status_bar = StatusBar(self)
        self.notifications_frame = NotificationFrame(self, self.logFile)
        self.serial_arm_controller = SerialArmController(self.status_bar, self.notifications_frame)

	def tester(trying, recived, expected, txt_If_True = "Test Passed", txt_If_False = "Test Failed"):
		print("Trying Value: ", trying)
		print("Recieved Value: ",recieved)
		print("Expected Value: ", expected)
		if(recieved == expected):
			print(txt_If_True)
		else:
			print(txt_If_False)
		print("\n\n")

	# Function Block 1
	def test1_1(self):
		print("Tests for Function Block 1.1 from IDEF0:")
		app = Application(master = self.master)
		app.master.title("Survivor Buddy 3.0")
    	self.master.protocol("WM_DELETE_WINDOW", app.close_app)
    	app.mainloop()
    	tester("Did It Open","Opened Properly","Opened Properly")

	def test1_2(self): #test 1.2
		self.serial_arm_controller.connect(0)
		print("Tests for Function Block 1.2 from IDEF0:")
		tester("Comport 0",self.serial_arm_controller.is_connected,True)

	def test1_3(self):#test 1.3
		app = Application(master = self.master)
		print("Tests for Function Block 1.3 from IDEF0:")
		tester("Trying Device 0",1,app.connect(0))


	def test1_4(self): #test 1.4
		print("Tests for Function Block 1.4 from IDEF0:")
		status = "Connected"
		self.status_bar.set_status(status) #StatusBar.py [1.4]
		tester("Setting status to Connected",self.status_bar.status_text,"Connected")

		status = "Disconnected"
		self.status_bar.set_status(status) #StatusBar.py [1.4]
		tester("Setting status to Disconnected",self.status_bar.status_text,"Disconnected")


	# Function Block 3
	def test3_1(self):#test 3.1
		print("Tests for Function Block 3.1 from IDEF0:")
		self.serial_arm_controller.update_position([0,90,0]) #SerialArmController.py [3.1]
		tester("0, 90, 0",[self.serial_arm_controller.position.pitch,self.serial_arm_controller.position.yaw,self.serial_arm_controller.position.roll],[0,0,0])

		self.serial_arm_controller.update_position([45,135,45]) #SerialArmController.py [3.1]
		tester("45, 135, 45",[self.serial_arm_controller.position.pitch,self.serial_arm_controller.position.yaw,self.serial_arm_controller.position.roll],[45,45,45])

	def test3_2(self):#test 3.2
	def test3_3(self):#test 3.3
	def test3_4(self):#test 3.4

	def test3_5(self): #test 3.5
		print("Tests for Function Block 3.5 from IDEF0:")
		val = 90
		expectedPitch = bytes((0, val))
		expectedYaw =bytes((1, val+90))
		expectedRoll =bytes((2, val))
		tester("pitch = 90",self.serial_arm_controller.set_pitch(val), expectedPitch) #SerialArmController.py [3.5]
		tester("yaw = 90",self.serial_arm_controller.set_yaw(val), expectedYaw) #SerialArmController.py [3.5]
		tester("roll = 90",self.serial_arm_controller.set_roll(val), expectedRoll) #SerialArmController.py [3.5]

root = tk.Tk()
root.geometry("800x600")
app = Testing(master=root)
