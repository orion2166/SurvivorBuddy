# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime

class NotificationFrame(tk.Frame):
    '''Box to display notification in the GUI'''

    def __init__(self, master, _logFile, **kwargs):
        '''
        The constructor for NotificationsFrame

        :param master: The Tk parent widget
        :param _logFile: The file handle for the output log file
        '''

        super().__init__(master, **kwargs)
        
        self.logFile = _logFile
        self.label = ttk.Label(self, text="Notifications")
        self.label.pack()
        
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.pack(fill="x", expand=1)
        
        self.text = tk.Text(self.scrollbar, height=4)
        self.text.config(state=tk.DISABLED)
        self.text.pack(fill="x", expand=1)
    

    def append_line(self, line):
        '''
        Prints a line to the notification box and 
        a timestamped line to the log file
        '''

        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, line + "\n")
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        self.logFile.write(timestamp + " - " + line + "\n") #Print notification to external log file
        self.text.see(tk.END)   #Scrolls down to show latest notification automatically
        self.text.config(state=tk.DISABLED)
        
        
        