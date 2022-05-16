#!/usr/bin/python3
# -*- coding: utf-8 -*-

class empleado:
    def __init__(self, dni, apellidos, nombre, centro=''):
        self.nombre = nombre
        self.apellidos = apellidos
        self.dni = dni
        self.centro = centro
        self.registro = []
        self.fichado = False

    def info_by_dni(self):
        return {
            'nombre': self.nombre,
            'apellidos': self. apellidos,
            'centro': self.centro
        }

    def add_registro(self, reg):
        if 'tipo' in reg:
            self.fichado = True if reg['tipo'] == 'entrada' else False
        else:
            reg['tipo'] = 'entrada' if not self.fichado else 'salida'
            self.fichado = not self.fichado
        
        self.registro.append(reg)
        return self.fichado


class empresa:
    def __init__(self, cif, nombre):
        self.cif = cif
        self.nombre = nombre
        self.centros = []
        self.empleados = []

    def add_centro(self, centro):
        self.centros.append(centro)

    def add_empleado(self, empleado):
        self.empleados.append(empleado)

    def empl_by_dni(self):
        listado = {}
        for empl in self.empleados:
            listado[empl.dni] = empl.info_by_dni()
        return listado

    def find_by_dni(self, dni):
        for empl in self.empleados:
            if empl.dni == dni:
                return empl
        return None


