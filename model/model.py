import sys
sys.dont_write_bytecode = True
import os
from pathlib import Path
import subprocess

from ultralytics import YOLO


def get_resource_path(relative_path: str) -> Path:
    # Return a Path to a resource, handling PyInstaller's _MEIPASS when frozen
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent
    return base_path / relative_path


def get_save_path() -> Path:
    # Automatically create "saves" directory whenever missing
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS).parent
    else:
        base_path = Path(__file__).resolve().parent.parent
    
    save_path = base_path / "saves"
    save_path.mkdir(parents=True, exist_ok=True)
    return save_path


class YOLO_Face_Detector:
    def __init__(self):
        self.__model = YOLO(get_resource_path("save/best.pt"))
        self.__img_path = None
        self.__confidence = 0.25
        self.__color_mode = "class"
        self.__save_path = get_save_path()
        self.__cur_pred_img = None


    def set_confidence(self, value:float):
        self.__confidence = value


    def set_img_path(self, img_path):
        self.__img_path = get_resource_path(img_path)


    def set_color_mode(self, cmode):
        self.__color_mode = cmode


    def _detect(self):    
        return self.__model.predict(source=self.__img_path, conf=self.__confidence, save=False, stream=False)


    def _save_img(self):
        if not self.__save_path.exists():
            self.__save_path = get_save_path()

        detected = self._detect()

        # Gathering filename components
        img_format = self.__img_path.suffix
        img_name = self.__img_path.stem
        img_save_name = img_name + " output" + img_format
        
        # Base save directory if no duplication
        destination = self.__save_path / img_save_name

        
        while True:
            # Handle duplicated filename: assign a number in the end (e.g. "predicted_image output (1).jpg")
            counter = 1
            # Scan all duplicated filenames iteratively
            while destination.exists():
                # Update filename
                img_save_name = f"{img_name} output ({counter}){img_format}"
                destination = self.__save_path / img_save_name
                counter += 1

            # Core saving mechanic into disk
            detected[0].plot(save=True, filename=destination, line_width=2, color_mode=self.__color_mode, labels=False, show=False)
            
            # If success, save the directory (Path)
            if destination.exists():
                self.__cur_pred_img = destination
                break
            
            # If encounter unsupported extensions, fallback to .jpg and retry
            img_format = ".jpg"
            img_save_name = img_name + " output" + img_format
            destination = self.__save_path / img_save_name
            continue


    def show_img(self):
        self._save_img()

        # Handle different OSs
        opener = {
            'win32': 'explorer',
            'darwin': 'open',
            'linux': 'xdg-open'
        }.get(sys.platform)
        
        subprocess.run([opener, self.__cur_pred_img])
        
        self.__cur_pred_img = None