# Example GUI for Command line capable machine learning programs

This is an example GUI made in PysimpleGUI and Tkinter, mainly for machine learning programs that lacks simple yet proper GUI. you only need couple of simple python programs with minimal requirements.

It supports:

- Multiple file selection and evaluation
- Re-rendering without reevaluation
- Saving evaluated results
- (Naturally) any ML programs you made in python.

## Installation

1. Clone this repository, or copy all python files to your desired repository.

2. install `PySimpleGUI`, along with other required libraries using pip. you need `numpy`, `Pillow`, `matplotlib`, and `PySimpleGUI`.

    ```bash
    pip install -r requirements.txt
    ```

3. change content in `main.py` to plug in your ML program into GUI. You do not need `evaluate.py` after modification, since what it does is give you some example about how things work.

## Running



  ```bash
  python main.py
  ```
  Please check `main.py` and `evaluate.py` for how things work. `evaluate.py` contains stub evaluator without any 'Evaluation', so technically no Tensorflow / Keras / PyTorch is required.

## Copyrights

This repository follows MIT License. check LICENSE and license at the sidebar for more information. You can also buy me a beer if you think it is worth it.

While this repository **DOES NOT CONTAIN ANY OF THE LIBRARY CODE BELOW**, I think it is great idea to acknowledge the great developers of FOSS libraries.

- Matplotlib: Matplotlib Development Team. https://matplotlib.org/stable/users/project/license.html

- Pillow: Copyright © 2010-2021 by Alex Clark and contributors. https://raw.githubusercontent.com/python-pillow/Pillow/master/LICENSE

- Numpy:  Copyright (c) 2005-2021, NumPy Developers. https://github.com/numpy/numpy/blob/main/LICENSE.txt

- PySimpleGUI: © Copyright 2021 PySimpleGUI, https://github.com/PySimpleGUI/PySimpleGUI/blob/master/license.txt

For example images:

- Water_droplets_on_leaf.jpg:  [Siddharth Patil](https://commons.wikimedia.org/wiki/File:Water_droplets_on_leaf.jpg), CC0, via Wikimedia
- Weidmoos 1.jpg: [Werner100359](https://commons.wikimedia.org/wiki/File:Weidmoos_1.jpg), CC0, via Wikimedia Commons