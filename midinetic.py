# coding: utf-8
import cv2
import math
import uuid
from event  import Event

prev_blob_state = {}

def obtener_mayores_contornos(contornos, cantidad=4):
    """Devuelve los indices de los mayores contornos"""
    container = []
    for i, cnt in enumerate(contornos):
        center, radius = cv2.minEnclosingCircle(cnt)
        container.append((i, center, radius))

    container.sort(lambda a, b: cmp(b[2], a[2]))
    return container[0:cantidad]

def etiquetar_eventos( original, puntos):
    global prev_blob_state
    etiquetas = {}
    for a in puntos:
        if prev_blob_state:
            distancias = map(lambda n: (n[0], calcular_distancia(a.center, n[1].center)),
                            prev_blob_state.iteritems())
            id_unico, d_minima = min(distancias, key=lambda n: n[1])

            if (d_minima < 40):
                a.tipo = 'keep'
                a.id = id_unico
                etiquetas[id_unico] = a
                cv2.putText(original, id_unico, a.center, cv2.FONT_HERSHEY_COMPLEX, 1.1, (255, 0, 0))
            else:
                a = nuevo_evento(a);
                etiquetas[a.id] = a
        else:
            a = nuevo_evento(a);
            etiquetas[a.id] = a

    for key, value in prev_blob_state.iteritems():
        if value.tipo != 'off' and key not in etiquetas:
            value.tipo = 'off'
            etiquetas[value.id] = value

    prev_blob_state = etiquetas
    return etiquetas

def nuevo_evento(evento):

    id = str(uuid.uuid4())
    evento.id = id
    evento.tipo = 'on'

    return evento



def calcular_distancia(a, b):
    return math.sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))

def draw_convex_hull(a, original):

    original = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)

    ret, b = cv2.threshold(a, 255, 255, cv2.THRESH_BINARY)

    contornos, jerarquia = cv2.findContours(a,
            cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

    mayores = obtener_mayores_contornos(contornos, 2)
    puntos = [];
    for n, center, radius in mayores:

        cnt = contornos[n]
        if radius < 30:
            continue

        #hull = cv2.convexHull(cnt)
        #foo = cv2.convexHull(cnt, returnPoints=False)
        #cv2.drawContours(original, contornos, n, (0, 35, 245))
        #if len(cnt) > 3 and len(foo) > 2:
        #    defectos = cv2.convexityDefects(cnt, foo)
        #    if defectos is not None:
        #        defectos = defectos.reshape(-1, 4)
        #        puntos = cnt.reshape(-1, 2)
        #        for d in defectos:
        #            if d[3] > 20:
        #                cv2.circle(original, tuple(puntos[d[0]]), 5, (255, 255, 0), 2)
        #                cv2.circle(original, tuple(puntos[d[1]]), 5, (255, 255, 0), 2)
        #                cv2.circle(original, tuple(puntos[d[2]]), 5, (0, 0, 255), 2)

        #lista = numpy.reshape(hull, (1, -1, 2))
        #cv2.polylines(original, lista, True, (0, 255, 0), 3)


        box = cv2.fitEllipse(cnt)
        cv2.ellipse(original, box, (255,255,0), 4)

        center = tuple(map(int, center))
        radius = int(radius)
        cv2.circle(original, center, radius, (255, 0, 0), 3)
        # Valores a devolver:
        # cantidad de defectos de convexion
        # Coordenadas del centro del circulo
        # inclinacion de la elipse
        # radio del centro del circulo
        puntos.append(Event(center, radius, box[2]))

    eventos = etiquetar_eventos(original, puntos)
    cv2.imshow('Original', original)
    return eventos

