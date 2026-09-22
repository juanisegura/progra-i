"""
TPO Programacion I - Sanatorio San Roque (v2.0.0)
Sistema de Reserva de Turnos Medicos - tema 13 del listado oficial del TPO.

Tecnicas obligatorias aplicadas: Funciones, Matrices, Cadenas, Diccionarios,
Excepciones, Archivos, Recursividad.
Modulos permitidos por la catedra: time, os, colorama (no usados por ahora),
datetime (solo para la fecha actual).
"""

from datetime import date

# --- Configuracion general ---------------------------------------------

SANATORIO_NOMBRE = "Sanatorio San Roque"

NOMBRES_DIAS_SEMANA = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
NOMBRES_MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]

HORA_APERTURA = "08:00"
HORA_CIERRE = "18:00"
PASO_MINUTOS = 10
HORIZONTE_DIAS = 60

ARCHIVO_AREAS = "areas.txt"
ARCHIVO_MEDICOS = "medicos.txt"
ARCHIVO_PACIENTES = "pacientes.txt"
ARCHIVO_TURNOS = "turnos.txt"

SEPARADOR_CAMPO = "|"
