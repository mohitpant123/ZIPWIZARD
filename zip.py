import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import zipfile
import os
from PIL import Image, ImageTk

def compress_files():
    files = filedialog.askopenfilenames(title="Select Files to Compress")
    if not files:
        return
    save_path = filedialog.asksaveasfilename(title="Save Compressed File As", defaultextension=".zip")
    if not save_path:
        return
    with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    status_label.config(text=f"Compressed: {len(files)} files -> {save_path}")

def decompress_file():
    archive_path = filedialog.askopenfilename(title="Select Archive to Decompress", filetypes=[("ZIP files", "*.zip")])
    if not archive_path:
        return
    extract_folder = filedialog.askdirectory(title="Select Destination Folder")
    if not extract_folder:
        return
    with zipfile.ZipFile(archive_path, 'r') as zipf:
        zipf.extractall(extract_folder)
    status_label.config(text=f"Decompressed: {archive_path} -> {extract_folder}")

def preview_archive():
    archive_path = filedialog.askopenfilename(title="Select Archive to Preview", filetypes=[("ZIP files", "*.zip")])
    if not archive_path:
        return
    try:
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            files = zipf.namelist()
            messagebox.showinfo("Archive Contents", "\n".join(files))
    except zipfile.BadZipFile:
        messagebox.showerror("Error", "Invalid or corrupted ZIP file.")

# Create the main window
root = tk.Tk()
root.title("ZipWizard (for Windows)")
root.geometry("400x500")  # Adjust window size

# Add an icon to the application
try:
    root.iconbitmap("e.ico")  # Ensure 'e.ico' is in the same directory as your Python script
except Exception as e:
    print(f"Error loading icon: {e}")

# Style buttons as rounded rectangles
style = ttk.Style()
style.configure("Rounded.TButton", font=("Arial", 12), padding=10, relief="flat", borderwidth=0)

# Add buttons to the GUI
compress_button = ttk.Button(root, text="Compress Files to ZIP", command=compress_files, style="Rounded.TButton")
compress_button.pack(pady=10)

decompress_button = ttk.Button(root, text="Decompress ZIP File", command=decompress_file, style="Rounded.TButton")
decompress_button.pack(pady=10)

preview_button = ttk.Button(root, text="Preview ZIP Contents", command=preview_archive, style="Rounded.TButton")
preview_button.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack(pady=10)

# Add a smiley with a zipped face
try:
    smiley_image = Image.open("e.png")  # Replace with the path to your smiley image
    smiley_image = smiley_image.resize((200, 200), Image.Resampling.LANCZOS)  # Updated method
    smiley_photo = ImageTk.PhotoImage(smiley_image)
    smiley_label = tk.Label(root, image=smiley_photo)
    smiley_label.image = smiley_photo  # Keep a reference to avoid garbage collection
    smiley_label.place(relx=0.9, rely=0.9, anchor="se")  # Position at bottom-right
except Exception as e:
    print(f"Error loading smiley image: {e}")

# Run the application
root.mainloop()
