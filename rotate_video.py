import argparse
import os

import cv2


def get_basename(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]


def process_video(
    input_path,
    output_dir,
    rotate_direction,
):
    print(f"Rotate direction: {rotate_direction}")
    video_name = get_basename(input_path)

    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{video_name}.mp4")

    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    if rotate_direction == "right":
        video = cv2.VideoWriter(output_path, fourcc, fps, (height, width))
    elif rotate_direction == "left":
        video = cv2.VideoWriter(output_path, fourcc, fps, (height, width))
    else:
        video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not video.isOpened():
        print("Cannot be opened")

    while True:
        ret, frame = cap.read()
        if ret:
            if rotate_direction == "right":
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif rotate_direction == "left":
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            video.write(frame)
        else:
            break

    video.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video processing script")
    parser.add_argument(
        "-i", "--input", type=str, help="Input video path", required=True
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output directory", required=True
    )
    parser.add_argument(
        "-r",
        "--rotate",
        type=str,
        choices=["right", "left", "none"],
        default="none",
        help="Rotation direction: 'right' for clockwise, 'left' for "
        + "counterclockwise, 'none' for no rotation (default)",
    )

    args = parser.parse_args()

    input_path = args.input
    output_dir = args.output
    rotate_direction = args.rotate

    process_video(input_path, output_dir, rotate_direction)
