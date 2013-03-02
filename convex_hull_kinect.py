# coding: utf-8
import freenect
import cv2
import numpy

threshold = 100
current_depth = 0

cv2.namedWindow('Original')
cv2.namedWindow('Mapa')

def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def show_depth():
    global threshold
    global current_depth

    source, timestamp = freenect.sync_get_depth()
    depth = 255 * numpy.logical_and(
            source >= current_depth - threshold,
            source <= current_depth + threshold)


    source += 1
    source >>= 3
    depth = depth.astype(numpy.uint8)
    source = source.astype(numpy.uint8)
    cv2.imshow('Mapa', depth)

    draw_convex_hull(depth, source)



def draw_convex_hull(a, original):

    ret, b = cv2.threshold(a, 255, 255, cv2.THRESH_BINARY)

    contornos, jerarquia = cv2.findContours(a,
            cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contornos:
        hull = cv2.convexHull(cnt)
        lista = numpy.reshape(hull, (1, -1, 2))

        cv2.polylines(original, lista, True, (0, 255, 0), 3)
        center, radius = cv2.minEnclosingCircle(cnt)
        center = tuple(map(int, center))
        radius = int(radius)
        cv2.circle(original, center, radius, (255, 0, 0), 3)

    cv2.imshow('Original', original)

cv2.createTrackbar('threshold', 'Original', threshold,     500,  change_threshold)
cv2.createTrackbar('depth',     'Original', current_depth, 2048, change_depth)

while True:
    show_depth()
    if cv2.waitKey(10) == 27:
        break

