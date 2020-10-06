# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk


class ControlButtons(tk.Frame):
    '''Buttons to control the Survivor Buddy 3.0 arm'''

    def __init__(self, master, arm_controller, notifications, **kwargs):
        '''
        The constructor for ControlButtons

        :param master: The Tk parent widget
        :param arm_controller: The SerialArmController being used
        :param notifications: The NotificationsFrame being used
        '''

        super().__init__(master, **kwargs)
        self.serial_arm_controller = arm_controller
        self.notifications_frame = notifications
        self.open_close_status = "CLOSED"
        self.orientation = "PORTRAIT"
        self.create_buttons()

        
    def create_buttons(self):
        '''Creates the control buttons displayed in the GUI'''

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(fill="x")
        
        # Open Arm button
        self.open_arm_btn = ttk.Button(self.top_frame,
            text="Open Arm", command=self.open_arm)
        self.open_arm_btn.pack(side="left")

        # Close Arm button
        self.close_arm_btn = ttk.Button(self.top_frame,
            text="Close Arm", command=self.close_arm)
        self.close_arm_btn.pack(side="left")
        
        # Portrait button
        self.portrait_btn = ttk.Button(self.top_frame,
            text="Portrait", command=self.portrait)
        self.portrait_btn.pack(side="left")
        
        self.landscape_btn= ttk.Button(self.top_frame,
            text="Landscape", command=self.landscape)
        self.landscape_btn.pack(side="left")
        
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(fill="x")
        
        # Head Tilt button
        self.head_tilt_btn = ttk.Button(self.bottom_frame,
            text="Tilt Head", command=self.tilt)
        self.head_tilt_btn.pack(side="left")
        
        # Nod Head button
        self.nod_head_btn = ttk.Button(self.bottom_frame,
            text="Nod Head", command=self.nod)
        self.nod_head_btn.pack(side="left")
        
        # Shake Head button
        self.shake_head_btn = ttk.Button(self.bottom_frame,
            text="Shake Head", command=self.shake)
        self.shake_head_btn.pack(side="left")

        # Shutdown button
        self.shutdown_btn = ttk.Button(self.bottom_frame,
            text="Shutdown", command=self.shutdown)
        self.shutdown_btn.pack(side="left")
        
                
    def open_arm(self):
        '''Opens the arm using SerialArmController'''

        if self.serial_arm_controller.is_connected:
            self.notifications_frame.append_line("Opening arm...")
            self.serial_arm_controller.open_arm()
        else:
            self.notifications_frame.append_line("[DISCONNECTED] Opening arm...") #For offline testing


    def close_arm(self):
        '''Closes the arm using SerialArmController'''

        if self.serial_arm_controller.is_connected:
            self.notifications_frame.append_line("Closing arm...")
            self.serial_arm_controller.close_arm()
        else:
            self.notifications_frame.append_line("[DISCONNECTED] Closing arm...") #For offline testing

                
    def portrait(self):
        '''Changes the arm to portrait mode using SerialArmController'''

        if self.serial_arm_controller.is_connected:
            self.notifications_frame.append_line("Changing to portrait...")
            self.serial_arm_controller.portrait()
            self.orientation = "PORTRAIT"
        else:
            self.notifications_frame.append_line("[DISCONNECTED] Changing to portrait...") #For offline testing
                

    def landscape(self):
        '''Changes the arm to landscape mode using SerialArmController'''

        if self.serial_arm_controller.is_connected:
            self.notifications_frame.append_line("Changing to landscape...")
            self.serial_arm_controller.landscape()
            self.orientation = "LANDSCAPE"
        else:
            self.notifications_frame.append_line("[DISCONNECTED] Changing to landscape...") #For offline testing
                

    def tilt(self):
        '''Tilts the arm using SerialArmController'''

        if self.serial_arm_controller.is_connected:
            self.notifications_frame.append_line("Tilting head...")
            self.serial_arm_controller.tilt()
        else:
            self.notifications_frame.append_line("[DISCONNECTED] Tilting head...") #For offline testing

            
    def nod(self):
        '''Nods the arm using SerialArmController'''

        if self.serial_arm_controller.is_connected:
            self.notifications_frame.append_line("Nodding head...")
            self.serial_arm_controller.nod()
        else:
            self.notifications_frame.append_line("[DISCONNECTED] Nodding head...") #For offline testing

            
    def shake(self):
        '''Shakes the arm using SerialArmController'''

        if self.serial_arm_controller.is_connected:
            self.notifications_frame.append_line("Shaking head...")
            self.serial_arm_controller.shake()
        else:
            self.notifications_frame.append_line("[DISCONNECTED] Shaking head...") #For offline testing


    def shutdown(self):
        '''Shuts down the arm using SerialArmController'''

        if self.serial_arm_controller.is_connected:
            self.notifications_frame.append_line("Shutting down...")
            self.serial_arm_controller._shutdown()
        else:
            self.notifications_frame.append_line("[DISCONNECTED] Shutting down...") #For offline testing
        