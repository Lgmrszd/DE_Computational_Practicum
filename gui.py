import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

import task_methods


class MainWindow(tk.Tk):
    def put_entry(self, row, name, label):
        self.widgets[name+"_label"] = tk.Label(self.params_frame, text=label, font=(None, 17))
        self.widgets[name+"_label"].grid(row=row, column=0, sticky="W")
        self.widgets[name+"_entry"] = tk.Entry(self.params_frame)
        self.widgets[name+"_entry"].grid(row=row, column=1)

    def put_check(self, row, name, label):
        self.widgets[name+"_var"] = tk.IntVar()
        self.widgets[name+"_cb"] = tk.Checkbutton(self.params_frame, text=label,
                                                  font=(None, 17), variable=self.widgets[name+"_var"])
        self.widgets[name+"_cb"].grid(row=row, column=0, columnspan=2, sticky="W")

    def get_values(self):
        values = {}
        for i in ["x0", "y0", "x"]:
            values[i] = float(self.widgets[i+"_entry"].get())
        for i in ["grid", "grid_from", "grid_to"]:
            values[i] = int(self.widgets[i+"_entry"].get())
        for i in["exact", "euler", "imp_euler", "r_k"]:
            values[i] = bool(self.widgets[i+"_var"].get())
        return values

    def validate_values(self):
        errors = []
        values_float = {}
        for i in ["x0", "y0", "x"]:
            values_float[i] = self.widgets[i + "_entry"].get()
        for key in values_float.keys():
            try:
                float(values_float[key])
            except ValueError:
                errors.append(str(key)+" is not float")

        values_int = {}
        for i in ["grid", "grid_from", "grid_to"]:
            values_int[i] = self.widgets[i + "_entry"].get()
        for key in values_int.keys():
            try:
                int(values_int[key])
            except ValueError:
                errors.append(str(key)+" is not int")

        return len(errors) == 0, errors

    def calculate_errors(self):
        correct, errors = self.validate_values()
        if not correct:
            self.status_bar.configure(text="; ".join(errors), bg="red")
            return
        values = self.get_values()
        x0 = values["x0"]
        y0 = values["y0"]
        x = values["x"]
        grid_from = values["grid_from"]
        grid_to = values["grid_to"]
        grid_range = [i for i in range(grid_from, grid_to+1)]
        euler_range = []
        imp_euler_range = []
        r_k_range = []
        for grid in grid_range:
            exact_x, exact_y, exact_is_overflow \
                = task_methods.exact(x0, y0, x, grid)
            euler_x, euler_y, euler_is_overflow \
                = task_methods.euler(x0, y0, x, grid)
            imp_euler_x, imp_euler_y, imp_euler_is_overflow \
                = task_methods.imp_euler(x0, y0, x, grid)
            r_k_x, r_k_y, r_k_is_overflow \
                = task_methods.r_k(x0, y0, x, grid)
            least = min(len(exact_y), len(euler_y), len(imp_euler_y), len(r_k_y))
            exact_y = exact_y[:least]
            euler_y = euler_y[:least]
            imp_euler_y = imp_euler_y[:least]
            r_k_y = r_k_y[:least]

            euler_y_error = np.abs(euler_y-exact_y)
            euler_error = euler_y_error.sum()/least
            euler_range.append(euler_error)

            imp_euler_y_error = np.abs(imp_euler_y-exact_y)
            imp_euler_error = imp_euler_y_error.sum()/least
            imp_euler_range.append(imp_euler_error)

            r_k_y_error = np.abs(r_k_y - exact_y)
            r_k_error = r_k_y_error.sum()/least
            r_k_range.append(r_k_error)

        # print(grid_range, euler_range)
        self.draw_error_plot("euler", grid_range, euler_range, "mo-")
        self.draw_error_plot("imp_euler", grid_range, imp_euler_range, "gs-")
        self.draw_error_plot("r_k", grid_range, r_k_range, "b^-")
        self.error_axes.legend([self.plots["euler_er"][0], self.plots["imp_euler_er"][0], self.plots["r_k_er"][0]],
                               ["Euler", "Improved Euler", "Runge-Kutta"], loc='upper right')
        self.error_canvas.draw()

        # euler_y_error = np.abs(exact_y - euler_y)
        # imp_euler_y_error = np.abs(exact_y - imp_euler_y)
        # r_k_y_error = np.abs(exact_y - r_k_y)
        # legend_lines = []
        # legend_labels = []
        # self.draw_error_plot("euler", total_x, euler_y_error, "m-")

    def apply_button_callback(self):
        correct, errors = self.validate_values()
        if not correct:
            self.status_bar.configure(text="; ".join(errors), bg="red")
            return

        values = self.get_values()
        x0 = values["x0"]
        y0 = values["y0"]
        x = values["x"]
        grid = values["grid"]
        is_exact = values["exact"]
        is_euler = values["euler"]
        is_imp_euler = values["imp_euler"]
        is_r_k = values["r_k"]
        self.status_bar.configure(text="OK", bg="green")

        # exact_x, exact_y, exact_is_overflow \
        #     = task_methods.exact(x0, y0, x, grid)
        # euler_x, euler_y, euler_is_overflow \
        #     = task_methods.euler(x0, y0, x, grid)
        # imp_euler_x, imp_euler_y, imp_euler_is_overflow \
        #     = task_methods.imp_euler(x0, y0, x, grid)
        # r_k_x, r_k_y, r_k_is_overflow \
        #     = task_methods.r_k(x0, y0, x, grid)
        # if exact_is_overflow:
        #     exact_y = exact_y[:len(exact_x)]
        # if euler_is_overflow:
        #     euler_y = euler_y[:len(euler_x)]
        # if imp_euler_is_overflow:
        #     imp_euler_y = imp_euler_y[:len(imp_euler_x)]
        # if r_k_is_overflow:
        #     r_k_y = r_k_y[:len(r_k_x)]

        legend_lines = []
        legend_labels = []
        for i in ["exact", "euler", "imp_euler", "r_k"]:
            self.remove_plot(i)
        if is_exact:
            exact_x, exact_y, exact_is_overflow \
                = task_methods.exact(x0, y0, x, grid)
            if exact_is_overflow:
                self.status_bar.configure(text="Warning: data overflow", bg="yellow")
            self.draw_plot("exact", exact_x, exact_y, "r-", label="Exact")
            legend_lines.append(self.plots["exact"][0])
            legend_labels.append("Exact")
        if is_euler:
            euler_x, euler_y, euler_is_overflow \
                = task_methods.euler(x0, y0, x, grid)
            if euler_is_overflow:
                self.status_bar.configure(text="Warning: data overflow", bg="yellow")
            self.draw_plot("euler", euler_x, euler_y, "m-", label="Euler")
            legend_lines.append(self.plots["euler"][0])
            legend_labels.append("Euler")
        if is_imp_euler:
            imp_euler_x, imp_euler_y, imp_euler_is_overflow \
                = task_methods.imp_euler(x0, y0, x, grid)
            if imp_euler_is_overflow:
                self.status_bar.configure(text="Warning: data overflow", bg="yellow")
            self.draw_plot("imp_euler", imp_euler_x, imp_euler_y, "g-", label="Improved Euler")
            legend_lines.append(self.plots["imp_euler"][0])
            legend_labels.append("Improved Euler")
        if is_r_k:
            r_k_x, r_k_y, r_k_is_overflow \
                = task_methods.r_k(x0, y0, x, grid)
            if r_k_is_overflow:
                self.status_bar.configure(text="Warning: data overflow", bg="yellow")
            self.draw_plot("r_k", r_k_x, r_k_y, "b-", label="Runge-Kutta")
            legend_lines.append(self.plots["r_k"][0])
            legend_labels.append("Runge-Kutta")

        self.axes.legend(legend_lines, legend_labels, loc='upper left')
        self.main_canvas.draw()
        self.error_canvas.draw()

    def draw_plot(self, name, x_data, y_data, *args, **kwargs):
        if name in self.plots.keys():
            self.remove_plot(name)
        self.plots[name] = self.axes.plot(x_data, y_data, *args, **kwargs)
        self.axes.relim()
        self.axes.autoscale()

    def remove_plot(self, name):
        if name in self.plots:
            line = self.plots[name].pop(0)
            line.remove()
            del self.plots[name]

    def draw_error_plot(self, name, x_data, y_data, *args, **kwargs):
        name = name + "_er"
        if name in self.plots.keys():
            self.remove_plot(name)
        self.plots[name] = self.error_axes.plot(x_data, y_data, *args, **kwargs)
        self.error_axes.relim()
        self.error_axes.autoscale()

    def remove_error_plot(self, name):
        name = name + "_er"
        if name in self.plots:
            line = self.plots[name].pop(0)
            line.remove()
            del self.plots[name]

    def __init__(self):
        super().__init__()

        self.widgets = {}
        self.plots = {}

        self.main_frame = tk.Frame(self)
        self.left_pane = tk.Frame(self.main_frame)
        self.params_frame = tk.Frame(self.left_pane)
        self.put_entry(0, "x0", u"x\N{SUBSCRIPT ZERO}:")
        self.put_entry(1, "y0", u"y\N{SUBSCRIPT ZERO}:")
        self.put_entry(2, "x", "X:")
        self.put_entry(3, "grid", "Grid:")
        self.put_check(4, "exact", "Draw Exact")
        self.put_check(5, "euler", "Draw Euler")
        self.put_check(6, "imp_euler", "Draw improved Euler")
        self.put_check(7, "r_k", "Draw Runge-Kutta")
        self.params_frame.pack(side=tk.TOP)

        self.apply_bt = tk.Button(self.left_pane, text="Apply", command=self.apply_button_callback)
        self.apply_bt.pack(side=tk.TOP, fill=tk.X, expand=0)

        self.error_opts = tk.Frame(self.left_pane)
        grid_from = tk.Label(self.error_opts, text="Grid from", font=(None, 14))
        grid_from.grid(row=0, column=0)
        self.widgets["grid_from_entry"] = tk.Entry(self.error_opts)
        self.widgets["grid_from_entry"].grid(row=0, column=1)
        grid_to = tk.Label(self.error_opts, text="Grid to", font=(None, 14))
        grid_to.grid(row=1, column=0)
        self.widgets["grid_to_entry"] = tk.Entry(self.error_opts)
        self.widgets["grid_to_entry"].grid(row=1, column=1)
        self.error_bt = tk.Button(self.error_opts, text="Calculate\nError", command=self.calculate_errors)
        self.error_bt.grid(row=0, column=2, rowspan=2)
        self.error_opts.pack(side=tk.TOP)

        self.error_fig = Figure(figsize=(5, 4), dpi=100)
        self.error_axes = self.error_fig.add_subplot(111)
        self.error_canvas = FigureCanvasTkAgg(self.error_fig, master=self.left_pane)
        self.error_canvas.draw()
        self.error_canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        self.left_pane.pack(side=tk.LEFT, fill=tk.Y)

        self.right_pane = tk.Frame(self.main_frame)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = self.fig.add_subplot(111)
        self.main_canvas = FigureCanvasTkAgg(self.fig, master=self.right_pane)
        self.main_canvas.draw()
        self.main_canvas.get_tk_widget().pack(side=tk.BOTTOM, expand=1, fill=tk.BOTH)

        self.toolbar = NavigationToolbar2Tk(self.main_canvas, self.right_pane)
        self.toolbar.pack()
        self.toolbar.update()

        self.right_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.status_bar = tk.Label(self, bg="green", text="OK")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, expand=0)
        default = task_methods.get_default()
        for k, v in default.items():
            self.widgets[k+"_entry"].insert(0, v)


root = MainWindow()
root.mainloop()
