import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

import cv2
from PIL import Image, ImageTk

from config import VIEWER_HEIGHT
from utils import VideoReader, process_video


class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player with Frame Counter")
        self.vid_reader = None
        self.playing = False
        self.stop_signal = threading.Event()
        self.video_thread = None
        self.start_frame = 0
        self.queue = queue.Queue()
        self.video_info_label = tk.Label(root, text="")
        self.video_info_label.pack(pady=10)
        self.btn_open = tk.Button(
            root, text="Open Video", command=self.open_video
        )
        self.btn_open.pack(pady=10)
        self.canvas = tk.Canvas(root, bg="black")
        self.canvas.pack(pady=20)
        self.label_frame_num = tk.Label(root, text="Frame: 0")
        self.label_frame_num.pack(pady=10)
        self.btn_start = tk.Button(
            root, text="Start", command=self.start_video
        )
        self.btn_start.pack(side=tk.LEFT, padx=10)
        self.btn_stop = tk.Button(root, text="Stop", command=self.stop_video)
        self.btn_stop.pack(side=tk.LEFT, padx=10)
        self.btn_reset = tk.Button(
            root, text="Reset", command=self.reset_video
        )
        self.btn_reset.pack(side=tk.LEFT, padx=10)
        self.btn_process_save = tk.Button(
            root, text="Process & Save", command=self.process_and_save
        )
        self.btn_process_save.pack(pady=10)

    def open_video(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        self.vid_reader = VideoReader(filepath)
        original_width, original_height = self.vid_reader.get_size()
        aspect_ratio = original_width / original_height
        if original_height > VIEWER_HEIGHT:
            new_height = VIEWER_HEIGHT
            new_width = int(new_height * aspect_ratio)
        else:
            new_height = int(original_height)
            new_width = int(original_width)
        self.new_size = (new_width, new_height)
        self.canvas.config(width=new_width, height=new_height)
        video_name = self.vid_reader.get_name()
        total_frames = self.vid_reader.get_frame_count()
        info_text = f"Video: {video_name} | Total Frames: {total_frames}"
        self.video_info_label["text"] = info_text
        self.update_video()

    def start_video(self):
        self.stop_video()
        self.root.after(100, self._start_video_thread)
        self.root.after(100, self.display_from_queue)

    def _start_video_thread(self):
        if not self.video_thread or not self.video_thread.is_alive():
            self.stop_signal.clear()
            self.video_thread = threading.Thread(target=self.update_video)
            self.video_thread.start()

    def stop_video(self):
        self.stop_signal.set()
        if self.video_thread and self.video_thread.is_alive():
            self.video_thread.join()

    def reset_video(self):
        new_start_frame = simpledialog.askinteger("Input", "Reset to frame:")
        if new_start_frame is not None:
            self.start_frame = new_start_frame
            self.vid_reader.cap.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)
            self.label_frame_num["text"] = f"Frame: {self.start_frame}"

    def update_video(self):
        if not self.vid_reader:
            return
        while self.vid_reader.cap.isOpened() and not self.stop_signal.is_set():
            ret, frame = self.vid_reader.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, self.new_size)
                self.queue.put(frame)
            else:
                break

    def display_from_queue(self):
        try:
            frame = self.queue.get_nowait()
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.label_frame_num[
                "text"
            ] = f"Frame: {int(self.vid_reader.get_current_frame())}"
            self.root.after(1, self.display_from_queue)
        except queue.Empty:
            self.root.after(100, self.display_from_queue)

    def process_and_save(self):
        output_video_name = simpledialog.askstring(
            "Input", "Output video name:"
        )
        base_output_dir = filedialog.askdirectory(
            title="Select Base Output Directory"
        )
        if not base_output_dir:
            messagebox.showwarning("Warning", "No directory selected!")
            return
        start_frame = simpledialog.askinteger("Input", "Start frame:")
        end_frame = simpledialog.askinteger("Input", "End frame:")
        if all(
            [
                output_video_name,
                base_output_dir,
                start_frame is not None,
                end_frame is not None,
            ]
        ):
            threading.Thread(
                target=process_video,
                args=(
                    self.vid_reader,
                    output_video_name,
                    base_output_dir,
                    start_frame,
                    end_frame,
                ),
            ).start()
            messagebox.showinfo("Info", "Processing started!")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()
