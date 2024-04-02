import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.font import Font
from PIL import Image, ImageTk
import whisper
import os


config_file_path = '../transcript_save_location.txt'
audio_dir_config_path = '../audio_open_location.txt'


def get_default_audio_folder():
    try:
        with open(audio_dir_config_path, 'r') as file:
            folder_path = file.readline().strip()
            if os.path.isdir(folder_path):
                return folder_path
    except FileNotFoundError:
        pass
    return os.path.expanduser("~")


def set_default_audio_folder(path):
    with open(audio_dir_config_path, 'w') as file:
        file.write(path)


def get_default_save_folder():
    try:
        with open(config_file_path, 'r') as file:
            folder_path = file.readline().strip()
            if os.path.isdir(folder_path):
                return folder_path
            else:
                return os.path.expanduser("~")
    except FileNotFoundError:
        return os.path.expanduser("~")


def set_default_save_folder(path):
    with open(config_file_path, 'w') as file:
        file.write(path)


def transcribe_audio():
    default_audio_dir = get_default_audio_folder()
    audio_path = filedialog.askopenfilename(
        title="Select Audio File",
        initialdir=default_audio_dir,
        filetypes=(("Audio Files", "*.mp3 *.wav *.m4a *.flac"), ("All Files", "*.*"))
    )
    if not audio_path:
        return

    audio_dir = os.path.dirname(audio_path)
    set_default_audio_folder(audio_dir)

    custom_file_name = simpledialog.askstring(
        "File Name",
        "Enter a name for the transcript file:",
        parent=root)
    if not custom_file_name:
        messagebox.showinfo("Info", "No filename entered. Using default.")
        custom_file_name = os.path.splitext(os.path.basename(audio_path))[0] + "_transcript"
    file_name = custom_file_name + ".txt"

    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    folder_selected = filedialog.askdirectory(
        initialdir=get_default_save_folder(),
        title="Select Folder to Save Transcript"
    )
    if not folder_selected:
        return

    set_default_save_folder(folder_selected)

    transcript_path = os.path.join(folder_selected, file_name)

    if os.path.exists(transcript_path):
        want_to_overwrite = messagebox.askyesno(
            "Overwrite File",
            "The file already exists. Do you want to overwrite it?",
            parent=root
        )
        if not want_to_overwrite:
            return

    with open(transcript_path, 'w') as file:
        file.write(result["text"])



    messagebox.showinfo("Success", f"Transcript saved successfully at:\n{transcript_path}")


root = tk.Tk()
root.title("Audio Transcription with Whisper")
root.geometry("700x600")

default_font = Font(family="Helvetica", size=14)
root.option_add("*Font", default_font)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

image_path = "../images/logo.png"
img = Image.open(image_path)
img = img.resize((300, 300), Image.Resampling.LANCZOS)
photoImg = ImageTk.PhotoImage(img)
labelImage = tk.Label(frame, image=photoImg)
labelImage.pack()

labelText = tk.Label(frame, text="Click the button below to select an audio file for transcription.",
                     wraplength=400,
                     pady=10)
labelText.pack(pady=30)

btn_select_audio = tk.Button(frame, text="Select Audio and Transcribe", command=transcribe_audio)
btn_select_audio.pack()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root.mainloop()
