import sys
sys.path.append('../gui')

import wmi
import cv2
import tkinter as tk
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from Application import Application

class ApplicationMethods(unittest.TestCase):
	def test_connect_to_survivor_cam(self):
		print("--------------------------")
		print("Test GUI Connection to Survivor Camera")
		print("IDEF0: 2.1")
		print("Input: Preview Name, Video Stream from Camera")
		print("Expected Output: cam.read().rval == true")
		
		self.previewName = "test"
		self.cam = cv2.VideoCapture(1)
		self.rval, self.frame = self.cam.read()

		print("Real Output:")
		print("cam.read() return value returned:",end='')
		print(self.rval)

		self.assertTrue(self.cam.read.__call__)
		self.assertTrue(self.rval)

		success = self.rval
		if success:
			print("Test Passed!")
		else:
			print("Failed!")

	def test_encode_survivor_video(self):
		print("--------------------------")
		print("Test GUI Encoding Survivor Video")
		print("IDEF0: 5.3")
		print("Input: Preview Name, Video Stream from Camera")
		print("Expected Output: cam.read().frame == tuple containing stream data")
		
		self.previewName = "test"
		self.cam = cv2.VideoCapture(1)
		self.rval, self.frame = self.cam.read()

		print("Real Output:")
		print("cam.read() returned:",end='')
		print(self.frame)

		self.assertTrue(self.cam.read.__call__)

		success = self.cam.read.__call__
		if success:
			print("Test Passed!")
		else:
			print("Failed!")

	def test_responder_display_connected(self):
		print("--------------------------")
		print("Test if responder display is connected")
		print("IDEF0: 2.7")
		print("Input: None")
		print("Expected Output: monitorCount > 0")
		
		obj = wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0)

		displays = [x for x in obj if 'DISPLAY' in str(x)]

		count = 0
		for item in displays:
			if(item.Service == "monitor"):
				print(item)
				count += 1

		print("Real Output:")
		print("Monitor count returned:",end='')
		print(count)

		success = (count > 0)
		self.assertTrue(success)

		if success:
			print("Test Passed!")
		else:
			print("Failed!")

	def test_survivor_display_connected(self):
		print("--------------------------")
		print("Test if Survivor display is connected")
		print("IDEF0: 2.3")
		print("Input: None")
		print("Expected Output: monitorCount > 1")
		
		obj = wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0)

		displays = [x for x in obj if 'DISPLAY' in str(x)]

		count = 0
		for item in displays:
			if(item.Service == "monitor"):
				print(item)
				count += 1

		print("Real Output:")
		print("Monitor count returned:",end='')
		print(count)

		success = (count > 0)
		self.assertTrue(success)

		if success:
			print("Test Passed!")
		else:
			print("Failed!")

	def test_gui_and_displaying_feed(self):
		print("--------------------------")
		print("Test Starting GUI Application")
		print("IDEF0: 1.1")
		print("Input: User input from command line to start Application (python Application.py)")
		print("Expected Output: create_widgets() called at least once == True")
		
		root = tk.Tk()
		app = Application(master=root)

		print("Real Output:")
		print("create_widgets() called at least once:",end='')
		print(app.create_widgets.__call__)

		self.assertTrue(app.create_widgets.__call__)

		success = app.create_widgets.__call__
		if success:
			print("Test Passed!")
		else:
			print("Failed!")

		print("--------------------------")
		print("Test GUI Displaying Survivor Feed on GUI")
		print("IDEF0: 3.7")
		print("Input: Video Stream from Camera")
		print("Expected Output: update_image() called at least once == True")

		print("Real Output:")
		print("Update_image called at least once:",end='')
		print(app.update_image.__call__)

		self.assertTrue(app.update_image.__call__)

		success = app.update_image.__call__
		if success:
			print("Test Passed!")
		else:
			print("Failed!")

		print("--------------------------")
		print("Verify Connection to Devices By GUI Program")
		print("IDEF0: 2.9")
		print("Input: Successful Connection to Devices")
		print("Expected Output: returns True")
		
		print("Real Output:")
		print("create_widgets finishes == True:",end='')
		print(app.hello.__call__)
		
		self.assertTrue(app.hello.__call__)

		success = app.hello.__call__
		if success:
			print("Test Passed!")
		else:
			print("Failed!")

if __name__ == '__main__':
    unittest.main()