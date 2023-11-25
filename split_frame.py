import argparse
import os

import cv2


def get_video_name(video_path):
    return os.path.splitext(os.path.basename(video_path))[0]


def split_frame(video_path, save_path):
    video_name = get_video_name(video_path)
    print(f"video_name: {video_name}")
    save_dir = os.path.join(save_path, video_name)
    os.makedirs(save_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        print(f"\rframe_count: {frame_count}", end="")
        if not ret:
            break
        cv2.imwrite(
            os.path.join(save_dir, f"{video_name}_{frame_count}.jpg"), frame
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
