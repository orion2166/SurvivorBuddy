import cv2
import threading

class camThread(threading.Thread):

    def __init__(self, previewName, camID, cam):
        """Initializes the camera device"""
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.cam = cam
        self.rval = False

    def run(self):
        """Helper to start camera thread"""
        self.camPreview(self.previewName, self.cam)

    def camPreview(self, previewName, cam):
        """Creates responder video reading"""
        cv2.namedWindow(previewName)
        if cam.isOpened():  # try to get the first frame
            self.rval, frame = cam.read()
        else:
            self.rval = False

        while self.rval:
            cv2.imshow(previewName, frame)
            self.rval, frame = cam.read()
            key = cv2.waitKey(20)
            if checkKey(key):  # exit on ESC
                break
        cv2.destroyWindow(previewName)

    def closeCams(self):
        """Stops reading of camera"""
        self.rval = False

def checkKey(key):
    """Helper function for key"""
    return key == 27
