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


def nombre_dia_semana(weekday_hoy, offset_desde_hoy):
    indice = (weekday_hoy + offset_desde_hoy) % 7
    return NOMBRES_DIAS_SEMANA[indice]


def generar_franjas_horarias(hora_inicio, hora_fin, paso_minutos):
    hora_i, min_i = hora_inicio.split(":")
    hora_f, min_f = hora_fin.split(":")
    minutos_inicio = int(hora_i) * 60 + int(min_i)
    minutos_fin = int(hora_f) * 60 + int(min_f)

    franjas = []
    minuto_actual = minutos_inicio
    while minuto_actual < minutos_fin:
        h = minuto_actual // 60
        m = minuto_actual % 60
        franjas.append(f"{h:02d}:{m:02d}")
        minuto_actual += paso_minutos
    return franjas


# --- Utilidad comun de ids ------------------------------------------------

def generar_siguiente_id(lista):
    if len(lista) == 0:
        return 1
    ids = [elemento["id"] for elemento in lista]
    return max(ids) + 1


# --- CRUD Areas (Diccionarios) --------------------------------------------

def crear_area(areas, nombre):
    area = {"id": generar_siguiente_id(areas), "nombre": nombre}
    areas.append(area)
    return area


def buscar_area_por_id(areas, area_id):
    for area in areas:
        if area["id"] == area_id:
            return area
    return None


def listar_areas(areas):
    print(f"\n--- AREAS ({len(areas)}) ---")
    if len(areas) == 0:
        print("No hay areas cargadas.")
    for area in areas:
        print(f"{area['id']}. {area['nombre']}")


def actualizar_area(areas, area_id, nombre_nuevo):
    area = buscar_area_por_id(areas, area_id)
    if area is None:
        return False
    area["nombre"] = nombre_nuevo
    return True


def eliminar_area(areas, medicos, area_id):
    area = buscar_area_por_id(areas, area_id)
    if area is None:
        return False, "El area no existe."
    tiene_medicos = any(medico["area_id"] == area_id for medico in medicos)
    if tiene_medicos:
        return False, "No se puede eliminar: hay medicos asignados a esta area."
    areas.remove(area)
    return True, "Area eliminada."


# --- CRUD Medicos (Diccionarios) ------------------------------------------

def crear_medico(medicos, nombre, area_id):
    medico = {"id": generar_siguiente_id(medicos), "nombre": nombre, "area_id": area_id}
    medicos.append(medico)
    return medico


def buscar_medico_por_id(medicos, medico_id):
    for medico in medicos:
        if medico["id"] == medico_id:
            return medico
    return None


def listar_medicos(medicos, areas, area_id=None):
    medicos_a_mostrar = [m for m in medicos if area_id is None or m["area_id"] == area_id]
    print(f"\n--- MEDICOS ({len(medicos_a_mostrar)}) ---")
    if len(medicos_a_mostrar) == 0:
        print("No hay medicos cargados para este filtro.")
    for medico in medicos_a_mostrar:
        area = buscar_area_por_id(areas, medico["area_id"])
        nombre_area = area["nombre"] if area is not None else "Area eliminada"
        print(f"{medico['id']}. Dr/a. {medico['nombre']} - {nombre_area}")


def actualizar_medico(medicos, medico_id, nombre_nuevo=None, area_id_nuevo=None):
    medico = buscar_medico_por_id(medicos, medico_id)
    if medico is None:
        return False
    if nombre_nuevo is not None:
        medico["nombre"] = nombre_nuevo
    if area_id_nuevo is not None:
        medico["area_id"] = area_id_nuevo
    return True


def eliminar_medico(medicos, turnos, medico_id):
    medico = buscar_medico_por_id(medicos, medico_id)
    if medico is None:
        return False, "El medico no existe."
    tiene_turnos_activos = any(
        turno["medico_id"] == medico_id and turno["estado"] == "reservado" for turno in turnos
    )
    if tiene_turnos_activos:
        return False, "No se puede eliminar: el medico tiene turnos reservados."
    medicos.remove(medico)
    return True, "Medico eliminado."


# --- Disponibilidad por medico (Matrices) ---------------------------------

def inicializar_matriz_disponibilidad(cantidad_dias, cantidad_franjas):
    return [["Libre" for _ in range(cantidad_franjas)] for _ in range(cantidad_dias)]


def obtener_matriz_medico(disponibilidad, medico_id, cantidad_dias, cantidad_franjas):
    if medico_id not in disponibilidad:
        disponibilidad[medico_id] = inicializar_matriz_disponibilidad(cantidad_dias, cantidad_franjas)
    return disponibilidad[medico_id]
