# -*- coding: utf-8 -*-

import tkinter as Tk
from retroarchgui import RetroarchGUI
from customgui import CustomGUI

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
        self.retroarchFrame = Tk.Frame(self.notebook,padx=10,pady=5)
        self.retroarchFrame.grid(column=0,row=0,sticky="EW",pady=5)
        self.retroarchFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.retroarchFrame, text='Retroarch',sticky="EW")
        self.notebook.select(self.retroarchFrame)
        retroarchGUI = RetroarchGUI(self.retroarchFrame,self.scriptDir,self.logger, self)
        retroarchGUI.draw()
        
        # CUSTOM TAB
        self.customFrame = Tk.Frame(self.notebook,padx=10,pady=5)
        self.customFrame.grid(column=0,row=0,sticky="EWN",pady=5)
        self.customFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.customFrame, text='Custom',sticky="EWNS")
        self.notebook.select(self.customFrame)
        customGUI = CustomGUI(self.customFrame,'custom',self.scriptDir,self.logger,self)
        customGUI.draw()
        
        # ATOMISWAVE TAB
        self.atomiswaveFrame = Tk.Frame(self.notebook,padx=10,pady=5)
        self.atomiswaveFrame.grid(column=0,row=0,sticky="EWN",pady=5)
        self.atomiswaveFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.atomiswaveFrame, text='Atomiswave',sticky="EWNS")
        self.notebook.select(self.atomiswaveFrame)
        atomiswaveGUI = CustomGUI(self.atomiswaveFrame,'atomiswave',self.scriptDir,self.logger,self)
        atomiswaveGUI.draw()  
        
        # NAOMI TAB
        self.naomiFrame = Tk.Frame(self.notebook,padx=10,pady=5)
        self.naomiFrame.grid(column=0,row=0,sticky="EWN",pady=5)
        self.naomiFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.naomiFrame, text='Naomi',sticky="EWNS")
        self.notebook.select(self.naomiFrame)
        naomiGUI = CustomGUI(self.naomiFrame,'naomi',self.scriptDir,self.logger,self)
        naomiGUI.draw() 
        
        # HANDHELD TAB
        self.handheldFrame = Tk.Frame(self.notebook,padx=10,pady=5)
        self.handheldFrame.grid(column=0,row=0,sticky="EWN",pady=5)
        self.handheldFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.handheldFrame, text='Handhelds',sticky="EWNS")
        self.notebook.select(self.handheldFrame)
        handheldGUI = CustomGUI(self.handheldFrame,'handheld',self.scriptDir,self.logger,self)
        handheldGUI.draw()

        # FUTURE TABS : CUSTOM MAME, ATOMISWAVE, NAOMI, MAME HANDHELDS        
        self.notebook.select(self.retroarchFrame)
        self.drawConsole()
        
    def disableOtherTabs(self, setKey) :
        if setKey == 'retroarch' :            
            self.notebook.tab(self.customFrame, state="disabled")
            self.notebook.tab(self.atomiswaveFrame, state="disabled")
            self.notebook.tab(self.naomiFrame, state="disabled")
        elif setKey == 'custom' :
            self.notebook.tab(self.retroarchFrame, state="disabled")            
            self.notebook.tab(self.atomiswaveFrame, state="disabled")
            self.notebook.tab(self.naomiFrame, state="disabled")
        elif setKey == 'atomiswave' :
            self.notebook.tab(self.retroarchFrame, state="disabled")
            self.notebook.tab(self.customFrame, state="disabled")            
            self.notebook.tab(self.naomiFrame, state="disabled")
        elif setKey == 'naomi' :
            self.notebook.tab(self.retroarchFrame, state="disabled")
            self.notebook.tab(self.customFrame, state="disabled")
            self.notebook.tab(self.atomiswaveFrame, state="disabled")            
            
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
