# coding: utf-8
import freenect
import cv2
import numpy
import sys

threshold = 100
current_depth = 0
prev = None

cv2.namedWindow('Original')
cv2.namedWindow('Mapa')
tilt = 0


def change_tilt(value):
    global tilt
    tilt = value

def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def show_depth(dev, data, timestamp):
    global threshold
    global current_depth
    global prev

    actual = data

    if prev is None:
        prev = numpy.array(actual)

    source = (actual + prev) / 2

    prev = actual

    depth = 255 * numpy.logical_and(
            source >= current_depth - threshold,
            source <= current_depth + threshold)


    source += 1
    source >>= 3
    depth = depth.astype(numpy.uint8)
    source = source.astype(numpy.uint8)
    cv2.imshow('Mapa', depth)

    draw_convex_hull(depth, source)

    if cv2.waitKey(10) == 27:
        sys.exit()

def obtener_mayores_contornos(contornos, cantidad=4):
    """Devuelve los indices de los mayores contornos"""
    container = []
    for i, cnt in enumerate(contornos):
        center, radius = cv2.minEnclosingCircle(cnt)
        container.append((i, center, radius))

    container.sort(lambda a, b: cmp(b[2], a[2]))
    return container[0:cantidad]


def draw_convex_hull(a, original):

    original = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)

    ret, b = cv2.threshold(a, 255, 255, cv2.THRESH_BINARY)

    contornos, jerarquia = cv2.findContours(a,
            cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

    mayores = obtener_mayores_contornos(contornos)

    for n, center, radius in mayores:

        cnt = contornos[n]
        if radius < 30:
            continue

        hull = cv2.convexHull(cnt)
        foo = cv2.convexHull(cnt, returnPoints=False)
        cv2.drawContours(original, contornos, n, (0, 35, 245))
        if len(cnt) > 3 and len(foo) > 2:
            defectos = cv2.convexityDefects(cnt, foo)
            if defectos is not None:
                defectos = defectos.reshape(-1, 4)
                puntos = cnt.reshape(-1, 2)
                for d in defectos:
                    if d[3] > 20:
                        cv2.circle(original, tuple(puntos[d[0]]), 5, (255, 255, 0), 2)
                        cv2.circle(original, tuple(puntos[d[1]]), 5, (255, 255, 0), 2)
                        cv2.circle(original, tuple(puntos[d[2]]), 5, (0, 0, 255), 2)

        lista = numpy.reshape(hull, (1, -1, 2))
        cv2.polylines(original, lista, True, (0, 255, 0), 3)

        box = cv2.fitEllipse(cnt)
        cv2.ellipse(original, box, (255,255,0))

        center = tuple(map(int, center))
        radius = int(radius)
        cv2.circle(original, center, radius, (255, 0, 0), 3)
        # Valores a devolver:
        # cantidad de defectos de convexion
        # Coordenadas del centro del circulo
        # inclinacion de la elipse
        # radio del centro del circulo

        #data = ()


    cv2.imshow('Original', original)

cv2.createTrackbar('threshold', 'Original', threshold,     500,  change_threshold)
cv2.createTrackbar('depth', 'Original', current_depth, 2048, change_depth)
cv2.createTrackbar('tilt', 'Original', 0, 30, change_tilt)

def main(dev, ctx):
    freenect.set_tilt_degs(dev, tilt)

freenect.runloop(depth=show_depth, body=main)
