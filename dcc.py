import PySimpleGUI as sg
import os
from correct import correct_image, analyze_video, process_video
import webbrowser
from logo.logo import LOGO

IMAGE_TYPES = (".png", ".jpeg", ".jpg", ".bmp")
VIDEO_TYPES = (".mp4", ".mkv", ".avi")

sg.theme('DarkGrey6')
sg.set_options(font=("Arial", 13))
sg.set_global_icon(LOGO)

left_column = [
    [
        sg.FilesBrowse(button_text="Select photos and videos", enable_events=True, key='__INPUT_FILES__')
    ],
    [
        sg.Listbox(values=[], enable_events=True, size=(50, 20), key="__INPUT_FILE_LIST__")
    ],
    [
        sg.Text("Output folder", size=(15, 1)),
        sg.InputText(default_text="./", size=(25, 1), enable_events=True, readonly=True, background_color='white', key="__OUTPUT_FOLDER__"),
        sg.FolderBrowse()
    ],
    [
        sg.Text(text="Output file prefix", size=(15, 1)),    
        sg.InputText(default_text="corrected", size=(25, 1), key="__OUTPUT_PREFIX__")
    ],
    [
        sg.Button(button_text="Correct All", enable_events=True, pad=(10, 20), button_color='#cc4827', key="__CORRECT__"),
        sg.Button(button_text="Cancel", enable_events=True, pad=(5, 20), disabled=True, key="__CANCEL__"),
        sg.Button(button_text="Clear", enable_events=True, pad=(5, 20), disabled=False, key="__CLEAR_LIST__")
    ],
    [
        sg.Text(text="", size=(20, 1), text_color='yellow', key="__STATUS__")    
    ]
]

info = [
    [
        sg.Text("DCC: Dive Color Corrector", font=('Arial', 30))
    ],
    [
        sg.Text("By"),
        sg.Text("@harsha_bornfree", pad=(1, 0), enable_events=True, text_color='khaki', key='__TWITTER_LINK__'),
    ],
    [
        sg.Text("", pad=(10, 5))
    ],
    [
        sg.Text("An easy and free tool to color correct your dive videos and photos.")
    ],
    [
        sg.Text("Just select your files using the button on top-left and click 'Correct All'.")
    ],
    [
        sg.Text("> No watermarks")
    ],
    [
        sg.Text("> No time limits")
    ],
    [
        sg.Text("> No locked features")
    ],
    [
        sg.Text("", pad=(10, 5))
    ],
    [
        sg.Text("If you found this tool useful, please consider making a donation", text_color='khaki'),
    ],
    [
        sg.Button("Donate", enable_events=True, key="__DONATION_LINK__")
    ],
]

viewer = [
    [
        sg.Frame("", layout=info, key="__INFO__"),
        sg.Image(visible=False, key="__PREVIEW__")
    ]
]

layout = [
    [
        sg.Column(left_column),
        # sg.VSeparator(),
        sg.Column(viewer)
    ]
]

window = sg.Window("DCC: Dive Color Corrector", layout)

def valid_file(path):

    extension = path[path.rfind("."):].lower() 
    return os.path.isfile(path) and (extension in IMAGE_TYPES or extension in VIDEO_TYPES)

def get_files(filepaths):
    input_filepaths = [f for f in filepaths  if valid_file(f)]
    
    for f in input_filepaths:
        yield f
            

file_generator = None
file_index = 0
analyze_video_generator = None
process_video_generator = None


