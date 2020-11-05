import cv2
import threading

class camThread(threading.Thread):
    def __init__(self, previewName, camID, cam):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.cam = cam
    def run(self):
        camPreview(self.previewName, self.cam)

def camPreview(previewName, cam):
    cv2.namedWindow(previewName)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if checkKey(key):  # exit on ESC
            break
    cv2.destroyWindow(previewName)

def checkKey(key):
    return key == 27