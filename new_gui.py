import tkinter as tk
import matplotlib 
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from PIL import ImageTk, Image
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


##Global Vars
LARGE_FONT= ("Verdana", 12)

data_choices = "EMG", "EOG", "ECG", "EEG", "Pulse-Ox", "Breath-Vel","Chest Motion","Body Motion"


data_dict = {
        "EMG": [1,2,3,4,5,6], 
        "EOG": [2,4,5,6,7], 
        "ECG": [22,8,7,8], 
        "EEG": [4,8,15,16,23,42],
        "Pulse-Ox":[12,20,2,4,66,17], 
        "Breath-Vel":[77,8,13,20,15,1],
        "Chest Motion":[0,3,0,3,0,3],
        "Body Motion": [0,4,1,5,6,1,0]
}
##Misc Functions
def make_graph(x):
    fig = Figure(figsize=(6,6))
    a = fig.add_subplot(111)
    a.set_title ="test"
    a.plot(x, range(len(x)))
    return fig

def save_graph(data, filename):
    plt.figure()
    plt.plot(data_dict[data], range(len(data_dict[data])))
    plt.savefig(filename)

##GUI stuff
class Gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        login_ref = []
        for F in (LoginPage,PageOne,DataPage):
            if (F == PageOne):
                frame = F(container,self,login_ref.name)
            else:
                frame = F(container, self)
            if (F == LoginPage):
                login_ref = frame

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        self.name = tk.StringVar()
        self.name.set("default")
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Login Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.button = tk.Button(self, text="Login",command=lambda:self.login(controller))
        self.button.pack()
        self.quit = tk.Button(self, text="QUIT", fg="red",
                command=lambda: controller.quit())
        self.quit.pack(side="bottom")

        self.e = tk.Entry(self,text='Name')
        self.e.pack(side='bottom')
        self.e.focus_set()
    def login(self,controller):
        self.string = "Welcome "+self.e.get()
        self.name.set(self.string)
        #TODO where security logic would be if neeeded
        controller.show_frame(PageOne)
        print(self.string + " logged in!")

class PageOne(tk.Frame):

    def __init__(self, parent, controller,name):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, textvar=name, font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.button = tk.Button(self, text = "Show data", command=lambda:self.showdata(controller))
        self.button.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                command=lambda: controller.quit())
        self.quit.pack(side="bottom")
    def showdata(self, controller):
        print("will show data")
        controller.show_frame(DataPage)

class DataPage(tk.Frame):
    def __init__(self,parent, controller):
        self.canvas = None
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Datas",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.var = tk.StringVar()
        self.var.set(data_choices[0])
        self.menu = tk.OptionMenu(self, self.var,"EMG", "EOG", "ECG", "EEG", "Pulse-Ox", "Breath-Vel","Chest Motion","Body Motion")
        self.menu.pack()
        self.show_graph = tk.Button(self, text="Show Graph",command=lambda:self.showgraph())
        self.show_graph.pack()
        self.save_as = tk.Button(self, text = "Save as", command=lambda:self.saveas()) 
        self.save_as.pack()
        self.e = tk.Entry(self,text='figure.png')
        self.e.pack()
        self.e.focus_set()
        
        self.quit = tk.Button(self, text="QUIT", fg="red",
                command=lambda: controller.quit())
        self.quit.pack()
    def showgraph(self):
        print(self.var.get())
        fig1 = make_graph(data_dict[self.var.get()])
        #TODO benefits of self.figure?
        if(self.canvas is not None):
            self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(fig1,master=self)
        self.canvas.get_tk_widget().pack()
    def saveas(self):
        save_graph(self.var.get(), self.e.get()+".png")
        print("Saved")
        self.e.delete(0,'end')




app = Gui()
app.mainloop()
