from tkinter import filedialog, messagebox, simpledialog

import torch.cuda
import whisper
import os
from config import (
    get_default_audio_folder,
    set_default_audio_folder,
    get_default_transcript_save_folder,
    set_default_transcript_save_folder
)


def prompt_for_custom_filename(root, default_name):
    """
    Prompts the user for a custom filename, providing a default based on the audio file name.

    Args:
    - root: The main Tkinter root window.
    - default_name: The default file name suggested to the user.

    Returns:
    - The custom file name entered by the user or the default name if none is provided.
    """
    custom_file_name = simpledialog.askstring(
        "File Name",
        "Enter a name for the transcript file:",
        parent=root
    )
    if not custom_file_name:
        messagebox.showinfo("Info", "No filename entered. Using default.")
        return default_name
    return custom_file_name


def check_for_overwrite_and_proceed(root, file_path):
    """
    Checks if a file at the given path exists and prompts the user to confirm overwriting.

    Args:
    - root: The main Tkinter root window.
    - file_path: The path to the file that might be overwritten.

    Returns:
    - True if the file doesn't exist or the user confirms overwriting, False otherwise.
    """
    if os.path.exists(file_path):
        return messagebox.askyesno(
            "Overwrite File",
            "The file already exists. Do you want to overwrite it?",
            parent=root
        )
    return True


def transcribe_audio(root):
    """
    Handles the audio file selection, transcription, and saving of the transcript to a file.

    Args:
    - root: The main Tkinter root window.
    """
    # Step 1: Select audio file
    default_audio_dir = get_default_audio_folder()
    audio_path = filedialog.askopenfilename(
        title="Select Audio File",
        initialdir=default_audio_dir,
        filetypes=(("Audio Files", "*.mp3 *.wav *.m4a *.flac"), ("All Files", "*.*"))
    )
    if not audio_path:
        return  # Exit if user cancels

    # Update the default directory based on user's choice
    audio_dir = os.path.dirname(audio_path)
    set_default_audio_folder(audio_dir)

    # Step 2: Select folder for saving the transcript
    folder_selected = filedialog.askdirectory(
        initialdir=get_default_transcript_save_folder(),
        title="Select Folder to Save Transcript"
    )
    if not folder_selected:
        return

    # Update the save folder to the newly selected folder
    set_default_transcript_save_folder(folder_selected)

    # Step 3: Prompt for custom filename after selecting save folder
    default_file_name = os.path.splitext(os.path.basename(audio_path))[0] + "_transcript.txt"
    custom_file_name = prompt_for_custom_filename(root, default_file_name)
    transcript_path = os.path.join(folder_selected, custom_file_name)

    # Check if the transcript file already exists and confirm overwrite if necessary
    if not check_for_overwrite_and_proceed(root, transcript_path):
        return  # Exit if the user does not want to overwrite existing file

    # Step 4: Load and transcribe audio using Whisper
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("base", device=device)
    result = model.transcribe(audio_path)
    text = result["text"]
    corrected_text = text.replace("Stenevate", "Stenovate")

    with open(transcript_path, 'w') as file:
        file.write(corrected_text)

    # Inform the user of success
    messagebox.showinfo(
        "Success",
        f"Transcript saved successfully at:\n{transcript_path}"
    )
