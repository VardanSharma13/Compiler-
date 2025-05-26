import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os

# Function to run your custom language code
def run_custom_code(file_path):
    # Pehle build.sh chalaye (jo tera C project compile karta hai)
    build_process = subprocess.run(["bash", "../build.sh"], capture_output=True, text=True, cwd=os.path.dirname(__file__))
    if build_process.returncode != 0:
        return f"Build Error:\n{build_process.stderr}"

    # Fir tera compiled program run kare, input .unn file ke saath
    run_process = subprocess.run(["./a.out", file_path], capture_output=True, text=True, cwd="..")
    if run_process.returncode != 0:
        return f"Runtime Error:\n{run_process.stderr}"

    return run_process.stdout

def open_file():
    file_path = filedialog.askopenfilename(
        title="Open .unn file",
        filetypes=[("UNN files", "*.unn"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as f:
            code_text.delete("1.0", tk.END)
            code_text.insert(tk.END, f.read())
        status_label.config(text=f"Opened: {file_path}")
        window.file_path = file_path

def save_file():
    if hasattr(window, "file_path"):
        path = window.file_path
    else:
        path = filedialog.asksaveasfilename(
            defaultextension=".unn",
            filetypes=[("UNN files", "*.unn"), ("All files", "*.*")]
        )
        window.file_path = path

    if path:
        with open(path, "w") as f:
            f.write(code_text.get("1.0", tk.END))
        status_label.config(text=f"Saved: {path}")

def run_code():
    # Save current editor content first
    save_file()
    output_text.delete("1.0", tk.END)

    if not hasattr(window, "file_path") or not window.file_path:
        messagebox.showerror("Error", "No file to run! Please open or save a .unn file.")
        return

    output_text.insert(tk.END, "Running...\n")
    window.update()

    output = run_custom_code(window.file_path)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)

# Tkinter Window setup
window = tk.Tk()
window.title("Custom Language GUI")
window.geometry("900x700")

# Menu bar
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)
window.config(menu=menubar)

# Code editor label
tk.Label(window, text="Code Editor (.unn):").pack(anchor="w", padx=10, pady=(10,0))

# Code editor text box
code_text = scrolledtext.ScrolledText(window, wrap=tk.NONE, font=("Consolas", 12))
code_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Run button
run_button = tk.Button(window, text="▶️ Play", font=("Arial", 14, "bold"), bg="green", fg="white", command=run_code)
run_button.pack(pady=10)

# Output label
tk.Label(window, text="Output:").pack(anchor="w", padx=10)

# Output text box (read-only)
output_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Consolas", 12), height=10, state=tk.NORMAL)
output_text.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0,10))

# Status bar label
status_label = tk.Label(window, text="Welcome! Open or create a .unn file.", bd=1, relief=tk.SUNKEN, anchor="w")
status_label.pack(fill=tk.X, side=tk.BOTTOM)

window.mainloop()

