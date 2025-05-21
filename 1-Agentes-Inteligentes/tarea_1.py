#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import entornos_f
from random import choice

# Import the random‐action agent from doscuartos_o
from doscuartos_o import AgenteAleatorio

class NueveCuartos(entornos_f.Entorno):
    """
    Entorno de tres pisos con tres cuartos cada uno.
    Cuartos: P1A, P1B, P1C, P2A, P2B, P2C, P3A, P3B, P3C
    Acciones: ['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']
    """
    def __init__(self):
        self.habitaciones = [(p, c) for p in ("P1", "P2", "P3") for c in ("A", "B", "C")]
        self.acciones = ['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']

    def accion_legal(self, estado, accion):
        piso, cuarto = estado[0]
        if accion == "subir":
            return piso in ("P1", "P2") and cuarto == "C"
        if accion == "bajar":
            return piso in ("P2", "P3") and cuarto == "A"
        if accion == "ir_Derecha":
            return cuarto in ("A", "B")
        if accion == "ir_Izquierda":
            return cuarto in ("B", "C")
        if accion in ("limpiar", "nada"):
            return True
        return False

    def transicion(self, estado, accion):
        ubicacion = estado[0]
        limpieza = list(estado[1:])
        piso, cuarto = ubicacion
        idx = self.habitaciones.index(ubicacion)
        costo = 1

        if accion == "nada" and all(x == "limpio" for x in limpieza):
            costo = 0
        elif accion == "limpiar":
            limpieza[idx] = "limpio"
            costo = 0.5
        elif accion == "ir_Derecha" and cuarto in ("A", "B"):
            ubicacion = (piso, chr(ord(cuarto) + 1))
        elif accion == "ir_Izquierda" and cuarto in ("B", "C"):
            ubicacion = (piso, chr(ord(cuarto) - 1))
        elif accion == "subir" and piso in ("P1", "P2") and cuarto == "C":
            ubicacion = (f"P{int(piso[1]) + 1}", cuarto)
            costo = 2
        elif accion == "bajar" and piso in ("P2", "P3") and cuarto == "A":
            ubicacion = (f"P{int(piso[1]) - 1}", cuarto)
            costo = 2

        return ((ubicacion, *limpieza), costo)

    def percepcion(self, estado):
        piso, cuarto = estado[0]
        idx = self.habitaciones.index((piso, cuarto))
        return (estado[0], estado[idx + 1])


class AgenteReactivoModeloNueveCuartos(entornos_f.Agente):
    def __init__(self):
        self.modelo = [("P1", "A")] + ["sucio"] * 9
        self.habitaciones = [(p, c) for p in ("P1", "P2", "P3") for c in ("A", "B", "C")]

    def programa(self, percepcion):
        ubicacion, estado = percepcion
        self.modelo[0] = ubicacion
        idx = self.habitaciones.index(ubicacion)
        self.modelo[idx + 1] = estado

        if all(x == "limpio" for x in self.modelo[1:]):
            return "nada"
        if estado == "sucio":
            return "limpiar"

        # busca la siguiente habitación sucia en el modelo
        for i, room in enumerate(self.habitaciones):
            if self.modelo[i + 1] == "sucio":
                target = room
                break

        piso, cuarto = ubicacion
        piso_t, cuarto_t = target

        if piso == piso_t:
            return "ir_Derecha" if cuarto < cuarto_t else "ir_Izquierda"
        else:
            if int(piso[1]) < int(piso_t[1]) and cuarto == "C":
                return "subir"
            if int(piso[1]) > int(piso_t[1]) and cuarto == "A":
                return "bajar"
            return "ir_Derecha" if int(piso[1]) < int(piso_t[1]) else "ir_Izquierda"


class NueveCuartosCiego(NueveCuartos):
    def percepcion(self, estado):
        # Solo sabe en qué cuarto está
        return estado[0]


