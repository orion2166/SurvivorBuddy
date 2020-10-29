# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
from PositionFrame import PositionFrame
from ControlButtons import ControlButtons
from NotificationsFrame import NotificationFrame
from StatusBar import StatusBar
from SerialArmController import SerialArmController
from CamThread import camThread
from CamThread import responderCamThread
from datetime import datetime   #For log file formatting
from PIL import Image, ImageTk
from Audio import Audio
import os.path
import webbrowser
import cv2


class Application(tk.Frame):
    '''The main GUI class'''

    def __init__(self, master, **kwargs):
        '''
        The constructor for the Application class

        :param master: the Tk parent widget
        '''

        super().__init__(master, **kwargs)
        self.pack()
        self.taskbar_icon = tk.PhotoImage(file="SBLogo.png")
        self.master.call('wm', 'iconphoto', self.master._w, self.taskbar_icon)
        self.config(padx=16, pady=16)
        
        now = datetime.now()    #Create unique logfile for notifications and errors
        timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
        file_name = 'LOGFILE_' + timestamp +'.txt'        
        self.logFile = open(os.path.join(os.path.realpath('../logs/'), file_name) , 'w+')   #Save logfile to log folder

        # need the status bar to give to the arm controller
        self.status_bar = StatusBar(self)
        self.notifications_frame = NotificationFrame(self, self.logFile)

        self.serial_arm_controller = SerialArmController(self.status_bar, self.notifications_frame)

        self.thread1 = camThread("Survivor Cam", 1)
        #self.thread2 = responderCamThread("Responder Cam", 1, "Responder Cam Copy")
        self.thread1.start()
        #self.thread2.start()

        self.vid = cv2.VideoCapture(0)
        
        self.create_widgets(self.vid)

    def create_widgets(self, vid):
        '''Creates the widgets seen in the GUI'''

        self.menu_bar = tk.Menu(self)
        self.create_menu(self.menu_bar)
        
        self.canvas = tk.Canvas(self, width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.interval = 10
        self.update_image()

        self.position_frame = PositionFrame(self, self.serial_arm_controller, self.logFile)
        self.position_frame.pack(side=tk.LEFT)
        
        self.control_buttons = ControlButtons(self, self.serial_arm_controller, self.notifications_frame)
        self.control_buttons.pack(side=tk.LEFT)
        
        self.notifications_frame.pack(side=tk.LEFT)
        
        self.status_bar.pack()
        
        self.master.config(menu=self.menu_bar)

    def update_image(self):
        # Get the latest frame and convert image format
        self.image = cv2.cvtColor(self.vid.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.image = Image.fromarray(self.image) # to PIL format
        self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
 
        # Update image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
 
        # Repeat every 'interval' ms
        self.after(self.interval, self.update_image)

    def close_app(self):    #Had to make new quit function to close file
        '''Closes the GUI application'''

        self.logFile.close()
        self.quit()


    def create_menu(self, root_menu):
        '''
        Creates the main GUI menu

        :param root_menu: The root menu (self.menu_bar) that is instantiated in create_widgets()
        '''

        # File Menu
        self.file_menu = tk.Menu(root_menu, tearoff=0)
        #self.file_menu.add_command(label="Preferences", command=self.hello)
        self.file_menu.add_command(label="Quit", command=self.close_app)
        root_menu.add_cascade(label="File", menu=self.file_menu)
        
        # Device Menu
        self.device_menu = tk.Menu(root_menu, tearoff=0)
        self.device_menu.add_command(label="Refresh Devices", command=self.refresh_devices)
        self.device_menu.add_separator()
        
        root_menu.add_cascade(label="Device", menu=self.device_menu)

        #Survivor mic menu
        self.device_menu = tk.Menu(root_menu, tearoff=0)
        audio = Audio()
        inputDeviceList = audio.createInputDeviceList()
        outputDeviceList = audio.createOutputDeviceList()

        for key, value in inputDeviceList.items():
            print(key)
            print(value)
            self.device_menu.add_command(label=key, command=lambda value=value: audio.setSurvivorMic(value))
        self.device_menu.add_separator()
        root_menu.add_cascade(label="Mic Survivor", menu=self.device_menu)

        #Survivor speaker menu
        self.device_menu = tk.Menu(root_menu, tearoff=0)
        for key, value in outputDeviceList.items():
            self.device_menu.add_command(label=key, command=lambda value=value: audio.setSurvivorSpeaker(value))
        self.device_menu.add_separator()
        root_menu.add_cascade(label="Speaker Survivor", menu=self.device_menu)

        #Responder mic menu
        self.device_menu = tk.Menu(root_menu, tearoff=0)
        for key, value in inputDeviceList.items():
            self.device_menu.add_command(label=key, command=lambda value=value: audio.setResponderMic(value))
        self.device_menu.add_separator()
        root_menu.add_cascade(label="Mic Responder", menu=self.device_menu)

        #Responder speaker menu
        self.device_menu = tk.Menu(root_menu, tearoff=0)
        for key, value in outputDeviceList.items():
            self.device_menu.add_command(label=key, command=lambda value=value: audio.setResponderSpeaker(value))
        self.device_menu.add_separator()
        root_menu.add_cascade(label="Speaker Responder", menu=self.device_menu)
        
        # Help Menu
        self.help_menu = tk.Menu(root_menu, tearoff=0)
        self.help_menu.add_command(label="About Survivor Buddy 3.0", command=self.open_survivor_buddy_page)
        self.help_menu.add_command(label="User Manual", command=self.open_user_manual)
        self.help_menu.add_command(label="Programmer's Reference", command=self.open_programmer_reference)
        root_menu.add_cascade(label="Help", menu=self.help_menu)

    def refresh_devices(self):
        '''Refreshes the Devices menu'''

        self.device_menu.delete(2, 100)
        self.serial_arm_controller.update_devs()
        if not self.serial_arm_controller.devs:
            self.device_menu.add_command(label="No devices", state=tk.DISABLED)
        else:
            for dev in self.serial_arm_controller.devs:
                self.device_menu.add_command(
                    label="{}: {}".format(dev[0], dev[1]),
                    command=lambda: self.connect(dev)
                )        
            
    def connect(self, dev):
        '''
        Connects to the given device

        :param dev: The serial device to connect to
        '''

        self.serial_arm_controller.connect(dev[0])
        self.device_menu.add_command(
            label="Close Connection",
            command=self.close
        )
    
    def close(self):
        '''Closes the active serial connection'''

        self.device_menu.delete(2 + len(self.serial_arm_controller.devs))
        self.serial_arm_controller.close()

    def open_survivor_buddy_page(self):
        webbrowser.open("http://survivorbuddy.cse.tamu.edu/")
        
    def open_user_manual(self):
        webbrowser.open("https://docs.google.com/document/d/1V6gmVehsxrlFoc5FzThtdTNSovUbyU03AUEBfnAclKA/edit?usp=sharing")

    def open_programmer_reference(self):
        webbrowser.open("https://drive.google.com/a/tamu.edu/file/d/1pMKci4BTCTu7H6GREmmWEmBEgZ4klQWn/view?usp=sharing")

    def hello(self):
        '''
        A test function
        
        Simply prints "Hello from Menu" to the console and the NotificationsFrame
        '''
        print("Hello from Menu")
        self.notifications_frame.append_line("Hello from Menu")
        
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x600")
    root.state('zoomed')
    app = Application(master=root)
    app.master.title("Survivor Buddy 3.0")
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    app.mainloop()