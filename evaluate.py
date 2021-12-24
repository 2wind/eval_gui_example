import time
import os
from typing import List
import numpy as np
import PySimpleGUI as sg

import utility
from config import *

class MLData:
    """Example MLData class for data compositiing."""
    def __init__(self, path):
        self.path = path
        self.image = utility.load_image(path)
        self.result = None

class StubModel:
    """Stub model that sleeps and returns some stub data."""
    def __init__(self) -> None:
        time.sleep(4)
        print("Model 'initialization' finished")

    def load_weights(self, path: str) -> None:
        """Example weight loading that can take some time."""
        time.sleep(3)
        print(f"Stub model from {path} 'loaded'")

    def detect(self, images:List[np.ndarray]):
        """Example detection function that gets multiple images,
         and returns multiple results(ex. bounding box).
        """
        time.sleep(2)
        print("'detection' complete")

        return [{"key": "values"}] * len(images)



class Evaluator:
    """Example Evaluator that runs on different thread.
    change or inherit as you like for your model.
    """

    def __init__(self, window: sg.Window) -> None:
        self.fixed_data = "Example data"
        self.model = StubModel() # Change to your model.
        self.model.load_weights("DATASET_PATH")
        self.window = window

        self.window.write_event_value(THREAD_EVENT, EVAL_READY) # Send EVAL_READY to main thread.

    def try_evaluate(self, image_paths: List[str], results: List):
        """이미지의 경로들을 받아, 경로에 대해 이미지를 불러오고 evaluate하여 Wood 클래스들을 반환하는 메소드
        evaluate 시작시와 종료시에 THREAD_EVENT를 통해 window에 메시지를 전달한다.
        멀티쓰레딩/프로세싱에 활용할 수 있다.
        """
        print("Loading files...")
        results.clear()

        for path in image_paths:
            try:
                # Load image
                ml_data = MLData(path)
                results.append(ml_data)
            except FileNotFoundError as e:
                print(e)
                print("image not found at ", path)
            except ValueError as e:
                print(e)
                print("Invalid file at ", path)

        print("Starting evaluation...")
        self.window.write_event_value(THREAD_EVENT, EVAL_START)

        for ml_data in results: 
            ml_data.result = self.evaluate(ml_data.image)
            self.window.write_event_value(THREAD_EVENT, EVAL_ONE_COMPLETE)

        self.window.write_event_value(THREAD_EVENT, EVAL_COMPLETE)

    def evaluate(self, image) -> List:
        """example evaluation function for single image. 
        If you want to use it for multiple images, feel free to change
        or create a new version for multiple images
        """
        print(image.shape)
        r = self.model.detect([image])[0]
        print(r)

        return r