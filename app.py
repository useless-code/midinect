#! -*- coding: utf8 -*-
from base_app import FreenectCv2App
import cv2
import numpy
import midinetic
import freenect
import math
import simplecoremidi

class Midinetic(FreenectCv2App):
    """Midinetic app"""
    def __init__(self):
        super(Midinetic, self).__init__()
        self.threshold = 100
        self.depth = 0
        self.prev_blob_state = []
        self.tilt = 0
        self.prev = None
        self.crear_interface()
        self.midi = simplecoremidi.MIDISource('midinetic')
        self.current_notes = {}
        self.particiones = (6, 4)
        self.resolucion = (640, 480)

    def crear_interface(self):
        cv2.namedWindow('Original')
        cv2.namedWindow('Mapa')
        cv2.createTrackbar('threshold', 'Original',
                self.threshold,     500,  self.change_threshold)
        cv2.createTrackbar('depth', 'Original',
                self.depth, 2048, self.change_depth)
        cv2.createTrackbar('tilt', 'Original',
                0, 30, self.change_tilt)

    def change_tilt(self, value):
        self.tilt = value

    def change_threshold(self, value):
        self.threshold = value

    def change_depth(self, value):
        self.depth = value

    def display_depth(self, dev, data, timestamp):

        source = data

        depth = 255 * numpy.logical_and(
                source >= self.depth - self.threshold,
                source <= self.depth + self.threshold)

        depth = numpy.fliplr(depth)
        source = numpy.fliplr(source)
        source += 1
        source >>= 3
        depth = depth.astype(numpy.uint8)
        source = source.astype(numpy.uint8)
        cv2.imshow('Mapa', depth)
        source = cv2.cvtColor(source, cv2.COLOR_GRAY2BGR)

        self.draw_grid(source)

        eventos = midinetic.draw_convex_hull(depth, source)

        cv2.imshow('Original', source)

        self.handle_events(eventos)
        super(Midinetic, self).display_depth(dev, data, timestamp)

    def main(self, dev, ctx):
        super(Midinetic, self).main(dev, ctx)
        freenect.set_tilt_degs(dev, self.tilt)

    def handle_events(self, events):
        for event in events.values():
            if event.tipo == 'on':
                #note on
                n = self.get_note_from_position(event.center)
                nota = n + 60
                self.current_notes[event.id] = nota
                self.midi.send((0x90, nota, 127))
            elif event.tipo == 'off':
                nota = self.current_notes[event.id]
                self.midi.send((0x90, nota, 0))
                print "apagar nota"
                #note off

    def draw_grid(self, canvas):
        w, h = self.resolucion
        x_partitions, y_partitions = self.particiones
        delta_w, delta_h = int(w / x_partitions), int(h / y_partitions)
        color = (0x4f, 0x96, 0x11)
        for n in xrange(0, x_partitions):
            x = delta_w * n
            cv2.line(canvas,(x, 0), (x, h), color, 4)
        for n in xrange(0, y_partitions):
            y = delta_h * n
            cv2.line(canvas,(0, y), (w, y), color, 4)
       #lineas verticales
       #lineas horizontales

    def get_note_from_position(self, position_tuple):

        w, h = self.resolucion
        x_partitions, y_partitions = self.particiones
        delta_w, delta_h = w / x_partitions, h / y_partitions

        n = y_partitions * math.floor(position_tuple[1] / delta_h) + math.floor(position_tuple[0] /delta_w)
        return int(n)


if __name__ == '__main__':
    app = Midinetic()
    app.run()
