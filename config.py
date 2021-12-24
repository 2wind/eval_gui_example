"""Static Strings and lists extracted for easy refactoring.
Can be changed here at once without searching all over the source code.

"""
import os

# 불러올 수 있는 파일 타입 세팅
IMAGE_FILETYPES = (("JPG file", ".jpg"), ("PNG file", ".png"), ("All files", ".*"))

# 경로 관련 세팅
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# 카테고리, 클래스 세팅

# 이미지 설명 부분 format string

# 테마 세팅
WINDOW_THEME = 'DarkAmber'

# Eval thread --> Main thread message
THREAD_EVENT = '-EVALUATION-'
EVAL_READY = 'evaluation_ready'
EVAL_START = 'evaluation_started'
EVAL_ONE_COMPLETE = 'evaluation_one_complete'
EVAL_COMPLETE = 'evaluation_complete'

# output 부분에 출력되는 메시지 부분
TEXT_OUTPUT_INITIAL = "Now loading model..."
TEXT_EVAL_READY = "Ready to evaluate"
TEXT_EVAL_START = "eval started"
TEXT_EVAL_COMPLETE = "eval complete"

# UI에 할당된 키값 및 버튼 제목들 
KEY_CONTROL_GROUP = "control_group"
KEY_OUTPUT_GROUP = "output_group"
KEY_BROWSE_FILES = "browse_files"
KEY_CANVAS = "canvas"
KEY_IMAGE_COLUMN = "image_column"
KEY_OUTPUT = "output"
KEY_SAVE_FILE = 'filename'
BUTTON_OK = "OK"
BUTTON_DETECT = "Detect"
BUTTON_EXIT = "Exit"
BUTTON_SAVE_FILE = "Save As..."
KEY_RERENDER = "Redraw"

