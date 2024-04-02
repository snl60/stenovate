import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
from transcribe import transcribe_audio


def setup_ui(root):
    """
    Sets up the user interface components within the given root window.

    Args:
    - root: The main Tkinter root window.
    """
    root.title("Audio Transcription with Whisper")
    root.geometry("700x600")

    default_font = Font(family="Helvetica", size=14)
    root.option_add("*Font", default_font)

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    image_path = "images/logo.png"  # Ensure this path is correct for your logo image
    img = Image.open(image_path)
    img = img.resize((300, 300), Image.Resampling.LANCZOS)
    photo_img = ImageTk.PhotoImage(img)
    label_image = tk.Label(frame, image=photo_img)
    label_image.image = photo_img  # Keep a reference to prevent garbage collection
    label_image.pack()

    label_text = tk.Label(
        frame,
        text="Click the button below to select an audio file for transcription.",
        wraplength=400, pady=10)

    label_text.pack(pady=30)

    btn_select_audio = tk.Button(
        frame,
        text="Select Audio and Transcribe",
        command=lambda: transcribe_audio(root))
    btn_select_audio.pack()


if __name__ == '__main__':
    root = tk.Tk()
    setup_ui(root)
    root.mainloop()
