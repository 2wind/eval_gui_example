from typing import List

from numpy import ndarray
import matplotlib.pyplot as plt
import threading
# import tensorflow as tf

from PIL import Image, ImageTk
import PySimpleGUI as sg

from config import *
import evaluate
import utility

# Global variables
input_values = [] # Input values for evaluator (ex. image paths)
ml_datas = [] # Output values from evaluator (ex. evaluated raw data)
display_image = None # Image displayed.
window = None # main window.
eval_event = threading.Event()

def initialize_window() -> sg.Window:
    sg.theme(WINDOW_THEME)
    sg_image = sg.Image(size=(900, 9000), key=KEY_CANVAS, expand_x=True, expand_y=True)
    image_column = [[sg.pin(
        sg.Column([[sg_image]], key=KEY_IMAGE_COLUMN, visible=False, scrollable=True, expand_x=True, expand_y=True)
        )]]
    output_text = sg.Text(TEXT_OUTPUT_INITIAL, key=KEY_OUTPUT)
    control_group = [[sg.Input(key='_FILES_'), sg.FilesBrowse(key=KEY_BROWSE_FILES, file_types=IMAGE_FILETYPES, initial_folder=DIR_PATH, disabled=True)],
                [sg.OK(button_text=BUTTON_DETECT, key=BUTTON_DETECT, disabled=True),
                 sg.FileSaveAs(
                    key=BUTTON_SAVE_FILE,
                    target=KEY_SAVE_FILE,
                    file_types=IMAGE_FILETYPES, 
                    default_extension=".jpg",
                    disabled=True
                ), 
                 sg.In(key=KEY_SAVE_FILE, enable_events=True, visible=False)],
                [sg.Submit(KEY_RERENDER, key=KEY_RERENDER, disabled=True)],
                [output_text]]
    output_group = [[sg.Output(size=(200, 10))]]
    # output_group = [[sg.Text("__")]] # Dummy group for evaluation
    layout = [[sg.Column(control_group, key=KEY_CONTROL_GROUP), sg.Column(output_group, key=KEY_OUTPUT_GROUP)],
                [image_column]]
    window = sg.Window('Example GUI for ML Project', resizable=True, auto_size_text=True, size=(900, 800), finalize=True).Layout(layout)

    return window

def create_thread(window:sg.Window, result_values:List[evaluate.MLData], eval_event:threading.Event):
    evaluator = evaluate.Evaluator(window)
    print("evaluator ready")
    while True:
        eval_event.wait()
        print("starting...")
        evaluator.try_evaluate(input_values, result_values)
        eval_event.clear()
        
    # Do evaluator clearing action here


def excepthook(args):
    print(args)
    # TODO: reactivate buttons in main thread when exception happens in other thread
    # disable_buttons(window, False)
    eval_event.clear()
    print("Unknown problem while evaluating. Run inside console to see tensorflow debug messages.")
    print("Possibly: Your GPU may not have enough memory to run model. Try running it in a CPU mode.")


threading.excepthook = excepthook

def main() -> None:
    # Initialize Window
    window = initialize_window()

    # Set memory growth for all GPUs to use least VRAM possible
    # gpus = tf.config.experimental.list_physical_devices('GPU')
    # for gpu in gpus:
    #     tf.config.experimental.set_memory_growth(gpu, True)   

    # Initialize evaluator with default window
    eval_thread = threading.Thread(target=create_thread, args=(window, ml_datas, eval_event), daemon=True)
    eval_thread.start()

    # Main loop
    while True:
        event, values = window.Read()

        if event == sg.WIN_CLOSED or event == 'Cancel' or event == BUTTON_EXIT: # if user closes window or clicks cancel
            break

        if (event == KEY_RERENDER): # if Rerender without evaluating
            display_image = draw_on_image(window, ml_datas)

        if (event.startswith(BUTTON_DETECT)): # if user presses Detect button
            window[KEY_IMAGE_COLUMN].Update(visible = False)
            input_values.clear()
            input_values.extend(values['_FILES_'].split(';'))
            print(input_values)
            try:
                # physical_devices = tf.config.list_physical_devices('GPU')
                # print("GPU Available: ", len(physical_devices))
                disable_buttons(window, True)
                eval_event.set()

            except Exception as e:
                eval_event.clear()
                disable_buttons(window, False)
                print(e)
                print("Unknown problem while evaluating. Run inside console to see tensorflow debug messages.")
                print("Possibly: Your GPU may not have enough memory to run model. Try running it in a CPU mode.")

        if (event.startswith(KEY_SAVE_FILE)): # if user closes file save dialog
            print("Try Saving file...")
            try:
                filename = values['filename']
                print(filename)
                display_image.convert('RGB').save(filename)
                print("Image saved")
            except Exception as e:
                print(e)
            
        if (event == THREAD_EVENT): # if try_evaluate signals THREAD_EVENT
            if values[THREAD_EVENT] == EVAL_READY:
                disable_buttons(window, False)
                window[KEY_OUTPUT].Update(value=TEXT_EVAL_READY)
            if values[THREAD_EVENT] == EVAL_START:
                window[KEY_OUTPUT].Update(value=TEXT_EVAL_START)
            if values[THREAD_EVENT] == EVAL_COMPLETE:
                window[KEY_OUTPUT].Update(value=TEXT_EVAL_COMPLETE)
                disable_buttons(window, False)
                display_image = draw_on_image(window, ml_datas)

    window.close()

def disable_buttons(window, disabled):
    window[BUTTON_DETECT].Update(disabled=disabled)
    window[KEY_SAVE_FILE].Update(disabled=disabled)
    window[KEY_BROWSE_FILES].Update(disabled=disabled)
    window[BUTTON_SAVE_FILE].Update(disabled=disabled)
    window[KEY_RERENDER].Update(disabled=disabled)


def draw_on_image(window: sg.Window, ml_datas:List[evaluate.MLData]) -> Image.Image:
    """
    Draw contents of RESULTS inside WINDOW.
    """
    print(f"drawing {len(ml_datas)} image(s)...")
    sg_image = window[KEY_CANVAS]
    display_image = None
    try:
        fig, axs = plt.subplots(nrows=len(ml_datas), ncols=1)

        for i, ml_data in enumerate(ml_datas):
            ax = axs[i] if type(axs) == ndarray else axs
            ax.set_anchor('N')

            # use drawing function that might come with your ML Package,
            # or simple draw image and data on ax using ml_data.
            ax.text(0, 0, ml_data.result["key"])
            ax.imshow(ml_data.image)


            
        fig.set_dpi(120)
        fig.subplots_adjust(left=0, right=1, wspace=0.01, hspace=0.15)
        # FIXME: magic number 대신, 추가 legend 비례한 값으로 fig 크기 늘리기
        height = 2.3 * len(ml_datas)
        fig.set_size_inches(7, height, forward=True)
        fig.tight_layout()

        display_image = Image.fromarray(utility.figure_to_array(fig))
        result_image = ImageTk.PhotoImage(image=display_image)
        # display image in main screen
        sg_image.update(data=result_image)
        window.refresh()    
        window[KEY_IMAGE_COLUMN].contents_changed()
        window[KEY_IMAGE_COLUMN].Update(visible = True)

    except ValueError as e:
        print(e)
        print("length of data detected is ", len(ml_datas))
    finally:
        return display_image


if __name__ == "__main__":
    main()
