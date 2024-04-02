import os

# Paths to the configuration files
CONFIG_AUDIO_DIR_PATH = 'audio_open_location.txt'
CONFIG_TRANSCRIPT_SAVE_DIR_PATH = 'transcript_save_location.txt'


def get_default_folder(config_file_path):
    """
    Retrieves the default folder path from a given configuration file.

    Args:
    - config_file_path: Path to the configuration file storing the default folder path.

    Returns:
    - The path to the default folder if it exists and is valid, otherwise the user's home directory.
    """
    try:
        with open(config_file_path, 'r') as file:
            folder_path = file.readline().strip()
            if os.path.isdir(folder_path):
                return folder_path
    except FileNotFoundError:
        pass
    return os.path.expanduser("~")  # Default to home directory if file doesn't exist or folder is invalid


def set_default_folder(config_file_path, path):
    """
    Sets the default folder path in a given configuration file.

    Args:
    - config_file_path: Path to the configuration file for storing the default folder path.
    - path: The path to the folder to be set as default.
    """
    with open(config_file_path, 'w') as file:
        file.write(path)


def get_default_audio_folder():
    """
    Wrapper function to get the default audio folder from its config file.

    Returns:
    - The default audio folder path.
    """
    return get_default_folder(CONFIG_AUDIO_DIR_PATH)


def set_default_audio_folder(path):
    """
    Wrapper function to set the default audio folder in its config file.

    Args:
    - path: The path to the folder to be set as the default audio folder.
    """
    set_default_folder(CONFIG_AUDIO_DIR_PATH, path)


def get_default_transcript_save_folder():
    """
    Wrapper function to get the default transcript save folder from its config file.

    Returns:
    - The default transcript save folder path.
    """
    return get_default_folder(CONFIG_TRANSCRIPT_SAVE_DIR_PATH)


def set_default_transcript_save_folder(path):
    """
    Wrapper function to set the default transcript save folder in its config file.

    Args:
    - path: The path to the folder to be set as the default transcript save folder.
    """
    set_default_folder(CONFIG_TRANSCRIPT_SAVE_DIR_PATH, path)
