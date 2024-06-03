import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import PchipInterpolator

# Function to plot the particle size distribution curve
def plot_curve(sieve_sizes, cum_percent_passing, student_info):
    plt.figure(figsize=(10, 6))

    # Perform monotonic cubic interpolation
    interp_func = PchipInterpolator(sieve_sizes, cum_percent_passing)
    x_interp = np.linspace(min(sieve_sizes), max(sieve_sizes), 1000)
    y_interp = interp_func(x_interp)

    # Plot the interpolated curve
    plt.plot(x_interp, y_interp, color='b', label='Interpolated Curve')

    # Plot data points
    plt.scatter(sieve_sizes, cum_percent_passing, color='r', label='Data Points')

    # Plot horizontal lines at 10%, 30%, and 60%
    plt.axhline(y=10, color='g', linestyle='--')
    plt.axhline(y=30, color='m', linestyle='--')
    plt.axhline(y=60, color='y', linestyle='--')

    # Find intersection points with interpolated curve
    d10_index = np.argmin(np.abs(y_interp - 10))
    d30_index = np.argmin(np.abs(y_interp - 30))
    d60_index = np.argmin(np.abs(y_interp - 60))

    # Plot intersection points and add to legend
    plt.scatter(x_interp[d10_index], 10, color='g', marker='x', label=f'D10: {x_interp[d10_index]:.2f}')
    plt.scatter(x_interp[d30_index], 30, color='m', marker='x', label=f'D30: {x_interp[d30_index]:.2f}')
    plt.scatter(x_interp[d60_index], 60, color='y', marker='x', label=f'D60: {x_interp[d60_index]:.2f}')

    # Draw vertical lines from intersection points
    plt.axvline(x=x_interp[d10_index], ymin=0, ymax=(10/100), color='g', linestyle='--')
    plt.axvline(x=x_interp[d30_index], ymin=0, ymax=(30/100), color='m', linestyle='--')
    plt.axvline(x=x_interp[d60_index], ymin=0, ymax=(60/100), color='y', linestyle='--')

    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlabel("Particle Size (mm)")
    plt.ylabel("Cumulative Percentage Passing (%)")
    plt.title(f"Lab 2: Grain Size Analysis of Soil\nStudent: {student_info['name']}, Roll No: {student_info['roll']}, Exam Symbol: {student_info['exam_symbol']}")
    plt.xscale('log')  # Set x-axis to logarithmic scale
    plt.xticks([0.1, 1, 10, 100, 1000])  # Set x-axis ticks at intervals of multiples of 10
    plt.legend()
    plt.show()

# Function to get data points from the user
def get_data_points(num_points, student_info):
    data_window = tk.Tk()
    data_window.title("Enter Data Points")
    data_window.geometry("800x600")

    font_large = ("Times New Roman", 30, "bold")
    font_medium = ("Times New Roman", 20, "bold")
    font_small = ("Times New Roman", 14, "bold")

    title_label = tk.Label(data_window, text="Lab 2: Grain Size Analysis of Soil", font=font_large, bg="lightblue", pady=10)
    title_label.pack(pady=10)

    form_frame = tk.Frame(data_window)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Sieve Size (mm)", font=font_medium).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(form_frame, text="Cumulative Percentage Passing (%)", font=font_medium).grid(row=0, column=1, padx=5, pady=5)

    sieve_sizes = []
    cum_percent_passing = []

    entries = []
    for i in range(num_points):
        entry_row = []
        for j in range(2):
            entry = tk.Entry(form_frame, font=font_medium)
            entry.grid(row=i + 1, column=j, padx=5, pady=5)
            entry_row.append(entry)
        entries.append(entry_row)

    def on_ok():
        try:
            prev_sieve_size = float('inf')
            prev_cum_percent = 101
            for entry_row in entries:
                sieve_size = float(entry_row[0].get())
                cum_percent = float(entry_row[1].get())
                if not (0 <= cum_percent <= 100):
                    raise ValueError("Cumulative percentage passing must be between 0 and 100.")
                if sieve_size >= prev_sieve_size or cum_percent >= prev_cum_percent:
                    raise ValueError("Sieve sizes and cumulative percentage passing values must be in decreasing order.")
                sieve_sizes.append(sieve_size)
                cum_percent_passing.append(cum_percent)
                prev_sieve_size = sieve_size
                prev_cum_percent = cum_percent
            if len(set(sieve_sizes)) != len(sieve_sizes):
                raise ValueError("Sieve sizes must be unique.")
            data_window.destroy()
            plot_curve(sieve_sizes[::-1], cum_percent_passing[::-1], student_info)  # Reverse the order
        except ValueError as ve:
            messagebox.showerror("Invalid input", f"Please enter valid numerical values.\nError: {ve}")

    ok_button = tk.Button(data_window, text="OK", command=on_ok, font=font_medium)
    ok_button.pack(pady=10)

    credit_frame = tk.Frame(data_window, bd=2, relief="groove", padx=10, pady=10)
    credit_frame.pack(side="bottom", pady=10)
    credit_label = tk.Label(credit_frame, text="Developed by: Er. Dipesh Jaisi Poudel\nMSc. in Structural Engineering\nLecturer, School of Engineering, Pokhara University", font=font_small, fg="darkblue")
    credit_label.pack()

    data_window.mainloop()

