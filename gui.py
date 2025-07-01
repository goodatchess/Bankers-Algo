import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def run_banker_engine(input_data):
    try:
        with open("input.txt", "w") as f:
            f.write(input_data)

        # Windows: use 'banker.exe'
        command = "./banker" if os.name != "nt" else "banker.exe"
        result = subprocess.check_output(f"{command} < input.txt", shell=True).decode()
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def submit():
    try:
        n = int(process_entry.get())
        m = int(resource_entry.get())

        alloc = []
        for i in range(n):
            row = alloc_text[i].get("1.0", "end").strip().split()
            if len(row) != m:
                raise ValueError(f"Alloc row {i+1} must have {m} values.")
            alloc.append(row)

        max_req = []
        for i in range(n):
            row = max_text[i].get("1.0", "end").strip().split()
            if len(row) != m:
                raise ValueError(f"Max row {i+1} must have {m} values.")
            max_req.append(row)

        avail = avail_entry.get().strip().split()
        if len(avail) != m:
            raise ValueError(f"Available vector must have {m} values.")

        # Format input data for C++
        input_data = f"{n}\n{m}\n"
        for row in alloc:
            input_data += " ".join(row) + "\n"
        for row in max_req:
            input_data += " ".join(row) + "\n"
        input_data += " ".join(avail) + "\n"

        output = run_banker_engine(input_data)
        output_box.delete("1.0", "end")
        output_box.insert("end", output)

    except Exception as e:
        messagebox.showerror("Input Error", str(e))

def create_matrix_inputs():
    for widget in matrix_frame.winfo_children():
        widget.destroy()

    try:
        n = int(process_entry.get())
        m = int(resource_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Enter valid integers for process/resource counts.")
        return

    global alloc_text, max_text, avail_entry
    alloc_text = []
    max_text = []

    tk.Label(matrix_frame, text="Allocation Matrix").grid(row=0, column=0)
    tk.Label(matrix_frame, text="Max Matrix").grid(row=0, column=1)

    for i in range(n):
        a = tk.Text(matrix_frame, height=1, width=20)
        b = tk.Text(matrix_frame, height=1, width=20)
        a.grid(row=i+1, column=0, padx=5, pady=2)
        b.grid(row=i+1, column=1, padx=5, pady=2)
        alloc_text.append(a)
        max_text.append(b)

    tk.Label(matrix_frame, text="Available Resources:").grid(row=n+1, column=0)
    avail_entry = tk.Entry(matrix_frame, width=20)
    avail_entry.grid(row=n+1, column=1, pady=5)

    tk.Button(matrix_frame, text="Run Deadlock Detection", command=submit).grid(row=n+2, columnspan=2, pady=10)

# Setup GUI
root = tk.Tk()
root.title("Deadlock Detection using Banker's Algorithm")

tk.Label(root, text="Number of Processes:").pack()
process_entry = tk.Entry(root)
process_entry.pack()

tk.Label(root, text="Number of Resource Types:").pack()
resource_entry = tk.Entry(root)
resource_entry.pack()

tk.Button(root, text="Create Input Fields", command=create_matrix_inputs).pack(pady=5)

matrix_frame = tk.Frame(root)
matrix_frame.pack()

tk.Label(root, text="Output:").pack()
output_box = tk.Text(root, height=10, width=70)
output_box.pack(pady=5)

root.mainloop()
