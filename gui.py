import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def run_compiler():
    code = code_input.get("1.0", tk.END)

    # Save to temp .unn file
    with open("temp_input.unn", "w") as f:
        f.write(code)

    try:
        # Run your compiler build script
        subprocess.run(["./build.sh"], check=True)

        # Read the output file (adjust as per your actual output)
        if os.path.exists("output/output.txt"):
            with open("output/output.txt", "r") as f:
                result = f.read()
        else:
            result = "[No output file generated]"

    except subprocess.CalledProcessError:
        result = "Compilation failed."

    output_display.delete("1.0", tk.END)
    output_display.insert(tk.END, result)

# GUI Layout
root = tk.Tk()
root.title("UNN Compiler GUI")

# Code input pane
code_input = tk.Text(root, height=30, width=60)
code_input.pack(side=tk.LEFT, padx=10, pady=10)

# Output display pane
output_display = tk.Text(root, height=30, width=60, bg="#f0f0f0")
output_display.pack(side=tk.RIGHT, padx=10, pady=10)

# Compile button
compile_button = tk.Button(root, text="Compile and Run", command=run_compiler)
compile_button.pack(pady=5)

root.mainloop()

