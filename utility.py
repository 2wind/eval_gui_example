from matplotlib import patches, pyplot as plt
import numpy as np
import skimage

from skimage.measure import find_contours
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from config import *

"""
Utility functions for image processing and display.
Some of them are oringinally from Masked R-CNN library.
(https://github.com/matterport/Mask_RCNN)
(Copyright (c) 2017 Matterport, Inc. Licensed under the MIT License (see LICENSE for details) Written by Waleed Abdulla)
"""


def load_image(path):
    """Load the specified image and return a [H,W,3] Numpy array.
        Changed from mrcnn/utils.py
    """
    # Load image
    image = skimage.io.imread(path)
    # If grayscale. Convert to RGB for consistency.
    if image.ndim != 3:
        image = skimage.color.gray2rgb(image)
    # If has an alpha channel, remove it for consistency
    if image.shape[-1] == 4:
        image = image[..., :3]
    return image



def draw_figure(canvas, fig) -> None:
    """
    https://stackoverflow.com/questions/64403707/interactive-matplotlib-plot-in-pysimplegui
    ------------------------------- This is to include a matplotlib figure in a Tkinter canvas
    """
    if canvas and canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)


# https://frhyme.github.io/python-lib/figure_to_np_array/

def figure_to_array(fig: plt.figure) -> np.ndarray:
    """
    plt.figure를 RGBA로 변환(layer가 4개)
    shape: height, width, layer
    """
    fig.canvas.draw()
    return np.array(fig.canvas.renderer._renderer)

