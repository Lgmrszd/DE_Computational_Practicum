import tkinter as tk


class MainWindow(tk.Tk):
    def put_entry(self, row, name, label):
        self.widgets[name+"_label"] = tk.Label(self.params_frame, text=label, font=(None, 20))
        self.widgets[name+"_label"].grid(row=row, column=0, sticky="W")
        self.widgets[name+"_entry"] = tk.Entry(self.params_frame)
        self.widgets[name+"_entry"].grid(row=row, column=1)

    def get_entry(self, name):
        return self.widgets[name+"_entry"]

    def apply_button_callback(self):
        print("Test")

    def __init__(self):
        super().__init__()

        self.widgets = {}

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
        # self.configure(background='red')


root = MainWindow()
root.mainloop()

