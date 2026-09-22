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

def crear_area(areas, nombre, estudios=None):
    area = {"id": generar_siguiente_id(areas), "nombre": nombre, "estudios": estudios or []}
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


def agregar_estudio_area(areas, area_id, nombre_estudio):
    area = buscar_area_por_id(areas, area_id)
    if area is None:
        return False
    area["estudios"].append(nombre_estudio)
    return True


# --- Disponibilidad por medico (Matrices) ---------------------------------

def inicializar_matriz_disponibilidad(cantidad_dias, cantidad_franjas):
    return [["Libre" for _ in range(cantidad_franjas)] for _ in range(cantidad_dias)]


def obtener_matriz_medico(disponibilidad, medico_id, cantidad_dias, cantidad_franjas):
    if medico_id not in disponibilidad:
        disponibilidad[medico_id] = inicializar_matriz_disponibilidad(cantidad_dias, cantidad_franjas)
    return disponibilidad[medico_id]


def obtener_franjas_libres(matriz, franjas, dia_idx):
    return [franjas[f] for f in range(len(franjas)) if matriz[dia_idx][f] == "Libre"]


def mostrar_franjas_libres(nombre_dia, fecha_texto, franjas_libres):
    print(f"\nHorarios libres el {nombre_dia} {fecha_texto}:")
    if len(franjas_libres) == 0:
        print("No hay horarios libres para este dia.")
    else:
        for franja in franjas_libres:
            print(f"- {franja}")


def marcar_franja(matriz, dia_idx, franja_idx, estado):
    matriz[dia_idx][franja_idx] = estado


def buscar_primer_hueco_libre(matriz, cantidad_dias, cantidad_franjas, dia_idx=0, franja_idx=0):
    if dia_idx >= cantidad_dias:
        return None
    if franja_idx >= cantidad_franjas:
        return buscar_primer_hueco_libre(matriz, cantidad_dias, cantidad_franjas, dia_idx + 1, 0)
    if matriz[dia_idx][franja_idx] == "Libre":
        return (dia_idx, franja_idx)
    return buscar_primer_hueco_libre(matriz, cantidad_dias, cantidad_franjas, dia_idx, franja_idx + 1)


# --- CRUD Pacientes (Diccionarios + Excepciones) --------------------------

def pedir_dni_valido(mensaje):
    while True:
        dni = input(mensaje).strip()
        try:
            if not dni.isdigit():
                raise ValueError("el DNI debe contener solo numeros.")
            if len(dni) < 7 or len(dni) > 8:
                raise ValueError("el DNI debe tener 7 u 8 digitos.")
        except ValueError as error:
            print(f"Dato invalido: {error}")
        else:
            return dni


def buscar_paciente_por_dni(pacientes, dni, indice=0):
    if indice >= len(pacientes):
        return None
    if pacientes[indice]["dni"] == dni:
        return pacientes[indice]
    return buscar_paciente_por_dni(pacientes, dni, indice + 1)


def crear_paciente(pacientes):
    print("\n--- DATOS DEL PACIENTE ---")
    dni = pedir_dni_valido("Ingrese el DNI del paciente: ")
    paciente_existente = buscar_paciente_por_dni(pacientes, dni)
    if paciente_existente is not None:
        print(f"El paciente {paciente_existente['nombre']} ya esta registrado, se reutilizan sus datos.")
        return paciente_existente

    nombre = pedir_texto_valido("Ingrese el nombre y apellido: ", 5, 25, transformar="titulo")
    edad = pedir_entero_valido("Ingrese la edad: ", 0, 110)
    mail = pedir_texto_valido("Ingrese un mail de confirmacion: ", 10, 200, transformar="minusculas")

    paciente = {"dni": dni, "nombre": nombre, "edad": edad, "mail": mail}
    pacientes.append(paciente)
    return paciente


def listar_pacientes(pacientes):
    print(f"\n--- PACIENTES REGISTRADOS ({len(pacientes)}) ---")
    if len(pacientes) == 0:
        print("No hay pacientes cargados.")
    for paciente in pacientes:
        fila = f"{paciente['dni']:<10}{paciente['nombre']:<26}{paciente['edad']:<5}{paciente['mail']}"
        print(fila)


def actualizar_paciente(pacientes, dni, nombre_nuevo=None, edad_nueva=None, mail_nuevo=None):
    paciente = buscar_paciente_por_dni(pacientes, dni)
    if paciente is None:
        return False
    if nombre_nuevo is not None:
        paciente["nombre"] = nombre_nuevo
    if edad_nueva is not None:
        paciente["edad"] = edad_nueva
    if mail_nuevo is not None:
        paciente["mail"] = mail_nuevo
    return True


