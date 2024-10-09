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
        tipo_persona = console.input("Ingrese el tipo de persona ([cyan]médico[/cyan] o [cyan]paciente[/cyan]): ")
        identificacion = console.input("Ingrese la identificación: ")
        nombre = console.input("Ingrese el nombre: ")
        celular = console.input("Ingrese el celular: ")

        if tipo_persona.lower() == "medico":
            especialidad = console.input("Ingrese la especialidad: ")
            persona = PersonasFactory.crear_persona("medico", identificacion, nombre, celular, especialidad)
            hospital.agregar_medico(persona)
            console.print(f"[green]Médico {nombre} agregado exitosamente.[/green]")
        elif tipo_persona.lower() == "paciente":
            correo = console.input("Ingrese el correo: ")
            persona = PersonasFactory.crear_persona("paciente", identificacion, nombre, celular, correo=correo)
            hospital.agregar_paciente(persona)
            console.print(f"[green]Paciente {nombre} agregado exitosamente.[/green]")
        else:
            console.print("[red]Tipo de persona inválido.[/red]")

    elif opcion == "2":
        id_paciente = console.input("Ingrese la identificación del paciente: ")
        id_medico = console.input("Ingrese la identificación del médico: ")
        fecha = console.input("Ingrese la fecha de la cita (YYYY-MM-DD): ")
        motivo = console.input("Ingrese el motivo de la cita: ")

        paciente = hospital.buscar_paciente(id_paciente)
        medico = hospital.buscar_medico(id_medico)

        if paciente and medico:
            paciente.pedir_cita(medico, fecha, motivo)
        else:
            console.print("[red]Paciente o médico no encontrado.[/red]")

    elif opcion == "3":
        id_paciente = console.input("Ingrese la identificación del paciente: ")
        paciente = hospital.buscar_paciente(id_paciente)

        if paciente:
            console.print("[bold]Citas pendientes:[/bold]")
            table = Table(title="Citas Pendientes")
            table.add_column("No.", justify="right")
            table.add_column("Fecha", style="cyan")
            table.add_column("Médico", style="magenta")

            for i, cita in enumerate(paciente.agenda.citas_pendientes):
                table.add_row(str(i+1), cita.fecha, cita.medico.nombre)

            console.print(table)

            opcion_cita = int(console.input("Seleccione la cita a cancelar: "))
            if 1 <= opcion_cita <= len(paciente.agenda.citas_pendientes):
                cita_a_cancelar = paciente.agenda.citas_pendientes[opcion_cita - 1]
                paciente.cancelar_cita(cita_a_cancelar)
            else:
                console.print("[red]Opción inválida.[/red]")
        else:
            console.print("[red]Paciente no encontrado.[/red]")

    elif opcion == "4":
        id_paciente = console.input("Ingrese la identificación del paciente: ")
        id_medico = console.input("Ingrese la identificación del médico: ")

        paciente = hospital.buscar_paciente(id_paciente)
        medico = hospital.buscar_medico(id_medico)

        if paciente and medico:
            paciente.asignar_medico_preferencia(medico)
        else:
            console.print("[red]Paciente o médico no encontrado.[/red]")

    elif opcion == "5":
        id_paciente = console.input("Ingrese la identificación del paciente: ")
        paciente = hospital.buscar_paciente(id_paciente)

        if paciente:
            console.print("[bold]Citas pendientes:[/bold]")
            for cita in paciente.agenda.citas_pendientes:
                console.print(cita)
        else:
            console.print("[red]Paciente no encontrado.[/red]")

    elif opcion == "6":
        console.print("[bold green]Saliendo del programa...[/bold green]")
        break

    else:
        console.print("[red]Opción inválida.[/red]")
