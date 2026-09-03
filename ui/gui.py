import sys
sys.dont_write_bytecode = True

import tkinter as tk
from tkinter import filedialog
from model.model import YOLO_Face_Detector
import webbrowser
from pathlib import Path


def get_resource_path(relative_path: str) -> Path:
    """Return a Path to a resource, handling PyInstaller's _MEIPASS when frozen."""
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent
    return base_path / relative_path


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YOLO Face Detector")
        self.root.geometry("640x480")
        self.root.resizable(False, False)

        self.yolo_model = YOLO_Face_Detector()
        self.model_conf = tk.IntVar(value=25)
        self.model_conf.trace_add("write", self._validate_conf_entry)
        self.src_btn_icon = tk.PhotoImage(file=str(get_resource_path("ui/assets/github_icon.png")))

        self.force_numeric_entry = self.root.register(self._force_conf_numeric)
        self.root.bind_all("<Button-1>", self._clear_focus)


        self.exec_btn = tk.Button(
            self.root,
            text="Open an Image File",
            command=self._get_yolo_result,
            font=("Helvetica", 20, "bold italic"),
            relief='raised',
            activebackground="gray",
            cursor="hand2",
            bd=5,
            width=20, height=2)
        self.exec_btn.place(relx=0.5, rely=0.3, anchor='center')


        self.model_conf.trace_add("write", self._change_confidence)
        self.conf_slider = tk.Scale(
            self.root,
            variable=self.model_conf,
            from_=0, to=100,
            orient='horizontal',
            resolution=1, length=200,
            showvalue=False,
            label="Detector's confidence",
            font=("Helvetica", 12, "bold")
        )
        self.conf_slider.place(relx=0.5, rely=0.5, anchor='center')
        self.conf_slider.set(75)

        self.conf_entry = tk.Entry(
            self.root,
            width=5,
            font=("Helvetica", 12),
            textvariable=self.model_conf,
            validate="key",
            validatecommand=(self.force_numeric_entry, "%P")
        )
        self.conf_entry.place(relx=0.7, rely=0.52, anchor="center")


        color_mode_var = tk.IntVar(value=1)
        self.radio_label = tk.Label(
            self.root,
            text="Box Color Mode",
            font=("Helvetica", 12, "bold")
        )
        self.radio_label.place(relx=0.5, rely=0.65, anchor="center")
        
        tk.Radiobutton(
            self.root, text="Identical",
            font=("Helvetica", 12, "italic"),
            variable=color_mode_var, value=1, cursor="hand2", 
            command=lambda: self.yolo_model.set_color_mode("class")
            ).place(relx=0.4, rely=0.7, anchor='center')
        
        tk.Radiobutton(
            self.root, text="Diverse",
            font=("Helvetica", 12, "italic"),
            variable=color_mode_var, value=2, cursor="hand2",
            command=lambda: self.yolo_model.set_color_mode("instance")
            ).place(relx=0.6, rely=0.7, anchor='center')


        self.url_btn = tk.Button(
            self.root,
            command=lambda:webbrowser.open("https://github.com/thangkaka26/YOLO-Face-Detector-GUI-App"),
            image=self.src_btn_icon,
            activebackground="gray",
            relief='raised',
            cursor="hand2",
            bd=5,
            width=50, height=50
        )
        self.url_btn.image = self.src_btn_icon 
        self.url_btn.place(relx=0.98, rely=0.98, anchor='se')


        self.root.mainloop()


    def _validate_conf_entry(self, *args):
        try:
            current = self.model_conf.get()
            self.model_conf.set(int(current))

            if (current < 0):
                self.model_conf.set(0)
            elif (current > 100):
                self.model_conf.set(100)
        
        except:
            self.model_conf.set(75)


    def _force_conf_numeric(self, text):
        if (text == "") or (text.isdigit()):
            return True
        return False

    
    def _clear_focus(self, event):
        if not (isinstance(event.widget, tk.Entry)):
            self.root.focus_set()


    def _get_yolo_result(self):
        try:
            img_path = filedialog.askopenfilename(
                parent=self.root,
                title="Select an Image File",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.tga *.jfif *.webp *avif"),
                    ("JPEG", "*.jpg *.jpeg *.jpe *.jfif *.exif"), ("PNG", "*.png"), ("TGA", "*.tga"),
                    ("AV1 (AVIF)", "*.avif"), ("WebP", "*.webp")]
            )
            if (img_path):
                self.yolo_model.set_img_path(img_path)
                self.yolo_model.show_img()
        except:
            pass


    def _change_confidence(self, *args):
        raw_value = self.model_conf.get()
        parsed_value = 1 - (raw_value / 100)
        return self.yolo_model.set_confidence(parsed_value)