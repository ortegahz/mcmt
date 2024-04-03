from multiprocessing import Process, Queue, Event

import cv2


class Decoder:
    def __init__(self, video_paths):
        self.video_paths = video_paths
        self.event_stop = Event()
        self.queues = list()

    def decode_video(self, video_path, queue):
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or self.event_stop.is_set():
                break
            queue.put(frame)
        cap.release()
        self.event_stop.set()

    def run(self):
        for video_path in self.video_paths:
            queue = Queue(maxsize=1)
            p = Process(target=self.decode_video, args=(video_path, queue), daemon=True)
            p.start()
            self.queues.append(queue)

    def get_items(self):
        items = [queue.get() for queue in self.queues] if not self.event_stop.is_set() else None
        return items
