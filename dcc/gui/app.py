"""GUI application for dive color correction."""

import PySimpleGUI as sg
import os
from ..core.correction import correct_image, analyze_video, process_video
import webbrowser
from .logo import LOGO

IMAGE_TYPES = (".png", ".jpeg", ".jpg", ".bmp")
VIDEO_TYPES = (".mp4", ".mkv", ".avi", ".mov")

def create_window():
    """Create and return the main application window."""
    sg.theme("DarkGrey6")
    sg.set_options(font=("Arial", 13))
    sg.set_global_icon(LOGO)

    left_column = [
        [sg.FilesBrowse(button_text="Select photos and videos", enable_events=True, key="__INPUT_FILES__")],
        [sg.Listbox(values=[], enable_events=True, size=(50, 20), key="__INPUT_FILE_LIST__")],
        [
            sg.Text("Output folder", size=(15, 1)),
            sg.InputText(
                default_text="./",
                size=(35, 1),
                key="__OUTPUT_FOLDER__",
            ),
            sg.FolderBrowse(),
        ],
    ]

    right_column = [
        [sg.Text("Preview", size=(15, 1))],
        [sg.Image(key="__PREVIEW__", size=(400, 300))],
        [sg.Button("Process", key="__PROCESS__", disabled=True)],
        [sg.ProgressBar(100, orientation="h", size=(20, 20), key="__PROGRESS__")],
        [sg.Text("", key="__STATUS__")],
    ]

    layout = [
        [
            sg.Column(left_column),
            sg.VSeperator(),
            sg.Column(right_column),
        ]
    ]

    return sg.Window("Dive Color Corrector", layout, finalize=True)

def valid_file(path):
    """Check if file is a valid image or video."""
    return path.lower().endswith(IMAGE_TYPES + VIDEO_TYPES)

def get_files(filepaths):
    """Get list of valid files from filepaths."""
    return [f for f in filepaths if valid_file(f)]

def run_gui():
    """Run the GUI application."""
    window = create_window()
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break
            
        if event == "__INPUT_FILES__":
            files = get_files(values["__INPUT_FILES__"].split(";"))
            window["__INPUT_FILE_LIST__"].update(files)
            window["__PROCESS__"].update(disabled=not files)
            
        if event == "__PROCESS__":
            # Process files logic here
            pass
            
    window.close() 