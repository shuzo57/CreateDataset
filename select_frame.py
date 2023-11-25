import os
import re
import shutil

import numpy as np

np.random.seed(0)


def extract_number(filename):
    match = re.search(r"_(\d+)\.jpg$", filename)
    return int(match.group(1)) if match else 0


def select_frame(
    source_dir: str,
    save_dir: str,
    num_frames: int,
    std_dev: int,
):
    files = os.listdir(source_dir)
    sorted_files = sorted(files, key=extract_number)
    center_frame = len(sorted_files) // 2

    selected_indices = set()
    while len(selected_indices) < num_frames:
        indices = np.random.normal(
            center_frame, std_dev, num_frames - len(selected_indices)
        ).astype(int)

        valid_indices = {i for i in indices if 0 <= i < len(files)}
        selected_indices.update(valid_indices)
    print(f"selected_indices: {len(selected_indices)}")

    for index in selected_indices:
        src_path = os.path.join(source_dir, sorted_files[index])
        shutil.copy(src_path, save_dir)


def process_directory(
    base_dir: str, save_dir: str, num_frames: int, std_dev: int
):
    if os.path.isfile(base_dir):
        select_frame(os.path.dirname(base_dir), save_dir, num_frames, std_dev)
    elif os.path.isdir(base_dir):
        for item in os.listdir(base_dir):
            item_path = os.path.join(base_dir, item)
            if os.path.isdir(item_path):
                select_frame(item_path, save_dir, num_frames, std_dev)


if __name__ == "__main__":
    process_directory(
        base_dir="/home/ohwada/imgs",
        save_dir="/home/ohwada/train_imgs",
        num_frames=40,
        std_dev=30,
    )
