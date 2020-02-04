#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-

import tkinter as Tk
from retroarchgui import RetroarchGUI

class GUI():    

    def __init__(self,scriptDir,logger) :        
        self.scriptDir = scriptDir
        self.window = Tk.Tk()
        self.window.resizable(False,False)
        self.window.title('BestArcade')        
        self.logger = logger         

    def draw(self) :
        self.root = Tk.Frame(self.window,padx=10,pady=5)
        self.root.grid(column=0,row=0)
        self.drawMainframe()
        self.window.mainloop()

# MAINFRAME, NOTEBOOK & TABS
    
    def drawMainframe(self) :
        self.mainFrame = Tk.Frame(self.root,padx=10,pady=5)
        self.mainFrame.grid(column=0,row=0,sticky="EW",pady=5)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.notebook = Tk.ttk.Notebook(self.mainFrame)
        self.notebook.grid(column=0,row=0,sticky="EW",pady=5)
        self.notebook.grid_columnconfigure(0, weight=1)
        
        # RETROARCH TAB        
        
        self.tabFrame = Tk.Frame(self.notebook,padx=10,pady=5)
        self.tabFrame.grid(column=0,row=0,sticky="EW",pady=5)
        self.tabFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.tabFrame, text='Retroarch',sticky="EW")
        self.notebook.select(self.tabFrame)
        retroarchGUI = RetroarchGUI(self.tabFrame,self.scriptDir,self.logger)
        retroarchGUI.draw()
        
        # SECOND TAB
#        self.tabFrame2 = Tk.Frame(self.notebook,padx=10,pady=5)
#        self.tabFrame2.grid(column=0,row=0,sticky="EW",pady=5)
#        self.tabFrame2.grid_columnconfigure(0, weight=1)
#        self.notebook.add(self.tabFrame2, text='Retroarch2',sticky="EW")
#        self.notebook.select(self.tabFrame2)
#        retroarchGUI2 = RetroarchGUI(self.tabFrame2,self.scriptDir,self.logger)
#        retroarchGUI2.draw()  

        # FUTURE TABS : CUSTOM MAME, ATOMISWAVE, NAOMI, MAME HANDHELDS        
        self.notebook.select(self.tabFrame)
        self.drawConsole()   


# CONSOLE STUFF

    def drawConsole(self) :
        self.consoleFrame = Tk.Frame(self.root, padx=10)
        self.consoleFrame.grid(column=0,row=4,sticky="EW",pady=5)
        self.consoleFrame.grid_columnconfigure(0, weight=1)
        self.logTest = Tk.Text(self.consoleFrame, height=15, state='disabled', wrap='word',background='black',foreground='yellow')
        self.logTest.grid(column=0,row=0,sticky="EW")
        self.scrollbar = Tk.Scrollbar(self.consoleFrame, orient=Tk.VERTICAL,command=self.logTest.yview)
        self.scrollbar.grid(column=1,row=0,sticky=(Tk.N,Tk.S))
        self.logTest['yscrollcommand'] = self.scrollbar.set
        self.logTest.after(10,self.updateConsoleFromQueue)
    
    def updateConsoleFromQueue(self):        
        while not self.logger.log_queue.empty():
            line = self.logger.log_queue.get()            
            self.writeToConsole(line)
            #TODO ?
            self.root.update_idletasks()
        self.logTest.after(10,self.updateConsoleFromQueue)
        
    def writeToConsole(self, msg):                
        numlines = self.logTest.index('end - 1 line').split('.')[0]
        self.logTest['state'] = 'normal'
        if numlines==24:
            self.logTest.delete(1.0, 2.0)
        if self.logTest.index('end-1c')!='1.0':
            self.logTest.insert('end', '\n')
        self.logTest.insert('end', msg)
        self.logTest.see(Tk.END)
        self.logTest['state'] = 'disabled'