def eliminar_paciente(pacientes, turnos, dni):
    paciente = buscar_paciente_por_dni(pacientes, dni)
    if paciente is None:
        return False, "El paciente no existe."
    tiene_turnos_activos = any(
        turno["paciente_dni"] == dni and turno["estado"] == "reservado" for turno in turnos
    )
    if tiene_turnos_activos:
        return False, "No se puede eliminar: el paciente tiene turnos reservados."
    pacientes.remove(paciente)
    return True, "Paciente eliminado."


# --- Seleccion interactiva para reservar un turno -------------------------

def elegir_area(areas):
    listar_areas(areas)
    if len(areas) == 0:
        return None
    ids_validos = [area["id"] for area in areas]
    while True:
        area_id = pedir_entero_valido("Elija un area por su numero: ", min(ids_validos), max(ids_validos))
        area = buscar_area_por_id(areas, area_id)
        if area is not None:
            return area
        print("Ese numero no corresponde a un area cargada, reintente.")


def elegir_medico(medicos, areas, area_id):
    listar_medicos(medicos, areas, area_id)
    medicos_del_area = [m for m in medicos if m["area_id"] == area_id]
    if len(medicos_del_area) == 0:
        return None
    ids_validos = [medico["id"] for medico in medicos_del_area]
    while True:
        medico_id = pedir_entero_valido("Elija un medico por su numero: ", min(ids_validos), max(ids_validos))
        if medico_id in ids_validos:
            return buscar_medico_por_id(medicos, medico_id)
        print("Ese numero no corresponde a un medico de esta area, reintente.")


def elegir_estudio(area):
    estudios = area["estudios"]
    print(f"\n--- ESTUDIOS DISPONIBLES EN {area['nombre']} ---")
    if len(estudios) == 0:
        print("Esta area no tiene estudios cargados.")
        return None
    for i in range(len(estudios)):
        print(f"{i + 1}. {estudios[i]}")
    opcion = pedir_entero_valido(f"Elija un estudio (1-{len(estudios)}): ", 1, len(estudios))
    return estudios[opcion - 1]


def elegir_tipo_turno():
    print("\n--- TIPO DE TURNO ---")
    print("1. Turno futuro (elige fecha)")
    print("2. Urgencia (primer horario libre disponible)")
    opcion = pedir_entero_valido("Elija una opcion (1-2): ", 1, 2)
    return "futuro" if opcion == 1 else "urgencia"


def obtener_meses_disponibles(fechas):
    meses = []
    for fecha in fechas:
        anio, mes, _ = fecha
        clave = (anio, mes)
        if clave not in meses:
            meses.append(clave)
    return meses


def elegir_mes(fechas):
    meses = obtener_meses_disponibles(fechas)
    print("\n--- MESES DISPONIBLES ---")
    for i in range(len(meses)):
        anio, mes = meses[i]
        print(f"{i + 1}. {NOMBRES_MESES[mes - 1]} {anio}")
    opcion = pedir_entero_valido(f"Elija un mes (1-{len(meses)}): ", 1, len(meses))
    return meses[opcion - 1]


def elegir_dia_del_mes(fechas, weekday_hoy, anio_mes_elegido):
    anio_sel, mes_sel = anio_mes_elegido
    indices_del_mes = [
        i for i in range(len(fechas)) if fechas[i][0] == anio_sel and fechas[i][1] == mes_sel
    ]
    print(f"\n--- DIAS DISPONIBLES EN {NOMBRES_MESES[mes_sel - 1]} {anio_sel} ---")
    for pos in range(len(indices_del_mes)):
        idx = indices_del_mes[pos]
        _, _, dia = fechas[idx]
        nombre_dia = nombre_dia_semana(weekday_hoy, idx)
        print(f"{pos + 1}. {nombre_dia} {dia:02d}/{mes_sel:02d}")
    opcion = pedir_entero_valido(f"Elija un dia (1-{len(indices_del_mes)}): ", 1, len(indices_del_mes))
    return indices_del_mes[opcion - 1]


def elegir_franja(matriz, franjas, dia_idx, nombre_dia, fecha_texto):
    franjas_libres = obtener_franjas_libres(matriz, franjas, dia_idx)
    mostrar_franjas_libres(nombre_dia, fecha_texto, franjas_libres)
    if len(franjas_libres) == 0:
        return None
    hora_elegida = input("Ingrese el horario deseado (formato HH:MM): ").strip()
    while hora_elegida not in franjas_libres:
        hora_elegida = input("Horario invalido u ocupado. Reingrese: ").strip()
    return franjas.index(hora_elegida)


