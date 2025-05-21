# dos_botes.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import busquedas

class ModeloDosBotes(busquedas.ModeloBusqueda):
    def __init__(self, cap1, cap2):
        self.cap1 = cap1
        self.cap2 = cap2

    def acciones_legales(self, estado):
        x, y = estado
        acciones = []
        if x < self.cap1: acciones.append('llenar1')
        if y < self.cap2: acciones.append('llenar2')
        if x > 0:         acciones.append('vaciar1')
        if y > 0:         acciones.append('vaciar2')
        if x > 0 and y < self.cap2: acciones.append('verter1_en_2')
        if y > 0 and x < self.cap1: acciones.append('verter2_en_1')
        return acciones

    def sucesor(self, estado, accion):
        x, y = estado
        if accion == 'llenar1':      return (self.cap1, y)
        if accion == 'llenar2':      return (x, self.cap2)
        if accion == 'vaciar1':      return (0, y)
        if accion == 'vaciar2':      return (x, 0)
        if accion == 'verter1_en_2':
            espacio = self.cap2 - y
            t = min(x, espacio)
            return (x - t, y + t)
        if accion == 'verter2_en_1':
            espacio = self.cap1 - x
            t = min(y, espacio)
            return (x + t, y - t)
        return estado

    def costo_local(self, estado, accion):
        return 1

    @staticmethod
    def bonito(estado):
        return f"Jug1={estado[0]}, Jug2={estado[1]}"

class PblDosBotes(busquedas.ProblemaBusqueda):
    def __init__(self, cap1, cap2, objetivo):
        modelo = ModeloDosBotes(cap1, cap2)
        super().__init__((0,0),
                         lambda s: s[0] == objetivo or s[1] == objetivo,
                         modelo)
