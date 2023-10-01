import os
import shutil

import cv2

from config import (
    IMG_DIR,
    SAVE_IMG_EXTENSION,
    SAVE_VIDEO_EXTENSION,
    VIDEO_DIR,
    VIDEO_EXTENTIONS,
)


class VideoReader:
    def __init__(self, path):
        self.path = path
        self.read_video(self.path)

    def read_video(self, path):
        if os.path.isfile(path):
            if any(path.endswith(ext) for ext in VIDEO_EXTENTIONS):
                self.cap = cv2.VideoCapture(path)
            else:
                raise ValueError("File extension is not supported")
        else:
            raise ValueError("File does not exist")

    def get_size(self):
        return (
            self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
            self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
        )

    def get_fps(self):
        return self.cap.get(cv2.CAP_PROP_FPS)

    def get_frame_count(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_current_frame(self):
        return self.cap.get(cv2.CAP_PROP_POS_FRAMES)

    def get_name(self):
        return os.path.splitext(os.path.basename(self.path))[0]


def get_basename(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]


def split_video(
    input_path, output_dir, rotate_direction: str = "None"
) -> None:
    video_reader = VideoReader(input_path)

    cap = video_reader.cap
    video_name = video_reader.get_name()

    output_dir = os.path.join(output_dir, video_name)
    os.makedirs(output_dir, exist_ok=True)

    while True:
        ret, frame = cap.read()
        if ret:
            frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            if rotate_direction == "left":
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif rotate_direction == "right":
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            frame_name = f"{video_name}_{frame_index}{SAVE_IMG_EXTENSION}"
            output_path = os.path.join(output_dir, frame_name)
            cv2.imwrite(output_path, frame)
        else:
            break

    cap.release()
    return None


def process_video(
    video_reader: VideoReader,
    output_video_name: str,
    base_output_dir: str,
    start_frame: int,
    end_frame: int,
    rotate_direction: str = "none",
) -> None:
    cap = video_reader.cap
    fps = video_reader.get_fps()
    width, height = video_reader.get_size()

    video_dir = os.path.join(base_output_dir, VIDEO_DIR)
    img_dir = os.path.join(base_output_dir, IMG_DIR)
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_output_path = os.path.join(
        video_dir, output_video_name + SAVE_VIDEO_EXTENSION
    )
    out = cv2.VideoWriter(
        video_output_path, fourcc, fps, (int(width), int(height))
    )

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

            if rotate_direction == "right":
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif rotate_direction == "left":
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            out.write(frame)
            frame_name = (
                f"{output_video_name}_{frame_index}{SAVE_IMG_EXTENSION}"
            )
            image_output_path = os.path.join(img_dir, frame_name)
            cv2.imwrite(image_output_path, frame)
            if frame_index == end_frame:
                break
        else:
            break

    cap.release()
    out.release()


def reconstruct_video(
    video_reader: VideoReader,
    output_video_name,
    start_frame: int,
    end_frame: int,
) -> None:
    cap = video_reader.cap
    fps = video_reader.get_fps()
    width, height = video_reader.get_size()

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_path = output_video_name + SAVE_VIDEO_EXTENSION
    out = cv2.VideoWriter(output_path, fourcc, fps, (int(width), int(height)))

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == end_frame:
                break
        else:
            break

    cap.release()
    out.release()
    return None


def save_frames_as_images(
    video_reader: VideoReader,
    output_dir: str,
    start_frame: int,
    end_frame: int,
) -> None:
    video_name = video_reader.get_name()
    os.makedirs(output_dir, exist_ok=True)

    cap = video_reader.cap

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_index > end_frame:
                break

            frame_name = f"{video_name}_{frame_index}{SAVE_IMG_EXTENSION}"
            output_path = os.path.join(output_dir, frame_name)
            cv2.imwrite(output_path, frame)
        else:
            break

    cap.release()


def delete_img_dir(img_dir) -> None:
    shutil.rmtree(img_dir)
