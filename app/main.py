from hospital import Hospital
from persona_factory import PersonasFactory
from rich.console import Console
from rich.table import Table

console = Console()
hospital = Hospital()

def mostrar_menu():
    console.print("\n[bold green]--- Menú ---[/bold green]")
    console.print("1. Agregar persona")
    console.print("2. Pedir cita")
    console.print("3. Cancelar cita")
    console.print("4. Asignar médico de preferencia")
    console.print("5. Ver citas pendientes")
    console.print("6. Reagendar cita")  # Nueva opción
    console.print("7. Actualizar paciente")  # Nueva opción
    console.print("8. Actualizar médico")  # Nueva opción
    console.print("9. Salir")

while True:
    mostrar_menu()
    opcion = console.input("[bold blue]Seleccione una opción: [/bold blue]")

    if opcion == "1":
        tipo_persona = console.input("Ingrese el tipo de persona ([cyan]médico[/cyan] o [cyan]paciente[/cyan]): ").lower()
        identificacion = console.input("Ingrese la identificación: ")
        nombre = console.input("Ingrese el nombre: ")
        celular = console.input("Ingrese el celular: ")

        if tipo_persona == "medico":
            especialidad = console.input("Ingrese la especialidad: ")
            persona = PersonasFactory.crear_persona("medico", identificacion, nombre, celular, especialidad)
            hospital.agregar_medico(persona)
            console.print(f"[green]Médico {nombre} agregado exitosamente.[/green]")
        elif tipo_persona == "paciente":
            correo = console.input("Ingrese el correo: ")
            persona = PersonasFactory.crear_persona("paciente", identificacion, nombre, celular, correo=correo)
            hospital.agregar_paciente(persona)
            console.print(f"[green]Paciente {nombre} agregado exitosamente.[/green]")
        else:
            console.print("[red]Tipo de persona inválido.[/red]")

    elif opcion == "2":  # Pedir cita
        id_paciente = console.input("Ingrese la identificación del paciente: ")
        especialidad = console.input("Ingrese la especialidad requerida: ")
        fecha = console.input("Ingrese la fecha y hora de la cita (YYYY-MM-DD HH:MM): ")

        paciente = hospital.buscar_paciente(id_paciente)
        if paciente:
            medicos_disponibles = hospital.buscar_medicos_por_especialidad(especialidad)
            if medicos_disponibles:
                console.print("Médicos disponibles:")
                table = Table(title="Médicos Disponibles")
                table.add_column("No.", justify="right")
                table.add_column("Nombre", style="cyan")
                table.add_column("Especialidad", style="magenta")

                for i, medico in enumerate(medicos_disponibles):
                    table.add_row(str(i + 1), medico.nombre, medico.especialidad)

                console.print(table)
                opcion_medico = int(console.input("Seleccione el médico (número): ")) - 1
                if 0 <= opcion_medico < len(medicos_disponibles):
                    medico_seleccionado = medicos_disponibles[opcion_medico]
                    paciente.agendar_cita(medico_seleccionado, fecha)
                    console.print(f"[green]Cita asignada exitosamente con el Dr. {medico_seleccionado.nombre} para el {fecha}.[/green]")
                else:
                    console.print("[red]Opción de médico inválida.[/red]")
            else:
                console.print("[red]No hay médicos disponibles para esa especialidad.[/red]")
        else:
            console.print("[red]Paciente no encontrado.[/red]")

    elif opcion == "3":  # Cancelar cita
        id_paciente = console.input("Ingrese la identificación del paciente: ")
        paciente = hospital.buscar_paciente(id_paciente)

        if paciente:
            citas_pendientes = [cita for cita in hospital.citas if cita.paciente == paciente]

            if citas_pendientes:
                console.print("[bold]Citas pendientes:[/bold]")
                table = Table(title="Citas Pendientes")
                table.add_column("No.", justify="right")
                table.add_column("Fecha", style="cyan")
                table.add_column("Médico", style="magenta")

                # Mostrar las citas pendientes del paciente
                for i, cita in enumerate(citas_pendientes):
                    table.add_row(str(i + 1), cita.fecha, cita.medico.nombre)

                console.print(table)
                opcion_cita = int(console.input("Seleccione la cita a cancelar (número): ")) - 1
                if 0 <= opcion_cita < len(citas_pendientes):
                    cita_seleccionada = citas_pendientes[opcion_cita]
                    hospital.cancelar_cita(paciente.identificacion, cita_seleccionada.fecha)
                else:
                    console.print("[red]Número de cita inválido.[/red]")
            else:
                console.print("[red]El paciente no tiene citas pendientes.[/red]")
        else:
            console.print("[red]Paciente no encontrado.[/red]")

    elif opcion == "4":  # Asignar médico de preferencia
        id_paciente = console.input("Ingrese la identificación del paciente: ")
        id_medico = console.input("Ingrese la identificación del médico: ")

        paciente = hospital.buscar_paciente(id_paciente)
        medico = hospital.buscar_medico(id_medico)

        if paciente and medico:
            paciente.asignar_medico_preferencia(medico)
            console.print(f"[green]Médico {medico.nombre} asignado como preferencia para {paciente.nombre}.[/green]")
        else:
            console.print("[red]Paciente o médico no encontrado.[/red]")

    elif opcion == "5":  # Ver citas pendientes
        id_paciente = console.input("Ingrese la identificación del paciente: ")
        paciente = hospital.buscar_paciente(id_paciente)

        if paciente:
            console.print("[bold]Citas pendientes:[/bold]")
            citas_pendientes = [cita for cita in hospital.citas if cita.paciente == paciente]

            if citas_pendientes:
                table = Table(title="Citas Pendientes")
                table.add_column("No.", justify="right")
                table.add_column("Fecha", style="cyan")
                table.add_column("Médico", style="magenta")

                for i, cita in enumerate(citas_pendientes):
                    table.add_row(str(i + 1), cita.fecha, cita.medico.nombre)

                console.print(table)
            else:
                console.print("[red]No hay citas pendientes.[/red]")
        else:
            console.print("[red]Paciente no encontrado.[/red]")

    elif opcion == "6":  # Reagendar cita
        id_paciente = console.input("Ingrese la identificación del paciente: ")
        fecha_actual = console.input("Ingrese la fecha actual de la cita (YYYY-MM-DD HH:MM): ")
        nueva_fecha = console.input("Ingrese la nueva fecha y hora de la cita (YYYY-MM-DD HH:MM): ")

        hospital.reagendar_cita(id_paciente, fecha_actual, nueva_fecha)

    elif opcion == "7":  # Actualizar paciente
        id_paciente = console.input("Ingrese la identificación del paciente a actualizar: ")
        nuevo_nombre = console.input("Ingrese el nuevo nombre (o presione Enter para no cambiar): ")
        nuevo_celular = console.input("Ingrese el nuevo celular (o presione Enter para no cambiar): ")
        nuevo_correo = console.input("Ingrese el nuevo correo (o presione Enter para no cambiar): ")

        hospital.actualizar_paciente(id_paciente, nuevo_nombre, nuevo_celular, nuevo_correo)

    elif opcion == "8":  # Actualizar médico
        id_medico = console.input("Ingrese la identificación del médico a actualizar: ")
        nuevo_nombre = console.input("Ingrese el nuevo nombre (o presione Enter para no cambiar): ")
        nuevo_celular = console.input("Ingrese el nuevo celular (o presione Enter para no cambiar): ")
        nueva_especialidad = console.input("Ingrese la nueva especialidad (o presione Enter para no cambiar): ")

        hospital.actualizar_medico(id_medico, nuevo_nombre, nuevo_celular, nueva_especialidad)

    elif opcion == "9":  # Salir del programa
        console.print("[bold green]Saliendo del programa...[/bold green]")
        break

    else:
        console.print("[red]Opción inválida.[/red]")

