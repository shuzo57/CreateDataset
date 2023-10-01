import argparse

from config import EXTRA_TIME
from utils import VideoReader, process_video


def extract_frames(
    input_path: str,
    output_dir: str,
    video_name: str,
    start_time: float,
    end_time: float = None,
    rotate_direction: str = "none",
    fps: float = None,
):
    video_reader = VideoReader(input_path)
    if fps is None:
        fps = video_reader.get_fps()
    print(f"FPS: {fps}")
    total_frames = video_reader.get_frame_count()
    print(f"Total frames: {total_frames}")

    if end_time is None:
        end_time = total_frames / fps

    start_frame = int((start_time - EXTRA_TIME) * fps)
    end_frame = int((end_time + EXTRA_TIME) * fps)

    print(f"Start frame: {start_frame}")
    print(f"End frame: {end_frame}")

    process_video(
        video_reader,
        video_name,
        output_dir,
        start_frame,
        end_frame,
        rotate_direction,
    )


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
        "-s", "--start", type=float, default=0, help="Start time"
    )
    parser.add_argument(
        "-e", "--end", type=float, default=None, help="End time"
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
    parser.add_argument(
        "-f",
        "--fps",
        type=float,
        default=None,
        help="FPS of output video",
    )

    args = parser.parse_args()

    input_path = args.input
    output_dir = args.output
    video_name = args.name
    start_time = args.start
    end_time = args.end
    rotate_direction = args.rotate
    fps = args.fps

    extract_frames(
        input_path,
        output_dir,
        video_name,
        start_time,
        end_time,
        rotate_direction,
        fps,
    )
