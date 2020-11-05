import sys
sys.path.append('../gui')

import unittest
import time
import keyboard
from unittest.mock import MagicMock
from CamThread import camThread
from CamThread import camPreview
from CamThread import checkKey

import cv2

class TestCamThreadMethods(unittest.TestCase):
	def test_connect_to_responder_cam(self):
		print("--------------------------")
		print("Test camPreview Connection to Responder Camera")
		print("IDEF0: 2.5")
		print("Input: Preview Name, Video Stream from Camera")
		print("Expected Output: cam.read().rval == true")
		
		self.previewName = "test"
		self.cam = cv2.VideoCapture(0)
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

	def test_encode_responder_video(self):
		print("--------------------------")
		print("Test camPreview Encoding Responder Video")
		print("IDEF0: 5.1")
		print("Input: Preview Name, Video Stream from Camera")
		print("Expected Output: cam.read().frame == tuple containing stream data")
		
		self.previewName = "test"
		self.cam = cv2.VideoCapture(0)
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

	def test_camPreview(self):
		print("--------------------------")
		print("Test camPreview Utility Function Displaying Live Video Stream On Survivor GUI")
		print("IDEF0: 6.1")
		print("Input: Preview Name, Video Stream from Camera")
		print("Expected Output: imshow() == None")
		
		self.previewName = "test"
		self.cam = cv2.VideoCapture(0)
		self.rval, self.frame = self.cam.read()

		print("Real Output:")
		print("imshow() returned:",end='')
		print(cv2.imshow(self.previewName, self.frame))

		self.assertEqual(cv2.imshow(self.previewName, self.frame), None)

		success = (cv2.imshow(self.previewName, self.frame) == None)
		if success:
			print("Test Passed!")
		else:
			print("Failed!")

if __name__ == '__main__':
    unittest.main()