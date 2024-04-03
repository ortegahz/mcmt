import argparse
import logging

from cores.decoder import Decoder
from cores.tracker import MCMTTracker
from cores.displayer import Displayer
from utils.functions import set_logging


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--paths_video', nargs='+',
                        default=['/media/manu/data/videos/wyl.mp4',
                                 '/media/manu/data/videos/wyl.mp4'])
    parser.add_argument('--frame_rate', default=25)
    return parser.parse_args()


def run(args):
    logging.info(args)
    decoder = Decoder(args.paths_video)
    tracker = MCMTTracker(num_videos=len(args.paths_video))
    displayer = Displayer(num_process=len(args.paths_video))
    decoder.run()
    displayer.run()
    while True:
        items_decoder = decoder.get_items()
        if items_decoder is None or displayer.event_stop.is_set():
            break
        tracker.update(items_decoder)
        for key in tracker.items.keys():
            displayer.queues_dict[key].put(tracker.items[key])


def main():
    set_logging()
    args = parse_args()
    run(args)


if __name__ == '__main__':
    main()
