import tkinter as tk
import matplotlib 
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from PIL import ImageTk, Image
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def make_graph(x):
   fig = Figure(figsize=(6,6))
   a = fig.add_subplot(111)
   a.set_title ="test"
   a.plot(x, range(len(x)))
   return fig


class my_button():
    def __init__(self, frame):
        self.button = tk.Button(frame)
        self.button["text"] = "start"
        self.button["fg"] = "green"
        self.button["command"] = lambda: self.get_data(frame)
        self.p = None
    def get_data(self, frame):
        if self.p == None:
            self.p = frame.get_data()  
            print ('have p')
        else :
            print ('killing p')
            frame.get_data(self.p)
            self.p = None

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()


    def create_widgets(self):
        both = "both"
        but = my_button(self)
        self.start = but.button
        self.start.pack(side="top", fill=both, expand=1)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="left", fill=both, expand=1)

        self.pair = tk.Button(self)
        self.pair["text"] = "pair"
        self.pair["fg"] = "blue"
        self.pair["command"] = self.pairing
        self.pair.pack(side="top", fill=both, expand=1)
        
        
        fig1 = make_graph([1,2,3,4,5])
        


        self.graph = tk.Button(self)
        self.graph["text"] = "show graph"
        self.graph["fg"] = "blue"
        self.graph["command"] = lambda: self.show_graph(fig1)
        self.graph.pack(side="right", fill=both, expand=1)

    def pairing(self):
        subprocess.call("./blue_connect.sh")
    def get_data(self, p=None): 
        if (self.start["text"]=="start"):  
            self.start["text"] = "stop"
            self.start["fg"] = "red"
            p = subprocess.Popen(("./endless_test.sh"))
            return p
        else:
            self.start["text"]="start"
            self.start["fg"]= "green"
            p.kill()
        
    def say_hi(self):
        if (self.start["text"]=="start"):  
            self.start["text"] = "stop"
            self.start["fg"] = "red"
            subprocess.call("./python_test.sh")
        else:
            self.start["text"]="start"
            self.start["fg"]= "green"

    def show_graph(self, fig1):
        print ("pushed button")
        canvas = FigureCanvasTkAgg(fig1, master=self)
        if (self.graph["text"] == "show graph"):
            print("got to show")
            canvas.get_tk_widget().pack(side = "bottom")
            self.graph["text"] = "hide graph"
        else:
            canvas.get_tk_widget().pack_forget()
            print("got to forget")
            self.graph["text"] = "show graph"
root = tk.Tk()
app = Application(master=root)
app.mainloop()
