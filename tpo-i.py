DIAS_SEMANA = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
FRANJAS_HORARIAS = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]


def datos_paciente():
    nombre_c = input("Ingrese el nombre y apellido del paciente: ").strip()
    while len(nombre_c) < 5 or len(nombre_c) > 25:
        print("Error el nombre y apellido ingresado es invalido")
        nombre_c = input("Reingrese el nombre y apellido del paciente: ").strip()
    nombre_c = nombre_c.title()

    edad = int(input("Ingrese la edad del paciente: "))
    while edad < 0 or edad > 110:
        print("Error la edad ingresada es invalida")
        edad = int(input("Reingrese la edad del paciente: "))

    mail = input("Ingrese un mail de confirmacion: ").lower().strip()
    while len(mail) < 10 or len(mail) > 200:
        print("Error el mail ingresado es invalido")
        mail = input("Reingrese un mail de confirmacion: ").lower().strip()

    dni = input("Ingrese el DNI del paciente: ").strip()
    while not dni.isdigit() or not (7 <= len(dni) <= 8): 
        print("Error el DNI ingresado es invalido")
        dni = input("Reingrese el DNI del paciente: ").strip()

    return [nombre_c, edad, dni, mail]


def seleccionar_estudio(especialidades, cardio, trauma, derma, pediatra):
    print("\n--- ESPECIALIDADES DISPONIBLES ---")
    opciones_especialidades = [f"{i + 1}. {especialidades[i]}" for i in range(len(especialidades))]
    for opcion in opciones_especialidades:
        print(opcion)

    eleccion = int(input("Elija un numero del 1-4 segun la especialidad requerida: "))
    while eleccion < 1 or eleccion > 4:
        print("Especialidad no disponible")
        eleccion = int(input("Elija un numero del 1-4 segun la especialidad requerida: "))

    match eleccion:
        case 1:
            lista_estudios = cardio
        case 2:
            lista_estudios = trauma
        case 3:
            lista_estudios = pediatra
        case 4:
            lista_estudios = derma

    print(f"\n--- Practicas disponibles en {especialidades[eleccion - 1]} ---")
    opciones_estudios = [f"{i + 1}. {lista_estudios[i]}" for i in range(len(lista_estudios))]
    for opcion in opciones_estudios:
        print(opcion)

    estudio_opc = int(input("\nSeleccione el motivo de consulta/estudio: "))
    while estudio_opc < 1 or estudio_opc > len(lista_estudios):
        estudio_opc = int(input("Opcion invalida. Reingrese: "))

    return especialidades[eleccion - 1], lista_estudios[estudio_opc - 1]


def mostrar_disponibilidad(matriz_turnos):
    print("\n--- GRILLA DE DISPONIBILIDAD ---")
    encabezado = f"{'':<12}"
    for franja in FRANJAS_HORARIAS:
        encabezado += f"{franja:<10}"
    print(encabezado)
    for d in range(len(DIAS_SEMANA)):
        fila = f"{DIAS_SEMANA[d]:<12}"
        for h in range(len(FRANJAS_HORARIAS)):
            fila += f"{matriz_turnos[d][h]:<10}"
        print(fila)


def elegir_turno(matriz_turnos):
    mostrar_disponibilidad(matriz_turnos)
    print("\nDias disponibles:")
    for d in range(len(DIAS_SEMANA)):
        print(f"{d + 1}. {DIAS_SEMANA[d]}")

    turno_reservado = False
    while not turno_reservado:
        dia_opc = int(input(f"\nElija un dia (1-{len(DIAS_SEMANA)}): "))
        while dia_opc < 1 or dia_opc > len(DIAS_SEMANA):
            dia_opc = int(input(f"Dia invalido. Elija un dia (1-{len(DIAS_SEMANA)}): "))
        dia_idx = dia_opc - 1

        horas_libres = [FRANJAS_HORARIAS[h] for h in range(len(FRANJAS_HORARIAS)) if matriz_turnos[dia_idx][h] == "Libre"]
        if len(horas_libres) == 0:
            print(f"No quedan turnos libres el {DIAS_SEMANA[dia_idx]}, elija otro dia")
            continue

        print(f"\nHorarios libres el {DIAS_SEMANA[dia_idx]}:")
        for horario in horas_libres:
            print(f"- {horario}")

        hora_elegida = input("Ingrese el horario deseado (formato HH:MM): ").strip()
        while hora_elegida not in horas_libres:
            hora_elegida = input("Horario invalido u ocupado. Reingrese: ").strip()

        franja_idx = FRANJAS_HORARIAS.index(hora_elegida)
        matriz_turnos[dia_idx][franja_idx] = "Ocupado"
        turno_reservado = True

    return DIAS_SEMANA[dia_idx], FRANJAS_HORARIAS[franja_idx]


