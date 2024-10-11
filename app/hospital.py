import json
import csv
from medico import Medico
from paciente import Paciente
from cita import Cita
from rich.console import Console

class Hospital:
    def __init__(self):
        self.console = Console()  # Crear una instancia de Console
        self.pacientes = []
        self.medicos = []
        self.citas = []  # Almacena las citas

        # Cargar médicos, pacientes y citas al inicializar la clase
        self.cargar_medicos()
        self.cargar_pacientes()
        self.cargar_citas()

    def cargar_medicos(self):
        try:
            with open(r"C:\Users\david\Desktop\Nueva carpeta\citas_medicas\datos\medicos.json", 'r', encoding='utf-8') as archivo:
                medicos_json = json.load(archivo)
                for medico_data in medicos_json:
                    medico = Medico(
                        medico_data['id'], 
                        medico_data['nombre'], 
                        medico_data['correo'], 
                        medico_data['especialidad']
                    )
                    self.agregar_medico(medico)
            self.console.print(f"[green]Se han cargado {len(self.medicos)} médicos.[/green]")
        except Exception as e:
            self.console.print(f"[red]Error al cargar médicos: {e}[/red]")

    def cargar_pacientes(self):
        try:
            with open(r"C:\Users\david\Desktop\Nueva carpeta\citas_medicas\datos\pacientes.csv", 'r', encoding='utf-8') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)  # Ignorar encabezado si existe
                for fila in lector_csv:
                    paciente = Paciente(
                        fila[0],  # ID
                        fila[1],  # Nombre
                        fila[2],  # Celular
                        fila[3]   # Correo
                    )
                    self.agregar_paciente(paciente)
            self.console.print(f"[green]Se han cargado {len(self.pacientes)} pacientes.[/green]")
        except Exception as e:
            self.console.print(f"[red]Error al cargar pacientes: {e}[/red]")

    def cargar_citas(self):
        try:
            with open(r"C:\Users\david\Desktop\Nueva carpeta\citas_medicas\datos\citas.csv", 'r', encoding='utf-8') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)  # Ignorar encabezado si existe
                for fila in lector_csv:
                    paciente = self.buscar_paciente(fila[1])  # ID del paciente
                    medico = self.buscar_medico(fila[2])  # ID del médico
                    if paciente and medico:
                        # Crear un objeto Cita con los datos
                        cita = Cita(
                            paciente,
                            medico,
                            fila[0]  # Fecha de la cita
                        )
                        self.citas.append(cita)  # Agregar la cita a la lista de citas del hospital
                        paciente.agenda.agregar_cita(cita)  # Agregar la cita a la agenda del paciente
                        medico.agenda.agregar_cita(cita)  # Agregar la cita a la agenda del médico
            self.console.print(f"[green]Se han cargado {len(self.citas)} citas.[/green]")
        except Exception as e:
            self.console.print(f"[red]Error al cargar citas: {e}[/red]")

    def agregar_paciente(self, paciente):
        self.pacientes.append(paciente)

    def agregar_medico(self, medico):
        self.medicos.append(medico)

    def buscar_paciente(self, identificacion):
        return next((p for p in self.pacientes if p.identificacion == identificacion), None)

    def buscar_medico(self, identificacion):
        return next((m for m in self.medicos if m.identificacion == identificacion), None)


