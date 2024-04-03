import logging
from multiprocessing import Process, Queue, Event
import time
import cv2


class TrackerBase:
    def __init__(self, path_video_in_main):
        self.path_video_in_main = path_video_in_main


class TrackerV0(TrackerBase):
    def __init__(self, path_video_in_main, path_video_in_aux):
        super(TrackerV0, self).__init__(path_video_in_main)
        self.path_video_in_aux = path_video_in_aux
        self.event = Event()
        self.event_stop = Event()
        self.main_skip_num = 256 + 16 * 2

    def run(self):
        process_aux = Process(target=self.__run_aux, daemon=True)
        process_aux.start()
        self.__run_main()
        process_aux.join()

    def __run_main(self):
        logging.info('__run_main start ...')
        name_win = 'main'
        cv2.namedWindow(name_win, cv2.WINDOW_NORMAL)
        cv2.moveWindow(name_win, 64, 64)
        cv2.resizeWindow(name_win, 640, 640)
        cap = cv2.VideoCapture(self.path_video_in_main)
        if not cap.isOpened():
            logging.error(f'Could not open video {self.path_video_in_main}. Exiting ...')
            exit()
        frame_id = 0
        cnt_skip = 0
        while cap.isOpened():
            if self.event_stop.is_set():
                break
            if self.event.is_set():
                time.sleep(0.001)
                continue
            self.event.set()
            if cnt_skip < self.main_skip_num:  # skip some frames for aux stream
                cnt_skip += 1
                continue
            ret, frame = cap.read()
            if not ret:
                logging.error(f"{name_win} Can't receive frame (stream end?). Exiting ...")
                break
            logging.info(f'{name_win} frame_id: {frame_id}')
            frame_id += 1
            cv2.imshow(name_win, frame)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        logging.info(f'__run_main end with {frame_id} frames ...')  # 1685

    def __run_aux(self):
        logging.info('__run_aux start ...')
        name_win = 'aux'
        cv2.namedWindow(name_win, cv2.WINDOW_NORMAL)
        cv2.moveWindow(name_win, 1024, 64)
        cv2.resizeWindow(name_win, 640, 640)
        cap = cv2.VideoCapture(self.path_video_in_aux)
        if not cap.isOpened():
            logging.error(f'Could not open video {self.path_video_in_aux}. Exiting ...')
            exit()
        frame_id = 0
        while cap.isOpened():
            self.event.wait()
            ret, frame = cap.read()
            if not ret:
                self.event_stop.set()
                logging.error(f"{name_win} Can't receive frame (stream end?). Exiting ...")
                break
            logging.info(f'{name_win} frame_id: {frame_id}')
            frame_id += 1
            cv2.imshow(name_win, frame)
            if cv2.waitKey(1) == ord('q'):
                break
            self.event.clear()
        cap.release()
        cv2.destroyAllWindows()
        logging.info(f'__run_aux end with {frame_id} frames ...')  # 1559
