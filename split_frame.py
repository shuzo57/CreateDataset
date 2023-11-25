import argparse
import os

import cv2

video_exts = [".mp4", ".MP4", ".avi", ".mov", ".mkv"]


def get_video_name(video_path):
    return os.path.splitext(os.path.basename(video_path))[0]


def get_dir_name(path):
    return os.path.basename(
        os.path.dirname(os.path.dirname(os.path.dirname(path)))
    )


def split_frame(video_path, save_path):
    if os.path.isdir(video_path):
        video_paths = []
        for ext in video_exts:
            video_paths += [
                os.path.join(video_path, file)
                for file in os.listdir(video_path)
                if file.endswith(ext)
            ]
    else:
        video_paths = [video_path]

    for video_path in video_paths:
        video_name = get_video_name(video_path)
        dir_name = get_dir_name(video_path)
        print(f"video_name: {dir_name}_{video_name}")
        save_dir = os.path.join(save_path, f"{dir_name}_{video_name}")
        os.makedirs(save_dir, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        while True:
            ret, frame = cap.read()
            print(f"\rframe_count: {frame_count}", end="")
            if not ret:
                break
            cv2.imwrite(
                os.path.join(
                    save_dir, f"{dir_name}_{video_name}_{frame_count}.jpg"
                ),
                frame,
            )
            frame_count += 1

        cap.release()
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video_path", type=str, required=True)
    args = parser.parse_args()
    video_path = args.video_path
    save_path = "/home/ohwada/imgs"
    split_frame(video_path, save_path)
