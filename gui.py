import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def run_pipeline():
    # Get code from left editor
    code = code_input.get("1.0", tk.END)

    # Save to temp file
    with open("temp_input.unn", "w") as f:
        f.write(code)

    try:
        # Step 1: Compile the compiler (build.sh)
        subprocess.run(["bash", "build.sh"], check=True)

        # Step 2: Run the compiler to generate output
        subprocess.run(["./build/unn", "temp_input.unn", "output"], check=True)

        # Step 3: Run the final output executable
        result = subprocess.run(["./output"], capture_output=True, text=True)

        # Display output
        output_display.delete("1.0", tk.END)
        output_display.insert(tk.END, result.stdout if result.stdout else "[No Output]")
        if result.stderr:
            output_display.insert(tk.END, "\n[Errors:]\n" + result.stderr)

    except subprocess.CalledProcessError as e:
        output_display.delete("1.0", tk.END)
        output_display.insert(tk.END, f"Error:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("UNN Language IDE")
root.geometry("1200x600")

# Code Editor (Left)
code_input = tk.Text(root, height=30, width=70, font=("Courier", 12))
code_input.pack(side=tk.LEFT, padx=10, pady=10)

# Output Viewer (Right)
output_display = tk.Text(root, height=30, width=70, font=("Courier", 12), bg="#f0f0f0")
output_display.pack(side=tk.RIGHT, padx=10, pady=10)

# Run Button
run_button = tk.Button(root, text="Compile & Run", font=("Arial", 14), command=run_pipeline)
run_button.pack(pady=5)

root.mainloop()
