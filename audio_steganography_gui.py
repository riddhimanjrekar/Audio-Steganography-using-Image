import tkinter as tk
from tkinter import filedialog, messagebox
import os
from encode_audio_in_image import encode_audio_in_image
from decode_audio_from_image import decode_audio_from_image
from audio_steganography_core import encode_audio_in_image, decode_audio_from_image

def encode_action():
    image_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg")])
    audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if not image_path or not audio_path:
        return messagebox.showerror("Error", "Please select both image and audio files.")
    out_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    if out_path:
        encode_audio_in_image(image_path, audio_path, out_path)
        messagebox.showinfo("Success", f"Audio encoded successfully!\nSaved as {out_path}")

def decode_action():
    stego_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg")])
    if not stego_path:
        return messagebox.showerror("Error", "Please select a stego image.")
    out_audio = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("Audio Files", "*.mp3")])
    if out_audio:
        decode_audio_from_image(stego_path, out_audio)
        messagebox.showinfo("Success", f"Audio decoded successfully!\nSaved as {out_audio}")

root = tk.Tk()
root.title("🎵 Audio Steganography Tool ")
root.geometry("400x300")
root.config(bg="#1e1e2f")

tk.Label(root, text="AUDIO STEGANOGRAPHY", bg="#1e1e2f", fg="white", font=("Helvetica", 16, "bold")).pack(pady=20)
tk.Button(root, text=" Encode Audio", command=encode_action, bg="#6c63ff", fg="white", font=("Helvetica", 12, "bold"), width=20).pack(pady=15)
tk.Button(root, text=" Decode Audio", command=decode_action, bg="#00c49a", fg="white", font=("Helvetica", 12, "bold"), width=20).pack(pady=15)
tk.Button(root, text=" Exit", command=root.destroy, bg="#ff5c5c", fg="white", font=("Helvetica", 12, "bold"), width=20).pack(pady=15)

root.mainloop()