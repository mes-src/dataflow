import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import *
from tkinter import simpledialog
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,  NavigationToolbar2Tk
import matplotlib.pyplot as plt

import numpy as np 

class Workflow(tk.Frame):

    def __init__(self, master=None, param_dict = None):
        super().__init__(master)

        self.param_dict = param_dict
 
        self.openwindow()
        self.create_widgets()

    def openwindow(self): 
        self.window = Toplevel(self.master) 
        self.window.title("New Window") 
        self.window.geometry("1000x350") 
    
    def time_series_workflow(self):
        c1_var= IntVar(value=1) 
        c1 = tk.Checkbutton(self.window, text='Yahoo',variable=c1_var,
            onvalue=1,offvalue=0,)
        c1.grid(row=4,column=0) 

        c2_var= IntVar()
        c2 = tk.Checkbutton(self.window, text='Quandl',variable=c2_var,
            onvalue=1,offvalue=0,)
        c2.grid(row=4,column=1) 


        l1 = Label(self.window, text = 'Returns')
        option_list = [
            "Universe C-bind",
            "Individual Historical Prices - Solo",
            "Individual Historical Prices & Desc",
        ]
        strat = tk.StringVar(self.window, option_list)
        strat.set(option_list[0])
        def init_flow(selected_value):
            if selected_value == "Universe C-bind":
                print('cbind')

        opt = tk.OptionMenu(self.window, strat ,*option_list, command=init_flow)
        opt.grid(row=8,column=1)





    def plot(self):
        x = ['Col A', 'Col B', 'Col C']
        y = [50, 20, 80]

        fig = plt.figure(figsize=(4, 5))
        plt.bar(x=x, height=y)
        plt.xticks(x, rotation=90)

        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, ipadx=40, ipady=20)

        # navigation toolbar
        toolbarFrame = tk.Frame(master=self.window)
        toolbarFrame.grid(row=2,column=0)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

        
    def create_widgets(self):
        exit_button = Button(self.window, text="Exit", command=self.window.destroy) 
        # self.window.wait_window(self.window)
        exit_button.grid(row=8,column=1)