def obra_social():
    precio_particular = 15000
    plus_coseguro = 3500

    respuesta = input("\n¿Posee Obra Social o Prepaga? (si/no): ").lower().strip()
    while respuesta != "si" and respuesta != "no":
        respuesta = input("Respuesta invalida. Ingrese 'si' o 'no': ").lower().strip()

    match respuesta:
        case "si":
            nombre_os = input("Ingrese el nombre de su Obra Social/Prepaga (ej. OSDE, Swiss Medical): ").strip().upper()
            monto_final = plus_coseguro
        case "no":
            nombre_os = "Particular (Sin Obra Social)"
            monto_final = precio_particular

    return nombre_os, monto_final


# --- CRUD Turnos (nucleo del sistema) --------------------------------------

def crear_turno(turnos, disponibilidad, fechas, franjas, weekday_hoy, paciente, area, medico, estudio, tipo, cobertura, monto):
    cantidad_dias = len(fechas)
    cantidad_franjas = len(franjas)
    matriz = obtener_matriz_medico(disponibilidad, medico["id"], cantidad_dias, cantidad_franjas)

    if tipo == "urgencia":
        hueco = buscar_primer_hueco_libre(matriz, cantidad_dias, cantidad_franjas)
        if hueco is None:
            print("No hay ningun horario libre para este medico en todo el horizonte disponible.")
            return None
        dia_idx, franja_idx = hueco
    else:
        anio_mes_elegido = elegir_mes(fechas)
        dia_idx = elegir_dia_del_mes(fechas, weekday_hoy, anio_mes_elegido)
        anio, mes, dia = fechas[dia_idx]
        nombre_dia = nombre_dia_semana(weekday_hoy, dia_idx)
        fecha_texto = f"{dia:02d}/{mes:02d}/{anio}"
        franja_idx = elegir_franja(matriz, franjas, dia_idx, nombre_dia, fecha_texto)
        if franja_idx is None:
            print(f"No hay horarios libres ese dia para el/la Dr/a. {medico['nombre']}.")
            return None

    marcar_franja(matriz, dia_idx, franja_idx, "Ocupado")
    anio, mes, dia = fechas[dia_idx]

    turno = {
        "id": generar_siguiente_id(turnos),
        "paciente_dni": paciente["dni"],
        "medico_id": medico["id"],
        "area_id": area["id"],
        "estudio": estudio,
        "anio": anio,
        "mes": mes,
        "dia": dia,
        "hora": franjas[franja_idx],
        "tipo": tipo,
        "estado": "reservado",
        "cobertura": cobertura,
        "monto": monto,
    }
    turnos.append(turno)
    return turno


def buscar_turno_por_id(turnos, turno_id):
    for turno in turnos:
        if turno["id"] == turno_id:
            return turno
    return None


def listar_turnos(turnos, pacientes, medicos, areas, medico_id=None, area_id=None, estado=None):
    filtrados = [
        t for t in turnos
        if (medico_id is None or t["medico_id"] == medico_id)
        and (area_id is None or t["area_id"] == area_id)
        and (estado is None or t["estado"] == estado)
    ]
    print(f"\n--- TURNOS ({len(filtrados)}) ---")
    if len(filtrados) == 0:
        print("No hay turnos para este filtro.")
    for turno in filtrados:
        paciente = buscar_paciente_por_dni(pacientes, turno["paciente_dni"])
        medico = buscar_medico_por_id(medicos, turno["medico_id"])
        area = buscar_area_por_id(areas, turno["area_id"])
        nombre_paciente = paciente["nombre"] if paciente is not None else "Paciente eliminado"
        nombre_medico = medico["nombre"] if medico is not None else "Medico eliminado"
        nombre_area = area["nombre"] if area is not None else "Area eliminada"
        fecha_texto = f"{turno['dia']:02d}/{turno['mes']:02d}/{turno['anio']}"
        fila = (
            f"#{turno['id']:<4}{fecha_texto} {turno['hora']:<7}"
            f"{nombre_paciente:<22}Dr/a. {nombre_medico:<18}{nombre_area:<14}{turno['estado']}"
        )
        print(fila)


def buscar_turnos_de_paciente(turnos, dni):
    return [turno for turno in turnos if turno["paciente_dni"] == dni]


