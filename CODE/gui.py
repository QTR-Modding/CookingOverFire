import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

# Helper Functions for CRUD
def select_yaml_file():
    """
    Opens a file dialog to let the user select a YAML file.

    Returns:
        str: The selected file path or None if no file is selected.
    """
    file_path = filedialog.askopenfilename(
        title="Select YAML File",
        filetypes=[("YAML files", "*.yml *.yaml"), ("All files", "*.*")]
    )
    if file_path:
        return file_path
    else:
        messagebox.showwarning("No file selected", "Please select a file to proceed.")
        return None

def read_yaml_file(file_path):
    """
    Reads the file content as text.

    Args:
        file_path (str): The path of the YAML file to read.

    Returns:
        list: A list of lines read from the file.
    """
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.readlines()
    return []

def write_yaml_file(file_path, lines):
    """
    Writes the given lines to the selected file.

    Args:
        file_path (str): The path of the YAML file to write to.
        lines (list): The list of strings to write.
    """
    with open(file_path, "w") as file:
        file.writelines(lines)

def add_entry(file_path):
    """
    Adds a new key-value entry to the YAML file.
    """
    key = simpledialog.askstring("Input", "Enter key:")
    value = simpledialog.askstring("Input", "Enter value:")
    if key and value:
        lines = read_yaml_file(file_path)
        lines.append(f"{key}: {value}\n")
        write_yaml_file(file_path, lines)
        messagebox.showinfo("Success", f"Entry '{key}' created!")

def read_entries(file_path, output_text):
    """
    Displays the content of the YAML file in the GUI.
    """
    lines = read_yaml_file(file_path)
    output_text.delete("1.0", tk.END)
    if lines:
        for line in lines:
            output_text.insert(tk.END, line)
    else:
        output_text.insert(tk.END, "No entries found.")

def update_entry(file_path):
    """
    Updates an existing key in the YAML file.
    """
    key_to_update = simpledialog.askstring("Input", "Enter key to update:")
    if not key_to_update:
        return
    lines = read_yaml_file(file_path)
    updated_lines = []
    found = False
    for line in lines:
        key, sep, value = line.partition(":")
        if key.strip() == key_to_update:
            new_value = simpledialog.askstring("Input", f"Enter new value for '{key_to_update}':")
            if new_value:
                updated_lines.append(f"{key}: {new_value}\n")
                found = True
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)
    if found:
        write_yaml_file(file_path, updated_lines)
        messagebox.showinfo("Success", f"Entry '{key_to_update}' updated!")
    else:
        messagebox.showerror("Error", f"Key '{key_to_update}' not found!")

def delete_entry(file_path):
    """
    Deletes a key-value entry from the YAML file.
    """
    key_to_delete = simpledialog.askstring("Input", "Enter key to delete:")
    if not key_to_delete:
        return
    lines = read_yaml_file(file_path)
    updated_lines = []
    found = False
    for line in lines:
        key, sep, value = line.partition(":")
        if key.strip() == key_to_delete:
            found = True
            continue
        updated_lines.append(line)
    if found:
        write_yaml_file(file_path, updated_lines)
        messagebox.showinfo("Success", f"Entry '{key_to_delete}' deleted!")
    else:
        messagebox.showerror("Error", f"Key '{key_to_delete}' not found!")

# Main GUI Window
def main():
    root = tk.Tk()
    root.title("YAML CRUD Application (Text-based)")

    file_path = select_yaml_file()
    if not file_path:
        root.destroy()
        return

    # Output Display
    output_text = tk.Text(root, height=15, width=50)
    output_text.pack()

    # Buttons for CRUD Operations
    btn_create = tk.Button(root, text="Create Entry", command=lambda: add_entry(file_path))
    btn_read = tk.Button(root, text="Read Entries", command=lambda: read_entries(file_path, output_text))
    btn_update = tk.Button(root, text="Update Entry", command=lambda: update_entry(file_path))
    btn_delete = tk.Button(root, text="Delete Entry", command=lambda: delete_entry(file_path))

    # Pack Buttons
    btn_create.pack()
    btn_read.pack()
    btn_update.pack()
    btn_delete.pack()

    # Load Initial Data
    read_entries(file_path, output_text)

    # Run the GUI Main Loop
    root.mainloop()

if __name__ == "__main__":
    main()