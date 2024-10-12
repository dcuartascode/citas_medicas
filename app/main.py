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
    console.print("6. Salir")

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
            correo = console.input("Ingrese el correo: ")
            persona = PersonasFactory.crear_persona("medico", identificacion, nombre, celular, especialidad, correo)
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
        fecha = console.input("Ingrese la fecha de la cita (YYYY-MM-DD HH:MM): ")  # Incluye fecha y hora en intervalos de 20 minutos
        motivo = console.input("Ingrese el motivo de la cita: ")

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
                    hospital.agendar_cita(id_paciente, especialidad, fecha)
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
            fecha_cita = console.input("Ingrese la fecha de la cita a cancelar (YYYY-MM-DD HH:MM): ")
            hospital.cancelar_cita(id_paciente, fecha_cita)
            console.print("[green]Cita cancelada exitosamente.[/green]")
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
            citas_pendientes = [c for c in hospital.citas if c.paciente == paciente]

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

    elif opcion == "6":  # Salir del programa
        console.print("[bold green]Saliendo del programa...[/bold green]")
        break

    else:
        console.print("[red]Opción inválida.[/red]")