def mostrar_turnos_de_paciente(turnos, pacientes, medicos, areas, dni):
    paciente = buscar_paciente_por_dni(pacientes, dni)
    if paciente is None:
        print("No existe un paciente registrado con ese DNI.")
        return
    turnos_paciente = buscar_turnos_de_paciente(turnos, dni)
    print(f"\n--- TURNOS DE {paciente['nombre']} ({len(turnos_paciente)}) ---")
    if len(turnos_paciente) == 0:
        print("Este paciente no tiene turnos registrados.")
    for turno in turnos_paciente:
        medico = buscar_medico_por_id(medicos, turno["medico_id"])
        area = buscar_area_por_id(areas, turno["area_id"])
        nombre_medico = medico["nombre"] if medico is not None else "Medico eliminado"
        nombre_area = area["nombre"] if area is not None else "Area eliminada"
        fecha_texto = f"{turno['dia']:02d}/{turno['mes']:02d}/{turno['anio']}"
        print(
            f"#{turno['id']} - {fecha_texto} {turno['hora']} - Dr/a. {nombre_medico} "
            f"({nombre_area}) - {turno['estudio']} - {turno['tipo']} - {turno['estado']}"
        )


def consultar_turnos_disponibles(areas, medicos, disponibilidad, fechas, franjas, weekday_hoy):
    if len(areas) == 0:
        print("No hay areas cargadas todavia.")
        return
    area = elegir_area(areas)
    medico = elegir_medico(medicos, areas, area["id"])
    if medico is None:
        print("Esta area no tiene medicos cargados.")
        return
    matriz = obtener_matriz_medico(disponibilidad, medico["id"], len(fechas), len(franjas))
    anio_mes_elegido = elegir_mes(fechas)
    dia_idx = elegir_dia_del_mes(fechas, weekday_hoy, anio_mes_elegido)
    anio, mes, dia = fechas[dia_idx]
    nombre_dia = nombre_dia_semana(weekday_hoy, dia_idx)
    fecha_texto = f"{dia:02d}/{mes:02d}/{anio}"
    franjas_libres = obtener_franjas_libres(matriz, franjas, dia_idx)
    mostrar_franjas_libres(nombre_dia, fecha_texto, franjas_libres)


def cancelar_turno(turnos, disponibilidad, fechas, franjas, turno_id):
    turno = buscar_turno_por_id(turnos, turno_id)
    if turno is None:
        return False, "El turno no existe."
    if turno["estado"] == "cancelado":
        return False, "El turno ya estaba cancelado."

    fecha_turno = (turno["anio"], turno["mes"], turno["dia"])
    matriz = disponibilidad.get(turno["medico_id"])
    if matriz is not None and fecha_turno in fechas and turno["hora"] in franjas:
        dia_idx = fechas.index(fecha_turno)
        franja_idx = franjas.index(turno["hora"])
        marcar_franja(matriz, dia_idx, franja_idx, "Libre")

    turno["estado"] = "cancelado"
    return True, "Turno cancelado."


def reprogramar_turno(turnos, disponibilidad, fechas, franjas, weekday_hoy, turno_id):
    turno = buscar_turno_por_id(turnos, turno_id)
    if turno is None or turno["estado"] != "reservado":
        return False, "El turno no existe o no esta activo."

    medico_id = turno["medico_id"]
    matriz = obtener_matriz_medico(disponibilidad, medico_id, len(fechas), len(franjas))

    dia_idx_viejo = fechas.index((turno["anio"], turno["mes"], turno["dia"]))
    franja_idx_viejo = franjas.index(turno["hora"])
    marcar_franja(matriz, dia_idx_viejo, franja_idx_viejo, "Libre")

    anio_mes_elegido = elegir_mes(fechas)
    dia_idx_nuevo = elegir_dia_del_mes(fechas, weekday_hoy, anio_mes_elegido)
    anio, mes, dia = fechas[dia_idx_nuevo]
    nombre_dia = nombre_dia_semana(weekday_hoy, dia_idx_nuevo)
    fecha_texto = f"{dia:02d}/{mes:02d}/{anio}"
    franja_idx_nuevo = elegir_franja(matriz, franjas, dia_idx_nuevo, nombre_dia, fecha_texto)

    if franja_idx_nuevo is None:
        marcar_franja(matriz, dia_idx_viejo, franja_idx_viejo, "Ocupado")
        return False, "No se pudo reprogramar: no hay horarios libres ese dia."

    marcar_franja(matriz, dia_idx_nuevo, franja_idx_nuevo, "Ocupado")
    turno["anio"], turno["mes"], turno["dia"] = anio, mes, dia
    turno["hora"] = franjas[franja_idx_nuevo]
    return True, "Turno reprogramado."