if __name__ == "__main__":

    while True:
        
        event, values = window.read(1)

        if event == sg.WIN_CLOSED:
            break
     
        if event == "__TWITTER_LINK__":
            webbrowser.open("https://twitter.com/harsha_bornfree")           

        if event == "__DONATION_LINK__":
            webbrowser.open("https://buy.stripe.com/28obMb8Mx2EEbRK7ss")

        if event == "__INPUT_FILES__":

            existing_filepaths = [x for x in window["__INPUT_FILE_LIST__"].get_list_values()]
            filepaths = existing_filepaths + values["__INPUT_FILES__"].split(";")

            # Populate listbox with filenames
            input_filepaths = [f for f in filepaths  if valid_file(f)]
            window["__INPUT_FILE_LIST__"].update(input_filepaths)

            # Change output folder to the same as input
            if len(input_filepaths) > 0:
                window["__OUTPUT_FOLDER__"].update(os.path.dirname(input_filepaths[0]))


        if event == "__OUTPUT_FOLDER__":
            window["__OUTPUT_FOLDER__"].update(values["__OUTPUT_FOLDER__"])


        if event == "__CORRECT__":
            filepaths = [x for x in window["__INPUT_FILE_LIST__"].get_list_values()]
            file_generator = get_files(filepaths)

            window["__CORRECT__"].update(disabled=True)
            window["__CANCEL__"].update(disabled=False)
            window["__CLEAR_LIST__"].update(disabled=True)
            window["__PREVIEW__"].update(visible=True)
            window["__INFO__"].update(visible=False)


        if event == "__CANCEL__":
            window["__CORRECT__"].update(disabled=False)
            window["__CANCEL__"].update(disabled=False)
            window["__CLEAR_LIST__"].update(disabled=False)
            window["__PREVIEW__"].update(visible=False)
            window["__INFO__"].update(visible=True)

            file_generator = None
            file_index = 0
            analyze_video_generator = None
            process_video_generator = None

            window["__STATUS__"].update("Cancelled")

        if event == "__CLEAR_LIST__":
            window["__INPUT_FILE_LIST__"].update(values=[])
            window["__STATUS__"].update("")


        if analyze_video_generator:
            try:
                item = next(analyze_video_generator)
                if type(item) == dict:
                    video_data = item
                    process_video_generator = process_video(video_data, True)
                    analyze_video_generator = None
                elif type(item) == int:
                    count = item
                    status_message = f"Analyzing: {count} frames"
                    window["__STATUS__"].update(status_message)
                else:
                    pass

            except StopIteration:
                window["__STATUS__"].update("Analysis done")
                analyze_video_generator = None

            except: 
                window["__STATUS__"].update("Analysis failed")
                analyze_video_generator = None

            continue


        if process_video_generator:
            try:
                percent, preview = next(process_video_generator)
                window["__PREVIEW__"](data=preview)
                status_message = "Processing: {:.2f} %".format(percent)
                window["__STATUS__"].update(status_message)

            except StopIteration:
                window["__STATUS__"].update("Processing done")
                process_video_generator = None

            except:
                window["__STATUS__"].update("Processing failed")
                process_video_generator = None

                
            continue

        if file_generator:

            try:
                f = next(file_generator)
                window["__INPUT_FILE_LIST__"].update(set_to_index=file_index)
                file_index += 1

                new_filename = values["__OUTPUT_PREFIX__"] + "_" + os.path.basename(f)
                output_filepath = os.path.join(values["__OUTPUT_FOLDER__"], new_filename)

                extension = f[f.rfind("."):].lower() 
                
                if extension in IMAGE_TYPES:
                    preview = correct_image(f, output_filepath)
                    window["__PREVIEW__"](data=preview)
                
                if extension in VIDEO_TYPES:
                    window["__STATUS__"].update("Analyzing")
                    analyze_video_generator = analyze_video(f, output_filepath)
            
            except StopIteration:
                window["__STATUS__"].update("All done!")
                window["__CORRECT__"].update(disabled=False)
                window["__CLEAR_LIST__"].update(disabled=False)
                window["__PREVIEW__"].update(visible=False)
                window["__INFO__"].update(visible=True)

                file_generator = None
                file_index = 0
                analyze_video_generator = None
                process_video_generator = None

            except:
                window["__STATUS__"].update("Error in accessing file")
                window["__CORRECT__"].update(disabled=False)
                window["__CLEAR_LIST__"].update(disabled=False)
                window["__PREVIEW__"].update(visible=False)
                window["__INFO__"].update(visible=True)

                file_generator = None
                file_index = 0
                analyze_video_generator = None
                process_video_generator = None
                    
