import argparse
import logging

from utils.functions import set_logging


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_video_main',
                        default='/media/manu/data/videos/vlc-record-2024-03-19-11h48m04s-rtsp___192.168.1.64_h264_ch1_main_av_stream-.avi')
    return parser.parse_args()


def run(args):
    logging.info(args)


def main():
    set_logging()
    args = parse_args()
    run(args)


if __name__ == '__main__':
    main()