def generar_comprobante(paciente, area, medico, turno):
    fecha_texto = f"{turno['dia']:02d}/{turno['mes']:02d}/{turno['anio']}"
    lineas = []
    lineas.append("=" * 50)
    lineas.append("COMPROBANTE DE RESERVA DE TURNO")
    lineas.append(SANATORIO_NOMBRE)
    lineas.append("=" * 50)
    lineas.append(f"{'Paciente:':<16}{paciente['nombre']}")
    lineas.append(f"{'DNI:':<16}{paciente['dni']}")
    lineas.append(f"{'Edad:':<16}{paciente['edad']}")
    lineas.append(f"{'Mail:':<16}{paciente['mail']}")
    lineas.append("-" * 50)
    lineas.append(f"{'Area:':<16}{area['nombre']}")
    lineas.append(f"{'Medico:':<16}Dr/a. {medico['nombre']}")
    lineas.append(f"{'Estudio:':<16}{turno['estudio']}")
    lineas.append(f"{'Tipo de turno:':<16}{turno['tipo'].capitalize()}")
    lineas.append(f"{'Fecha:':<16}{fecha_texto}")
    lineas.append(f"{'Horario:':<16}{turno['hora']}")
    lineas.append("-" * 50)
    lineas.append(f"{'Cobertura:':<16}{turno['cobertura']}")
    lineas.append(f"{'Total a pagar:':<16}{formatear_monto(turno['monto'])}")
    lineas.append("=" * 50)

    comprobante = "\n".join(lineas)
    print("\n" + comprobante)
    return comprobante


# --- Archivos (persistencia en texto plano, sin csv/json) -----------------

def guardar_lineas_en_archivo(nombre_archivo, lineas):
    archivo = None
    try:
        archivo = open(nombre_archivo, "w", encoding="utf-8")
        for linea in lineas:
            archivo.write(linea + "\n")
    except OSError as error:
        print(f"No se pudo guardar {nombre_archivo}: {error}")
    finally:
        if archivo is not None:
            archivo.close()


def leer_lineas_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            lineas = [linea.rstrip("\n") for linea in archivo]
    except FileNotFoundError:
        lineas = []
    return lineas


def guardar_areas(areas):
    lineas = []
    for area in areas:
        estudios_texto = ",".join(area["estudios"])
        linea = SEPARADOR_CAMPO.join([str(area["id"]), area["nombre"], estudios_texto])
        lineas.append(linea)
    guardar_lineas_en_archivo(ARCHIVO_AREAS, lineas)


def cargar_areas():
    lineas = leer_lineas_archivo(ARCHIVO_AREAS)
    areas = []
    for linea in lineas:
        try:
            partes = linea.split(SEPARADOR_CAMPO)
            area_id = int(partes[0])
            nombre = partes[1]
            estudios = partes[2].split(",") if partes[2] != "" else []
            areas.append({"id": area_id, "nombre": nombre, "estudios": estudios})
        except (ValueError, IndexError):
            print(f"Linea invalida en {ARCHIVO_AREAS}, se ignora: {linea}")
    return areas


def guardar_medicos(medicos):
    lineas = []
    for medico in medicos:
        linea = SEPARADOR_CAMPO.join([str(medico["id"]), medico["nombre"], str(medico["area_id"])])
        lineas.append(linea)
    guardar_lineas_en_archivo(ARCHIVO_MEDICOS, lineas)


def cargar_medicos():
    lineas = leer_lineas_archivo(ARCHIVO_MEDICOS)
    medicos = []
    for linea in lineas:
        try:
            partes = linea.split(SEPARADOR_CAMPO)
            medicos.append({"id": int(partes[0]), "nombre": partes[1], "area_id": int(partes[2])})
        except (ValueError, IndexError):
            print(f"Linea invalida en {ARCHIVO_MEDICOS}, se ignora: {linea}")
    return medicos


def guardar_pacientes(pacientes):
    lineas = []
    for paciente in pacientes:
        linea = SEPARADOR_CAMPO.join(
            [paciente["dni"], paciente["nombre"], str(paciente["edad"]), paciente["mail"]]
        )
        lineas.append(linea)
    guardar_lineas_en_archivo(ARCHIVO_PACIENTES, lineas)


def cargar_pacientes():
    lineas = leer_lineas_archivo(ARCHIVO_PACIENTES)
    pacientes = []
    for linea in lineas:
        try:
            partes = linea.split(SEPARADOR_CAMPO)
            pacientes.append({
                "dni": partes[0],
                "nombre": partes[1],
                "edad": int(partes[2]),
                "mail": partes[3],
            })
        except (ValueError, IndexError):
            print(f"Linea invalida en {ARCHIVO_PACIENTES}, se ignora: {linea}")
    return pacientes


