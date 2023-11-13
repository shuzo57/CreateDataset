import argparse
import os

import cv2

EXTRA_TIME = 1.0
SAVE_VIDEO_EXTENSION = ".mp4"


def split_video(
    input_path: str,
    output_dir: str,
    video_name: str,
    start_frame: int,
    end_frame: int,
):
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    start_frame = start_frame - int(fps * EXTRA_TIME)
    end_frame = end_frame + int(fps * EXTRA_TIME)

    output_dir = os.path.join(output_dir, video_name)
    os.makedirs(output_dir, exist_ok=True)

    save_path = os.path.join(output_dir, video_name + SAVE_VIDEO_EXTENSION)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(save_path, fourcc, fps, (int(width), int(height)))

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_index > end_frame:
                break
            if start_frame <= frame_index <= end_frame:
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
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Output video name",
        required=True,
    )
    parser.add_argument(
        "-s", "--start", type=int, default=0, help="Start frame"
    )
    parser.add_argument("-e", "--end", type=int, default=0, help="End frame")

    args = parser.parse_args()

    split_video(
        args.input,
        args.output,
        args.name,
        args.start,
        args.end,
    )
