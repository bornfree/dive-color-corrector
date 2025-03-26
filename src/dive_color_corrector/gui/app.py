"""GUI application for dive color correction."""

import os
from pathlib import Path

import PySimpleGUI as sg

from dive_color_corrector.core.correction import analyze_video, correct_image, process_video
from dive_color_corrector.core.utils.constants import (
    IMAGE_FORMATS,
    VIDEO_FORMATS,
    PREVIEW_WIDTH,
    PREVIEW_HEIGHT,
)

# Window settings
WINDOW_SIZE = (1200, 800)  # Adjusted to accommodate larger preview

def create_window():
    """Create and return the main application window."""
    sg.theme("DarkBlue")
    sg.set_options(font=("Helvetica", 11))
    
    # Create file type filter string
    file_types = (
        ("Images", list(IMAGE_FORMATS.keys())),
        ("Videos", list(VIDEO_FORMATS.keys())),
    )
    
    layout = [
        [sg.Text("Dive Color Corrector", font=("Helvetica", 16, "bold"), justification="center", expand_x=True)],
        [sg.HSeparator()],
        [
            sg.Column([
                [sg.Text("Input Files", font=("Helvetica", 12, "bold"))],
                [sg.FilesBrowse("Select Files", file_types=file_types),
                 sg.Button("Clear Selection", key="-CLEAR-")],
                [sg.Listbox(values=[], size=(40, 15), key="-FILE_LIST-", enable_events=True)],
                [sg.HSeparator()],
                [sg.Text("Processing Options", font=("Helvetica", 12, "bold"))],
                [sg.Checkbox("Use Deep Learning Model", key="-USE_DEEP-", default=False)],
            ], expand_y=True),
            sg.VSeparator(),
            sg.Column([
                [sg.Text("Preview", font=("Helvetica", 12, "bold"))],
                [sg.Image(key="-PREVIEW-", size=(PREVIEW_WIDTH // 2, PREVIEW_HEIGHT // 2))],
                [sg.HSeparator()],
                [sg.Text("Output Folder:", size=(12, 1)),
                 sg.Input(default_text=str(Path.home() / "Pictures" / "Corrected"), key="-OUTPUT-", size=(30, 1)),
                 sg.FolderBrowse()],
                [sg.HSeparator()],
                [sg.Button("Process Files", key="-PROCESS-", disabled=True, size=(20, 1))],
                [sg.ProgressBar(100, orientation="h", size=(30, 20), key="-PROGRESS-")],
                [sg.Text("", key="-STATUS-", size=(40, 1))],
            ], expand_y=True),
        ],
    ]

    return sg.Window("Dive Color Corrector", layout, size=WINDOW_SIZE, finalize=True)

def valid_file(path):
    """Check if file is a valid image or video."""
    return path.lower().endswith(tuple(IMAGE_FORMATS.keys()) + tuple(VIDEO_FORMATS.keys()))

def get_files(filepaths):
    """Get list of valid files from filepaths."""
    return [f for f in filepaths.split(";") if valid_file(f)]

def process_files(window, files, output_folder):
    """Process the selected files."""
    total_files = len(files)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get processing method from checkbox
    use_deep = window["-USE_DEEP-"].get()

    for i, file in enumerate(files, 1):
        filename = Path(file).name
        output_file = output_path / f"corrected_{filename}"

        window["-STATUS-"].update(f"Processing {filename}...")
        window["-PROGRESS-"].update((i * 100) // total_files)
        window.refresh()

        try:
            if file.lower().endswith(tuple(IMAGE_FORMATS.keys())):
                preview_data = correct_image(file, str(output_file), use_deep=use_deep)
                window["-PREVIEW-"].update(data=preview_data)
            else:  # Video file
                for data in analyze_video(file, str(output_file)):
                    if isinstance(data, dict):
                        video_data = data
                    else:
                        window["-PROGRESS-"].update((data * 100) // video_data["frame_count"])
                        window.refresh()

                for progress, preview in process_video(video_data, yield_preview=True, use_deep=use_deep):
                    if preview:
                        window["-PREVIEW-"].update(data=preview)
                    window["-PROGRESS-"].update(progress)
                    window.refresh()
        except Exception as e:
            window["-STATUS-"].update(f"Error processing {filename}: {str(e)}")
            continue

    window["-STATUS-"].update("Processing complete!")
    window["-PROGRESS-"].update(100)

def run_gui():
    """Run the GUI application."""
    window = create_window()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-CLEAR-":
            window["-FILE_LIST-"].update([])
            window["-PROCESS-"].update(disabled=True)
            window["-PREVIEW-"].update(data=None)
            window["-STATUS-"].update("")
            window["-PROGRESS-"].update(0)

        if event == "-FILE_LIST-":
            files = values["-FILE_LIST-"]
            window["-PROCESS-"].update(disabled=not files)
            if files:
                # Show preview of first selected file
                if files[0].lower().endswith(tuple(IMAGE_FORMATS.keys())):
                    preview_data = correct_image(files[0], None, use_deep=values["-USE_DEEP-"])  # None to skip saving
                    window["-PREVIEW-"].update(data=preview_data)

        if event == "-PROCESS-":
            files = values["-FILE_LIST-"]
            output_folder = values["-OUTPUT-"]
            process_files(window, files, output_folder)

    window.close()