def guardar_turnos(turnos):
    lineas = []
    for turno in turnos:
        linea = SEPARADOR_CAMPO.join([
            str(turno["id"]),
            turno["paciente_dni"],
            str(turno["medico_id"]),
            str(turno["area_id"]),
            turno["estudio"],
            str(turno["anio"]),
            str(turno["mes"]),
            str(turno["dia"]),
            turno["hora"],
            turno["tipo"],
            turno["estado"],
            turno["cobertura"],
            str(turno["monto"]),
        ])
        lineas.append(linea)
    guardar_lineas_en_archivo(ARCHIVO_TURNOS, lineas)


def cargar_turnos():
    lineas = leer_lineas_archivo(ARCHIVO_TURNOS)
    turnos = []
    for linea in lineas:
        try:
            partes = linea.split(SEPARADOR_CAMPO)
            turnos.append({
                "id": int(partes[0]),
                "paciente_dni": partes[1],
                "medico_id": int(partes[2]),
                "area_id": int(partes[3]),
                "estudio": partes[4],
                "anio": int(partes[5]),
                "mes": int(partes[6]),
                "dia": int(partes[7]),
                "hora": partes[8],
                "tipo": partes[9],
                "estado": partes[10],
                "cobertura": partes[11],
                "monto": float(partes[12]),
            })
        except (ValueError, IndexError):
            print(f"Linea invalida en {ARCHIVO_TURNOS}, se ignora: {linea}")
    return turnos


def reconstruir_disponibilidad(turnos, fechas, franjas):
    disponibilidad = {}
    for turno in turnos:
        if turno["estado"] != "reservado":
            continue
        fecha_turno = (turno["anio"], turno["mes"], turno["dia"])
        if fecha_turno not in fechas or turno["hora"] not in franjas:
            continue
        matriz = obtener_matriz_medico(disponibilidad, turno["medico_id"], len(fechas), len(franjas))
        dia_idx = fechas.index(fecha_turno)
        franja_idx = franjas.index(turno["hora"])
        marcar_franja(matriz, dia_idx, franja_idx, "Ocupado")
    return disponibilidad


def guardar_datos(areas, medicos, pacientes, turnos):
    guardar_areas(areas)
    guardar_medicos(medicos)
    guardar_pacientes(pacientes)
    guardar_turnos(turnos)
    print("\nDatos guardados en areas.txt, medicos.txt, pacientes.txt y turnos.txt.")


def cargar_datos():
    areas = cargar_areas()
    medicos = cargar_medicos()
    pacientes = cargar_pacientes()
    turnos = cargar_turnos()
    return areas, medicos, pacientes, turnos


# --- Estadisticas -----------------------------------------------------------

def calcular_estadisticas(turnos, medicos, areas):
    por_area = {}
    por_medico = {}
    for turno in turnos:
        area = buscar_area_por_id(areas, turno["area_id"])
        nombre_area = area["nombre"] if area is not None else "Area eliminada"
        por_area[nombre_area] = por_area.get(nombre_area, 0) + 1

        medico = buscar_medico_por_id(medicos, turno["medico_id"])
        nombre_medico = medico["nombre"] if medico is not None else "Medico eliminado"
        por_medico[nombre_medico] = por_medico.get(nombre_medico, 0) + 1

    return {
        "total": len(turnos),
        "reservados": len([t for t in turnos if t["estado"] == "reservado"]),
        "cancelados": len([t for t in turnos if t["estado"] == "cancelado"]),
        "urgencias": len([t for t in turnos if t["tipo"] == "urgencia"]),
        "futuros": len([t for t in turnos if t["tipo"] == "futuro"]),
        "por_area": por_area,
        "por_medico": por_medico,
    }


def mostrar_estadisticas(estadisticas):
    print("\n" + "=" * 50)
    print("ESTADISTICAS DEL SANATORIO")
    print("=" * 50)
    print(f"Total de turnos registrados: {estadisticas['total']}")
    print(f"  Reservados: {estadisticas['reservados']}")
    print(f"  Cancelados: {estadisticas['cancelados']}")
    print(f"  Urgencias: {estadisticas['urgencias']}")
    print(f"  Futuros: {estadisticas['futuros']}")

    print("\nTurnos por area:")
    if len(estadisticas["por_area"]) == 0:
        print("  (sin datos)")
    for nombre_area, cantidad in estadisticas["por_area"].items():
        print(f"  {nombre_area}: {cantidad}")

    print("\nTurnos por medico:")
    if len(estadisticas["por_medico"]) == 0:
        print("  (sin datos)")
    for nombre_medico, cantidad in estadisticas["por_medico"].items():
        print(f"  Dr/a. {nombre_medico}: {cantidad}")
    print("=" * 50)


