import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import subprocess
import threading
import os

def run_script():
    result = messagebox.askquestion("Confirmation", "Are you sure you want to run the script?")
    if result == "yes":
        try:
            process = subprocess.Popen(["powershell", "-File", "cleanerBash.ps1"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                log_text.insert(tk.END, line)
                log_text.see(tk.END)  # Otomatik olarak aşağıya kaydırma
            process.wait()
            messagebox.showinfo("Success", "Script execution completed.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "An error occurred while executing the script.")
    else:
        messagebox.showinfo("Cancelled", "Script execution cancelled.")

def open_exclude_file():
    try:
        os.startfile("exclude.txt")
    except FileNotFoundError:
        messagebox.showerror("Error", "exclude.txt file not found.")

def open_header():
    try:
        os.startfile("exclude.txt")
    except FileNotFoundError:
        messagebox.showerror("Error", "exclude.txt file not found.")

def start_thread():
    thread = threading.Thread(target=run_script)
    thread.start()

root = tk.Tk()
root.title("Jalo Cleaner")
root.geometry("500x500")
root.iconbitmap('images\Araz.ico')

# Arka plan rengini ayarla
bg_color = "#343541"
root.configure(bg=bg_color)

# Saydamlık ayarı
root.attributes("-alpha", 0.9)

def show_about():
    messagebox.showinfo("About", "Jalo Cleaner\nVersion 1.0\n\nThis application is developed by Eray Araz at Hybris to clean jalo classes.\n\nThe purpose is to resolve jalo class errors during ant clean all.")


menu_bar = tk.Menu(root)

# Yardım menüsü
info_menu = tk.Menu(menu_bar, tearoff=0)
info_menu.add_command(label="About", command=show_about)

# Exclude Class menüsü
exclude_menu = tk.Menu(menu_bar, tearoff=0)
exclude_menu.add_command(label="Exclude File", command=open_exclude_file)

menu_bar.add_cascade(label="Exclude Class", menu=exclude_menu)
menu_bar.add_cascade(label="About", menu=info_menu)

root.config(menu=menu_bar)

frame = tk.Frame(root, bg=bg_color)
frame.pack(expand=True, fill=tk.BOTH)

log_text = scrolledtext.ScrolledText(frame, bg="white", height=10)
log_text.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

button_frame = tk.Frame(frame, bg=bg_color)
button_frame.pack(pady=20)

run_button = tk.Button(button_frame, text="Clean Jalo", command=start_thread, height=2, width=15)
run_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
