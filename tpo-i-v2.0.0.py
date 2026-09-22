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


# --- Utilidades de entrada/validacion (Cadenas + Excepciones) -----------

def pedir_entero_valido(mensaje, minimo, maximo):
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if valor < minimo or valor > maximo:
                raise ValueError("fuera de rango")
        except ValueError:
            print(f"Dato invalido. Ingrese un numero entero entre {minimo} y {maximo}.")
        else:
            return valor


def pedir_texto_valido(mensaje, min_len, max_len, transformar=None):
    while True:
        texto = input(mensaje).strip()
        if len(texto) < min_len or len(texto) > max_len:
            print(f"Dato invalido. Debe tener entre {min_len} y {max_len} caracteres.")
            continue
        if transformar == "titulo":
            texto = texto.title()
        elif transformar == "mayusculas":
            texto = texto.upper()
        elif transformar == "minusculas":
            texto = texto.lower()
        return texto


def formatear_monto(monto):
    return f"${monto:,.0f}".replace(",", ".")


# --- Calendario (Matrices auxiliares + Recursividad) ---------------------

def es_bisiesto(anio):
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)


def dias_en_mes(mes, anio):
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dias = dias_por_mes[mes - 1]
    if mes == 2 and es_bisiesto(anio):
        dias = 29
    return dias


def avanzar_un_dia(fecha):
    anio, mes, dia = fecha
    if dia < dias_en_mes(mes, anio):
        return (anio, mes, dia + 1)
    if mes < 12:
        return (anio, mes + 1, 1)
    return (anio + 1, 1, 1)


def generar_proximos_dias(fecha_inicio, cantidad):
    if cantidad <= 0:
        return []
    return [fecha_inicio] + generar_proximos_dias(avanzar_un_dia(fecha_inicio), cantidad - 1)