# --- Menus interactivos ------------------------------------------------

def ejecutar_gestion_areas(areas, medicos):
    continuar_submenu = True
    while continuar_submenu:
        print("\n--- GESTION DE AREAS ---")
        print("1. Listar areas")
        print("2. Crear area")
        print("3. Agregar estudio a un area")
        print("4. Renombrar area")
        print("5. Eliminar area")
        print("6. Volver al menu principal")
        opcion = pedir_entero_valido("Elija una opcion (1-6): ", 1, 6)

        match opcion:
            case 1:
                listar_areas(areas)
            case 2:
                nombre = pedir_texto_valido("Nombre de la nueva area: ", 3, 30, transformar="titulo")
                area = crear_area(areas, nombre)
                print(f"Area creada con id {area['id']}.")
            case 3:
                listar_areas(areas)
                area_id = pedir_entero_valido("Id del area: ", 1, generar_siguiente_id(areas))
                estudio = pedir_texto_valido("Nombre del estudio/practica: ", 3, 40, transformar="titulo")
                if agregar_estudio_area(areas, area_id, estudio):
                    print("Estudio agregado.")
                else:
                    print("No existe un area con ese id.")
            case 4:
                listar_areas(areas)
                area_id = pedir_entero_valido("Id del area a renombrar: ", 1, generar_siguiente_id(areas))
                nombre_nuevo = pedir_texto_valido("Nuevo nombre: ", 3, 30, transformar="titulo")
                if actualizar_area(areas, area_id, nombre_nuevo):
                    print("Area actualizada.")
                else:
                    print("No existe un area con ese id.")
            case 5:
                listar_areas(areas)
                area_id = pedir_entero_valido("Id del area a eliminar: ", 1, generar_siguiente_id(areas))
                ok, mensaje = eliminar_area(areas, medicos, area_id)
                print(mensaje)
            case 6:
                continuar_submenu = False


def ejecutar_gestion_medicos(medicos, areas, turnos):
    continuar_submenu = True
    while continuar_submenu:
        print("\n--- GESTION DE MEDICOS ---")
        print("1. Listar medicos")
        print("2. Crear medico")
        print("3. Reasignar medico a otra area")
        print("4. Eliminar medico")
        print("5. Volver al menu principal")
        opcion = pedir_entero_valido("Elija una opcion (1-5): ", 1, 5)

        match opcion:
            case 1:
                listar_medicos(medicos, areas)
            case 2:
                if len(areas) == 0:
                    print("Primero tiene que crear al menos un area.")
                else:
                    area = elegir_area(areas)
                    nombre = pedir_texto_valido("Nombre y apellido del medico: ", 5, 30, transformar="titulo")
                    medico = crear_medico(medicos, nombre, area["id"])
                    print(f"Medico creado con id {medico['id']}.")
            case 3:
                listar_medicos(medicos, areas)
                medico_id = pedir_entero_valido("Id del medico: ", 1, generar_siguiente_id(medicos))
                area = elegir_area(areas)
                if actualizar_medico(medicos, medico_id, area_id_nuevo=area["id"]):
                    print("Medico reasignado.")
                else:
                    print("No existe un medico con ese id.")
            case 4:
                listar_medicos(medicos, areas)
                medico_id = pedir_entero_valido("Id del medico a eliminar: ", 1, generar_siguiente_id(medicos))
                ok, mensaje = eliminar_medico(medicos, turnos, medico_id)
                print(mensaje)
            case 5:
                continuar_submenu = False


def ejecutar_gestion_pacientes(pacientes, turnos):
    continuar_submenu = True
    while continuar_submenu:
        print("\n--- GESTION DE PACIENTES ---")
        print("1. Listar pacientes")
        print("2. Crear paciente")
        print("3. Actualizar mail de un paciente")
        print("4. Eliminar paciente")
        print("5. Volver al menu principal")
        opcion = pedir_entero_valido("Elija una opcion (1-5): ", 1, 5)

        match opcion:
            case 1:
                listar_pacientes(pacientes)
            case 2:
                paciente = crear_paciente(pacientes)
                print(f"Paciente {paciente['nombre']} listo (DNI {paciente['dni']}).")
            case 3:
                dni = pedir_dni_valido("DNI del paciente: ")
                mail_nuevo = pedir_texto_valido("Nuevo mail: ", 10, 200, transformar="minusculas")
                if actualizar_paciente(pacientes, dni, mail_nuevo=mail_nuevo):
                    print("Mail actualizado.")
                else:
                    print("No existe un paciente con ese DNI.")
            case 4:
                dni = pedir_dni_valido("DNI del paciente a eliminar: ")
                ok, mensaje = eliminar_paciente(pacientes, turnos, dni)
                print(mensaje)
            case 5:
                continuar_submenu = False


