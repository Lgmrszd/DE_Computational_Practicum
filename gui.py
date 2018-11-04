import tkinter as tk

root = tk.Tk()

left_pane = tk.Frame(root)
params_frame = tk.Frame(left_pane)
params_labels = tk.Frame(params_frame)
params_entries = tk.Frame(params_frame)

# x0_frame = tk.Frame(params_frame)
x0_lbl = tk.Label(params_labels, text="x\N{SUBSCRIPT ZERO}:")
x0_lbl.pack(side=tk.TOP)
x0_entry = tk.Entry(params_entries)
x0_entry.pack(side=tk.TOP)
# x0_frame.pack(side=tk.TOP)

# y0_frame = tk.Frame(params_frame)
y0_lbl = tk.Label(params_labels, text=u"y\N{SUBSCRIPT ZERO}:")
y0_lbl.pack(side=tk.TOP)
y0_entry = tk.Entry(params_entries)
y0_entry.pack(side=tk.TOP)
# y0_frame.pack(side=tk.TOP)

# x_frame = tk.Frame(params_frame)
x_lbl = tk.Label(params_labels, text="X:")
x_lbl.pack(side=tk.TOP)
x_entry = tk.Entry(params_entries)
x_entry.pack(side=tk.TOP)
# x_frame.pack(side=tk.TOP)

params_labels.pack(side=tk.LEFT)
params_entries.pack(side=tk.LEFT)

apply_bt = tk.Button(left_pane, text="Apply")
apply_bt.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

params_frame.pack(side=tk.LEFT)
left_pane.pack(side=tk.LEFT, fill=tk.Y)
left_pane.configure(background='black')
root.configure(background='red')
root.mainloop()

