# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:17:02 2020

@author: shill
"""

import tkinter as tk
import tkinter.ttk as ttk

class StatusBar(tk.Frame):
    '''Displays the connection status of the GUI to the arm'''

    def __init__(self, master, **kwargs):
        '''
        Constructor for StatusBar

        :param master: The Tk parent widget
        '''

        super().__init__(master, **kwargs)
        
        # STATUS #
        self.status_frame = tk.Frame(self)
        self.status_frame.pack(side="left")
        
        self.status_label = ttk.Label(self.status_frame, text="Status:")
        self.status_label.pack(side="left")
        
        self.status_text = tk.StringVar()
        self.status_text.set("DISCONNECTED")
        self.status_text_label = ttk.Label(
            self.status_frame, textvariable=self.status_text)
        self.status_text_label.pack(side="left")


    def set_status(self, status):
        '''
        Sets the status of the GUI to the arm

        :param status: The status to set to
        '''

        self.status_text.set(status)
        