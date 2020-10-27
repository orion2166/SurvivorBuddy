import cv2
import threading

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

class responderCamThread(threading.Thread):
    def __init__(self, previewName, camID, previewName2):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.previewName2 = previewName2
        self.camID = camID
    def run(self):
        responderCamPreview(self.previewName, self.camID, self.previewName2)

def responderCamPreview(previewName, camID, previewName2):
    cv2.namedWindow(previewName)
    cv2.namedWindow(previewName2)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        cv2.imshow(previewName2, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)
    cv2.destroyWindow(previewName2)