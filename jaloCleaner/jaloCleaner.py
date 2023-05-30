import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import threading
import os
import shutil
import datetime

script_directory = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(script_directory, "cleanerBash.ps1")
ico_path = os.path.join(script_directory, "images/Araz.ico")

current_script_directory = os.path.dirname(os.path.abspath(__file__))
parent_current_script_directory = os.path.dirname(current_script_directory)

current_date_time = datetime.datetime.now().strftime("%d-%m-%Y-%I-%p")

log_folder = os.path.join(current_script_directory, "log")

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file_path = os.path.join(log_folder, f"logfiles-{current_date_time}.log")
exclude_file_path = os.path.join(current_script_directory, "exclude.txt")

exclude_class_names = []
with open(exclude_file_path, "r") as exclude_file:
    exclude_class_names = exclude_file.read().splitlines()

main_folder = parent_current_script_directory
file_extensions = [".class", ".java"]


def run_script():
    result = messagebox.askquestion("Confirmation", "Are you sure you want to run the script?")
    if result == "yes":
        try:
            start_delete_jalo_classes()
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "An error occurred while executing the script.")
    else:
        messagebox.showinfo("Cancelled", "Script execution cancelled.")


# Function: Delete Jalo classes
def delete_jalo_classes(folder):
    subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]
    for subfolder in subfolders:
        if os.path.basename(subfolder) == "jalo":
            message = f"Jalo folder found: {subfolder}"
            with open(log_file_path, "a") as log_file:
                log_file.write(message + "\n")
            log_text.insert(tk.END, message + "\n")
            log_text.see(tk.END)

            print(message)
            files = [
                f.path
                for f in os.scandir(subfolder)
                if f.is_file() and f.name.endswith(tuple(file_extensions))
            ]
            for file in files:
                file_name = os.path.basename(file)
                if file_name in exclude_class_names:
                    message = f"Excluded Jalo class found: {file_name}"
                    with open(log_file_path, "a") as log_file:
                        log_file.write(message + "\n")
                    print(message)
                else:
                    message = f"Deleting Jalo class: {file}"
                    with open(log_file_path, "a") as log_file:
                        log_file.write(message + "\n")
                    print(message)
                    os.remove(file)
        else:
            delete_jalo_classes(subfolder)


def start_delete_jalo_classes():
    start_time = datetime.datetime.now()
    delete_jalo_classes(main_folder)
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    message = f"All Jalo classes successfully deleted. Total time: {duration.total_seconds()} seconds"
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)

    log_text.tag_configure("bold_green", font=("Arial", 10, "bold"), foreground="green")
    log_text.tag_add("bold_green", "end-2l", "end-1c")  # Apply bold and green style
    with open(log_file_path, "a") as log_file:
        log_file.write(message + "\n")


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
root.iconbitmap(ico_path)

# Set background color
bg_color = "#343541"
root.configure(bg=bg_color)

# Set transparency
root.attributes("-alpha", 0.9)


def show_about():
    messagebox.showinfo(
        "About",
        "Jalo Cleaner\nVersion 1.0\n\n"
        "This application is developed by Eray Araz at Hybris to clean jalo classes.\n\n"
        "The purpose is to resolve jalo class errors during ant clean all.",
    )


menu_bar = tk.Menu(root)

# Help menu
info_menu = tk.Menu(menu_bar, tearoff=0)
info_menu.add_command(label="About", command=show_about)

# Exclude Class menu
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

run_button = tk.Button(
    button_frame, text="Clean Jalo", command=start_thread, height=2, width=15
)
run_button.pack(side=tk.LEFT, padx=10)

root.mainloop()

