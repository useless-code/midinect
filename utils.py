#! -*- coding: utf8 -*-

import cv2

def calcular_centroide(trazado):
    momentos = cv2.moments(trazado)
    x = momentos['m10'] / momentos['m00']
    y = momentos['m01'] / momentos['m00']
    return (int(x), int(y))

def dibujar_marcador(imagen, centro, color):
    cv2.circle(imagen, centro, 5, color, 4)
    cv2.circle(imagen, centro, 10, color, 4)
    cv2.circle(imagen, centro, 20, color, 4)

