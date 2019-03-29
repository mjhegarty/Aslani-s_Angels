import tkinter as tk
import matplotlib 
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from PIL import ImageTk, Image
from subprocess import call
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def make_graph(x):
   fig = Figure(figsize=(6,6))
   a = fig.add_subplot(111)
   a.set_title ="test"
   a.plot(x, range(len(x)))
   return fig

def show_graph(self, canvas):
    if (self.graph["text"] == "show graph"):
        print("got to show")
        canvas.get_tk_widget().pack(side = "bottom")
        self.graph["text"] = "hide graph"
    else:
        canvas.get_tk_widget().pack_forget()
        print("got to forget")
        self.graph["text"] = "show graph"

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()




    def create_widgets(self):
        both = "both"
        self.start = tk.Button(self)
        self.start["text"] = "start"
        self.start["fg"] = "green"
        self.start["command"] = self.say_hi
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
        canvas = FigureCanvasTkAgg(fig1, master=self)


        self.graph = tk.Button(self)
        self.graph["text"] = "show graph"
        self.graph["fg"] = "blue"
        self.graph["command"] = lambda: show_graph(self, canvas)
        self.graph.pack(side="right", fill=both, expand=1)
        #path = "testimage.png"
        
        

        #self.img = ImageTk.PhotoImage(Image.open(path))

        #self.panel = tk.Label(self, image=self.img)
     #  # self.panel.image = self.img
        #self.panel.pack(side = "bottom")


        #fig1 = make_graph([1,2,3,4,5])
        #fig2 = make_graph([1,2,3,4,5])
        #canvas = FigureCanvasTkAgg(fig1, master=self)
        #canvas.get_tk_widget().pack(side = "bottom")

        #canvas2 = FigureCanvasTkAgg(fig2, master=self)
        #canvas2.get_tk_widget().pack(side = "bottom")

    def pairing(self):
        call("./python_test.sh")
    def say_hi(self):
        if (self.start["text"]=="start"):  
            self.start["text"] = "stop"
            self.start["fg"] = "red"
            call("./python_test.sh")
        else:
            self.start["text"]="start"
            self.start["fg"]= "green"
root = tk.Tk()
app = Application(master=root)
app.mainloop()