class AgenteRacionalCiegoNueveCuartos(entornos_f.Agente):
    def __init__(self):
        self.modelo = [("P1", "A")] + ["desconocido"] * 9
        self.habitaciones = [(p, c) for p in ("P1", "P2", "P3") for c in ("A", "B", "C")]

    def programa(self, percepcion):
        ubicacion = percepcion
        self.modelo[0] = ubicacion
        idx = self.habitaciones.index(ubicacion)

        if self.modelo[idx + 1] != "limpio":
            self.modelo[idx + 1] = "limpio"
            return "limpiar"

        # encontrar siguiente no limpio
        for i, est in enumerate(self.modelo[1:], start=1):
            if est != "limpio":
                destino = self.habitaciones[i - 1]
                break
        else:
            return "nada"

        piso, cu = ubicacion
        piso_d, cu_d = destino
        if piso == piso_d:
            return "ir_Derecha" if cu < cu_d else "ir_Izquierda"
        if int(piso[1]) < int(piso_d[1]) and cu == "C":
            return "subir"
        if int(piso[1]) > int(piso_d[1]) and cu == "A":
            return "bajar"
        return "ir_Derecha" if int(piso[1]) < int(piso_d[1]) else "ir_Izquierda"


class NueveCuartosEstocastico(NueveCuartos):
    def transicion(self, estado, accion):
        ubicacion, *limpieza = estado
        idx = self.habitaciones.index(ubicacion)

        if accion == "limpiar":
            if random.random() < 0.8:
                limpieza[idx] = "limpio"
            return ((ubicacion, *limpieza), 0.5)

        if accion in ("ir_Derecha", "ir_Izquierda", "subir", "bajar"):
            r = random.random()
            if r < 0.8:
                return super().transicion((ubicacion, *limpieza), accion)
            if r < 0.9:
                return ((ubicacion, *limpieza), 1)
            azar = choice([a for a in self.acciones
                           if self.accion_legal((ubicacion, *limpieza), a)])
            return super().transicion((ubicacion, *limpieza), azar)

        return super().transicion((ubicacion, *limpieza), accion)
    
class AgenteAleatorioCiegoLegal(entornos_f.Agente):
    def __init__(self):
        # Podríamos repetir la lista, pero en programa calcularemos legalidad
        self.acciones = ['ir_Derecha','ir_Izquierda','subir','bajar','limpiar','nada']

    def programa(self, percepcion):
        # percepcion es solo la ubicación: ('P1','A'), etc.
        piso, cuarto = percepcion
        legales = []
        # horizontales
        if cuarto in ('A','B'): legales.append('ir_Derecha')
        if cuarto in ('B','C'): legales.append('ir_Izquierda')
        # verticales
        if piso in ('P1','P2') and cuarto == 'C': legales.append('subir')
        if piso in ('P2','P3') and cuarto == 'A': legales.append('bajar')
        # limpiar y nada siempre son legales
        legales.extend(['limpiar','nada'])
        return choice(legales)



# ————— funciones de prueba —————

def prueba_nueve_cuartos_agente(agente, pasos=200):
    estado0 = (("P1", "A"),) + tuple("sucio" for _ in range(9))
    entornos_f.imprime_simulacion(
        entornos_f.simulador(NueveCuartos(), agente, estado0, pasos),
        estado0
    )

def prueba_nueve_cuartos_ciego(pasos=200):
    estado0 = (("P1", "A"),) + tuple("sucio" for _ in range(9))
    print("\n=== Agente Racional Ciego")
    entornos_f.imprime_simulacion(
        entornos_f.simulador(
            NueveCuartosCiego(),
            AgenteRacionalCiegoNueveCuartos(),
            estado0, pasos),
        estado0
    )

    print("\n=== Agente Aleatorio Ciego")
    entornos_f.imprime_simulacion(
        entornos_f.simulador(
            NueveCuartosCiego(),
            AgenteAleatorioCiegoLegal(),
            estado0, pasos),
        estado0
    )

if __name__ == "__main__":
    print("== Prueba: Agente Reactivo Basado en Modelo ==")
    prueba_nueve_cuartos_agente(AgenteReactivoModeloNueveCuartos())
    prueba_nueve_cuartos_ciego()

