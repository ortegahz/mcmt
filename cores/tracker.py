import pickle
import sys

sys.path.append('/home/manu/nfs/ByteTrack')
from yolox.tracker.byte_tracker import BYTETracker

sys.path.append('/home/manu/nfs/YOLOv6')
from yolov6.core.inferer import Inferer


class MCMTTracker:
    def __init__(self, frame_rate=25, num_videos=1):
        with open('/home/manu/tmp/args_tracker.pickle', 'rb') as f:
            args_tracker = pickle.load(f)
        self.mot_tracker = BYTETracker(args_tracker, frame_rate=frame_rate)
        self.detector = \
            Inferer(
                '/media/manu/data/videos/vlc-record-2024-04-02-10h31m02s-rtsp___192.168.1.108_554_cam_realmonitor-.mp4',
                False, 0, '/home/manu/tmp/n6_ft_b64_nab_s640_dv2r_ncml_nsilu_ncont/weights/best_ckpt.pt',
                0, '/home/manu/nfs/YOLOv6/data/head.yaml', [640, 640], False)
        self.items = dict()

    def update(self, items):
        for i, item in enumerate(items):
            frame = item
            dets = self.detector.infer_custom(frame, 0.4, 0.45, None, False, 1000)
            dets = dets[:, 0:5].detach().cpu().numpy()
            online_targets = \
                self.mot_tracker.update(dets, [frame.shape[0], frame.shape[1]], [frame.shape[0], frame.shape[1]])
            self.items[i] = [frame, online_targets]