def obra_social():
    precio_particular = 15000
    plus_coseguro = 3500

    respuesta = input("\n¿Posee Obra Social o Prepaga? (si/no): ").lower().strip()
    while respuesta != "si" and respuesta != "no":
        respuesta = input("Respuesta invalida. Ingrese 'si' o 'no': ").lower().strip()

    match respuesta:
        case "si":
            nombre_os = input("Ingrese el nombre de su Obra Social/Prepaga (ej. OSDE, Swiss Medical): ").strip().upper()
            print(f"\nCobertura registrada: {nombre_os}")
            print(f"Su entidad cubre la practica base. Corresponde abonar un coseguro/plus de: ${plus_coseguro}")
            monto_final = plus_coseguro
        case "no":
            nombre_os = "Particular (Sin Obra Social)"
            print(f"\nAtencion Particular: Debe abonar el valor total de la consulta/estudio: ${precio_particular}")
            monto_final = precio_particular

    return nombre_os, monto_final


def formatear_monto(monto):
    return f"${monto:,.0f}".replace(",", ".")


def generar_comprobante(datos, especialidad, estudio, dia, hora, obra_social_nombre, monto):
    nombre_c, edad, dni, mail = datos
    lineas = []
    lineas.append("=" * 45)
    lineas.append("COMPROBANTE DE RESERVA DE TURNO")
    lineas.append("SANATORIO SAN ROQUE")
    lineas.append("=" * 45)
    lineas.append(f"{'Paciente:':<16}{nombre_c}")
    lineas.append(f"{'DNI:':<16}{dni}")
    lineas.append(f"{'Edad:':<16}{edad}")
    lineas.append(f"{'Mail:':<16}{mail}")
    lineas.append("-" * 45)
    lineas.append(f"{'Especialidad:':<16}{especialidad}")
    lineas.append(f"{'Estudio:':<16}{estudio}")
    lineas.append(f"{'Dia:':<16}{dia}")
    lineas.append(f"{'Horario:':<16}{hora}")
    lineas.append("-" * 45)
    lineas.append(f"{'Cobertura:':<16}{obra_social_nombre}")
    lineas.append(f"{'Total a pagar:':<16}{formatear_monto(monto)}")
    lineas.append("=" * 45)

    comprobante = "\n".join(lineas)
    print("\n" + comprobante)
    return comprobante


def mostrar_resumen_turnos(lista_turnos):
    print("\n" + "=" * 60)
    print("RESUMEN DE TURNOS RESERVADOS EN ESTA SESION")
    print("=" * 60)
    if len(lista_turnos) == 0:
        print("No se registraron turnos.")
    for turno in lista_turnos:
        nombre_c, dni, especialidad, estudio, dia, hora, monto = turno
        fila = f"{nombre_c:<22}{dni:<11}{especialidad:<14}{estudio:<24}{dia:<11}{hora:<7}{formatear_monto(monto)}"
        print(fila)
    print("=" * 60)


#programa
print("¡Hola! Bienvenido a la sucursal virtual del Sanatorio San Roque")

especialidades = ["Cardiologia", "Traumatologia", "Pediatria", "Dermatologia"]
cardio = ["Consulta - control", "Electrocardiograma", "Ecocardiograma"]
trauma = ["Consulta", "Radiografia", "Infiltracion"]
derma = ["Consulta - Control", "Biopsia de piel", "Crioterapia"]
pediatra = ["Consulta - Control", "Apto fisico escolar", "Vacunacion de calendario"]

matriz_turnos = [["Libre" for _ in range(len(FRANJAS_HORARIAS))] for _ in range(len(DIAS_SEMANA))]
lista_turnos = []

continuar = True
while continuar:
    print("\n--- MENU PRINCIPAL ---")
    print("1. Atender nuevo paciente")
    print("2. Finalizar y ver resumen")
    opcion_menu = int(input("Elija una opcion: "))
    while opcion_menu != 1 and opcion_menu != 2:
        opcion_menu = int(input("Opcion invalida. Elija 1 o 2: "))

    match opcion_menu:
        case 1:
            datos = datos_paciente()
            especialidad, estudio = seleccionar_estudio(especialidades, cardio, trauma, derma, pediatra)
            dia, hora = elegir_turno(matriz_turnos)
            obra_social_nombre, monto = obra_social()
            generar_comprobante(datos, especialidad, estudio, dia, hora, obra_social_nombre, monto)
            lista_turnos.append([datos[0], datos[2], especialidad, estudio, dia, hora, monto])
        case 2:
            continuar = False

mostrar_resumen_turnos(lista_turnos)