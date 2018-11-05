import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np


class MainWindow(tk.Tk):
    def put_entry(self, row, name, label):
        self.widgets[name+"_label"] = tk.Label(self.params_frame, text=label, font=(None, 20))
        self.widgets[name+"_label"].grid(row=row, column=0, sticky="W")
        self.widgets[name+"_entry"] = tk.Entry(self.params_frame)
        self.widgets[name+"_entry"].grid(row=row, column=1)

    def get_entry(self, name):
        return self.widgets[name+"_entry"]

    def apply_button_callback(self):
        x = np.linspace(-10, 10)
        y = 1/x
        self.draw_plot("euler", x, y, "r")
        self.draw_plot("imp_euler", x, x*2, "b")
        self.canvas.draw()

    def remove_plot(self, name):
        line = self.plots[name].pop(0)
        line.remove()

    def draw_plot(self, name, x_data, y_data, format):
        if name in self.plots.keys():
            self.remove_plot(name)
        self.plots[name] = self.axes.plot(x_data, y_data, format)

    def __init__(self):
        super().__init__()

        self.widgets = {}
        self.plots = {}

        self.left_pane = tk.Frame(self)
        self.params_frame = tk.Frame(self.left_pane)
        self.put_entry(0, "x0", u"x\N{SUBSCRIPT ZERO}:")
        self.put_entry(1, "y0", u"y\N{SUBSCRIPT ZERO}:")
        self.put_entry(2, "x", "X:")
        self.put_entry(3, "step", "Step:")
        self.apply_bt = tk.Button(self.left_pane, text="Apply", command=self.apply_button_callback)
        self.apply_bt.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.params_frame.pack(side=tk.LEFT)
        self.left_pane.pack(side=tk.LEFT, fill=tk.Y)

        self.right_pane = tk.Frame(self)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_pane)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.right_pane)
        self.toolbar.pack()
        self.toolbar.update()

        self.right_pane.pack(fill=tk.BOTH, expand=1)
        self.right_pane.configure(background="red")

        # self.configure(background='red')


root = MainWindow()
root.mainloop()