# Custom dialog to get initial student info and number of data points
def get_initial_info():
    initial_info_window = tk.Tk()
    initial_info_window.title("Student Information")
    initial_info_window.geometry("800x600")

    font_large = ("Times New Roman", 30, "bold")
    font_medium = ("Times New Roman", 20, "bold")
    font_small = ("Times New Roman", 14, "bold")

    title_label = tk.Label(initial_info_window, text="Lab 2: Grain Size Analysis of Soil", font=font_large, bg="lightblue", pady=10)
    title_label.pack(pady=10)

    form_frame = tk.Frame(initial_info_window)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Student Name:", font=font_medium).grid(row=0, column=0, padx=5, pady=5, sticky='e')
    tk.Label(form_frame, text="Roll Number:", font=font_medium).grid(row=1, column=0, padx=5, pady=5, sticky='e')
    tk.Label(form_frame, text="Exam Symbol Number:", font=font_medium).grid(row=2, column=0, padx=5, pady=5, sticky='e')
    tk.Label(form_frame, text="Number of Data Points:", font=font_medium).grid(row=3, column=0, padx=5, pady=5, sticky='e')

    name_entry = tk.Entry(form_frame, font=font_medium)
    roll_entry = tk.Entry(form_frame, font=font_medium)
    exam_symbol_entry = tk.Entry(form_frame, font=font_medium)
    num_points_entry = tk.Entry(form_frame, font=font_medium)

    name_entry.grid(row=0, column=1, padx=5, pady=5)
    roll_entry.grid(row=1, column=1, padx=5, pady=5)
    exam_symbol_entry.grid(row=2, column=1, padx=5, pady=5)
    num_points_entry.grid(row=3, column=1, padx=5, pady=5)

    def on_ok():
        try:
            student_info = {
                'name': name_entry.get(),
                'roll': roll_entry.get(),
                'exam_symbol': exam_symbol_entry.get()
            }
            num_points = int(num_points_entry.get())
            if not student_info['name'] or not student_info['roll'] or not student_info['exam_symbol']:
                raise ValueError("All fields are required.")
            initial_info_window.destroy()
            get_data_points(num_points, student_info)
        except ValueError as ve:
            messagebox.showerror("Invalid input", f"Please fill in all the fields with valid information.\nError: {ve}")

    ok_button = tk.Button(initial_info_window, text="OK", command=on_ok, font=font_medium)
    ok_button.pack(pady=10)

    credit_frame = tk.Frame(initial_info_window, bd=2, relief="groove", padx=10, pady=10)
    credit_frame.pack(side="bottom", pady=10)
    credit_label = tk.Label(credit_frame, text="Developed by: Er. Dipesh Jaisi Poudel\nMSc. in Structural Engineering\nLecturer, School of Engineering, Pokhara University", font=font_small, fg="darkblue")
    credit_label.pack()

    initial_info_window.mainloop()


# Start the program
get_initial_info()

