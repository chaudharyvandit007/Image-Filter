import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

# Apply image filters
def apply_filter(filter_type):
    global img_cv, img_tk
    if img_cv is None:
        return

    filtered = img_cv.copy()

    if filter_type == "Grayscale":
        filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    elif filter_type == "Sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        filtered = cv2.transform(filtered, kernel)
        filtered = np.clip(filtered, 0, 255)
    elif filter_type == "Blur":
        filtered = cv2.GaussianBlur(filtered, (15, 15), 0)
    elif filter_type == "Edge Detection":
        filtered = cv2.Canny(filtered, 100, 200)

    if len(filtered.shape) == 2:
        filtered = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)
    img_pil = Image.fromarray(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
    img_tk = ImageTk.PhotoImage(img_pil)
    panel.config(image=img_tk)
    panel.image = img_tk

# Load image
def load_image():
    global img_cv, img_tk
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if not path:
        return
    img_cv = cv2.imread(path)
    if img_cv is None:
        messagebox.showerror("Error", "Could not load image. Please try again.")
        return
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    img_tk = ImageTk.PhotoImage(img_pil)
    panel.config(image=img_tk)
    panel.image = img_tk

# GUI setup
root = tk.Tk()
root.title("Image Filter App")
root.geometry("600x600")
root.config(bg="#f0f0f0")

img_cv = None
img_tk = None

# Title Label
title_label = tk.Label(root, text="Image Filter App", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=20)

# Panel for image display with dynamic size
panel = tk.Label(root, bg="#dcdcdc", relief="sunken")
panel.pack(pady=10)

# Load image button with custom styling
load_btn = tk.Button(root, text="Load Image", command=load_image, font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="raised", width=20)
load_btn.pack(pady=10)

# Filter buttons with custom styling
filters = ["Grayscale", "Sepia", "Blur", "Edge Detection"]
for f in filters:
    tk.Button(root, text=f, command=lambda ft=f: apply_filter(ft), font=("Helvetica", 12), bg="#2196F3", fg="white", relief="raised", width=20).pack(pady=5)

root.mainloop()
