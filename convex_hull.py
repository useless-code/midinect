# coding: utf-8
import cv2
import numpy

from utils import calcular_centroide, dibujar_marcador

cv2.namedWindow('Original')
cv2.namedWindow('Test')

a = cv2.imread('cloud.png')

gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)

print gray.shape
print gray
ret, b = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

cv2.imshow('Test', b)

contornos, jerarquia = cv2.findContours(b,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

for cnt in contornos:
    hull = cv2.convexHull(cnt)
    lista = numpy.reshape(hull, (1, -1, 2))

    centro = calcular_centroide(hull)

    dibujar_marcador(a, centro, (255, 255, 0))

    centro = calcular_centroide(cnt)
    dibujar_marcador(a, centro, (20, 40, 255))

    cv2.polylines(a, lista, True, (0, 255, 0), 3)
    center, radius = cv2.minEnclosingCircle(cnt)
    center = tuple(map(int, center))
    radius = int(radius)
    cv2.circle(a, center, radius, (255, 0, 0), 3)
    cv2.circle(a, center, 5, (255, 0, 0), 3)

cv2.imshow('Original', a)

while True:
    if cv2.waitKey(1) == 27:
        break

