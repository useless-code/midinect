#! -*- coding:utf8 -*-

import freenect
import cv2

class FreenectCv2App(object):
    """Clase base para extender una aplicacion freenect"""
    def __init__(self, depth, body):
        self.keep_running = True

    def run(self):
        """Starts execution"""
        freenect.runloop(
                depth=self.display_depth,
                video=self.display_rgb,
                body=self.main
                )

    def main(self):
        if not self.keep_running:
            raise freenect.Kill

    def display_depth(self, dev, data, timestamp):
        """Works over a frame of depth map"""
        self._wait_for_exit()

    def display_rgb(self, dev, data, timestamp):
        """Works over a video frame"""
        self._wait_for_exit()

    def _wait_for_exit(self):
        """Wait for ESC keypress to exit app"""
        if cv2.waitKey(10) == 27:
            self.keep_running = False






