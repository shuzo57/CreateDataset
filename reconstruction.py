import argparse
import os

import cv2

from config import SAVE_VIDEO_EXTENSION
from utils import VideoReader


def reconstruct_video_with_frame_number(
    video_reader: VideoReader,
    output_dir: str,
):
    cap = video_reader.cap
    fps = video_reader.get_fps()
    width, height = video_reader.get_size()
    total_frames = video_reader.get_frame_count()

    output_dir = os.path.join(output_dir, video_reader.get_name())
    os.makedirs(output_dir, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_path = os.path.join(
        output_dir, video_reader.get_name() + SAVE_VIDEO_EXTENSION
    )
    out = cv2.VideoWriter(output_path, fourcc, fps, (int(width), int(height)))

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            print(f"\r[{frame_index:6d} | {total_frames:6d}]", end="")
            frame = cv2.putText(
                frame,
                str(frame_index),
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
                thickness=2,
            )
            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Video frame extraction script"
    )
    parser.add_argument(
        "-i", "--input", type=str, help="Input video path", required=True
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output directory", required=True
    )

    args = parser.parse_args()

    video_reader = VideoReader(args.input)
    reconstruct_video_with_frame_number(video_reader, args.output)
