import argparse
import logging

from cores.mcmt_tracker import TrackerV0
from utils.functions import set_logging


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_video_main', default='/media/manu/data/videos/mcmt_main_fps25.mp4')
    parser.add_argument('--path_video_aux', default='/media/manu/data/videos/mcmt_aux_fps25.avi')
    return parser.parse_args()


def run(args):
    logging.info(args)
    mcmt_tracker_obj = TrackerV0(args.path_video_main, args.path_video_aux)
    mcmt_tracker_obj.run()


def main():
    set_logging()
    args = parse_args()
    run(args)


if __name__ == '__main__':
    main()
