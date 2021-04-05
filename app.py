# ui
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import *
from tkinter import simpledialog

# plot
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,  NavigationToolbar2Tk


from workflow import Workflow


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.root = master
        self.root.geometry("1500x500") 
        self.create_widgets()
        self.param_dict = dict()

        
        self.root.mainloop() 


    def create_widgets(self):

        ''' entry forms for tickers'''

        tk.Label(self.root, text="Security").grid(row=0)
        tk.Label(self.root, text="Universe").grid(row=1)
        e1 = tk.Entry(self.root)
        e2 = tk.Entry(self.root)
        e1.insert(END, 'MRVL') #default
        e2.insert(END, 'NVDA TSM AVGO')
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)


        ''' checkbox's for workflow assignements '''

        c1_var= IntVar(value=1) # default True
        c1 = tk.Checkbutton(self.root, text='Time Series',variable=c1_var,
            onvalue=1,offvalue=0,)
        c1.grid(row=4,column=0) 

        c2_var= IntVar()
        c2 = tk.Checkbutton(self.root, text='Fundamentals',variable=c2_var,
            onvalue=1,offvalue=0,)
        c2.grid(row=4,column=1) 

        c3_var= IntVar()
        c3 = tk.Checkbutton(self.root, text='Edgar',variable=c3_var,
            onvalue=1,offvalue=0,)
        c3.grid(row=4,column=2) 

        def build_workflow():
            check_values = [False, True]
            self.param_dict['scurity'] = e1.get()
            self.param_dict['universe'] = e2.get()

            self.param_dict['timeseries'] = check_values[c1_var.get()]
            self.param_dict['funamentals'] = check_values[c2_var.get()]
            self.param_dict['edgar'] = check_values[c3_var.get()]
            print(self.param_dict)

            ''' dispatch workflow based upon user selctions '''
            w = Workflow(self.root, self.param_dict) # opens a workflow window as child of this parent frame
            if self.param_dict.get('timeseries') == True:
                w.time_series_workflow()

        b_go = tk.Button(self.root, text = 'Start!', command = build_workflow)
        b_go.grid(row=5,column=1)


        ''' dropdown menu '''

        option_list = [
            "plot",
            "...",
        ]
        strat = tk.StringVar(self.root, option_list)
        strat.set(option_list[0])
        def create_plot_window(selected_value):
            plot_window = Workflow(self.root, self.param_dict)
            plot_window.plot()

        opt = tk.OptionMenu(self.root, strat ,*option_list, command=create_plot_window)
        opt.grid(row=8,column=1)



        ''' exit '''

        exit_button = tk.Button(self.root, text="Exit", command=self.root.quit) 
        exit_button.grid(row=6,column=1)


def init(app):
    #workflow = app.param_dict
    pass



if __name__ == '__main__':
    a = App(tk.Tk())
    init(a)