def ejecutar_reserva_turno(pacientes, areas, medicos, turnos, disponibilidad, fechas, franjas, weekday_hoy):
    if len(areas) == 0:
        print("No hay areas cargadas todavia, pida a un administrador que cree al menos una.")
        return

    print("\n--- RESERVAR TURNO ---")
    paciente = crear_paciente(pacientes)
    area = elegir_area(areas)
    medico = elegir_medico(medicos, areas, area["id"])
    if medico is None:
        print("Esta area no tiene medicos disponibles.")
        return
    estudio = elegir_estudio(area)
    if estudio is None:
        return
    tipo = elegir_tipo_turno()
    cobertura, monto = obra_social()

    turno = crear_turno(
        turnos, disponibilidad, fechas, franjas, weekday_hoy,
        paciente, area, medico, estudio, tipo, cobertura, monto,
    )
    if turno is None:
        return
    generar_comprobante(paciente, area, medico, turno)


def ejecutar_consulta_turnos(pacientes, medicos, areas, turnos, disponibilidad, fechas, franjas, weekday_hoy):
    continuar_submenu = True
    while continuar_submenu:
        print("\n--- CONSULTAR TURNOS ---")
        print("1. Ver horarios disponibles de un medico")
        print("2. Ver turnos de un paciente (por DNI)")
        print("3. Listar todos los turnos")
        print("4. Volver al menu principal")
        opcion = pedir_entero_valido("Elija una opcion (1-4): ", 1, 4)

        match opcion:
            case 1:
                consultar_turnos_disponibles(areas, medicos, disponibilidad, fechas, franjas, weekday_hoy)
            case 2:
                dni = pedir_dni_valido("DNI del paciente: ")
                mostrar_turnos_de_paciente(turnos, pacientes, medicos, areas, dni)
            case 3:
                listar_turnos(turnos, pacientes, medicos, areas)
            case 4:
                continuar_submenu = False


def ejecutar_cancelar_o_reprogramar(turnos, pacientes, medicos, areas, disponibilidad, fechas, franjas, weekday_hoy):
    listar_turnos(turnos, pacientes, medicos, areas, estado="reservado")
    if len(turnos) == 0:
        return

    print("\n1. Cancelar un turno")
    print("2. Reprogramar un turno")
    opcion = pedir_entero_valido("Elija una opcion (1-2): ", 1, 2)
    turno_id = pedir_entero_valido("Numero de turno (#): ", 1, generar_siguiente_id(turnos))

    if opcion == 1:
        ok, mensaje = cancelar_turno(turnos, disponibilidad, fechas, franjas, turno_id)
    else:
        ok, mensaje = reprogramar_turno(turnos, disponibilidad, fechas, franjas, weekday_hoy, turno_id)
    print(mensaje)


def seed_datos_iniciales(areas, medicos):
    if len(areas) > 0:
        return
    catalogo = [
        ("Cardiologia", ["Consulta - Control", "Electrocardiograma", "Ecocardiograma"],
         ["Julian Perez", "Marina Sosa"]),
        ("Traumatologia", ["Consulta", "Radiografia", "Infiltracion"],
         ["Ezequiel Lima"]),
        ("Pediatria", ["Consulta - Control", "Apto fisico escolar", "Vacunacion de calendario"],
         ["Carla Nunez", "Tomas Ferro"]),
        ("Dermatologia", ["Consulta - Control", "Biopsia de piel", "Crioterapia"],
         ["Ines Roldan"]),
        ("Clinica Medica", ["Consulta general", "Control de rutina", "Certificado medico"],
         ["Pablo Ortega", "Natalia Vega"]),
        ("Oftalmologia", ["Consulta", "Control de fondo de ojo", "Test de agudeza visual"],
         ["Ramiro Diaz"]),
    ]
    for nombre_area, estudios, nombres_medicos in catalogo:
        area = crear_area(areas, nombre_area, estudios)
        for nombre_medico in nombres_medicos:
            crear_medico(medicos, nombre_medico, area["id"])
