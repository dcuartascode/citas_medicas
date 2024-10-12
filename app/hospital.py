import json
import csv
from medico import Medico
from paciente import Paciente
from cita import Cita
from rich.console import Console

class Hospital:
    def __init__(self):
        self.console = Console()
        self.pacientes = []
        self.medicos = []
        self.citas = []
        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        self.cargar_medicos()
        self.cargar_pacientes()
        self.cargar_citas()

    def cargar_medicos(self):
        try:
            with open('medicos.json', 'r', encoding='utf-8') as archivo:
                medicos_json = json.load(archivo)
                for medico_data in medicos_json:
                    medico = Medico(
                        medico_data['id'], 
                        medico_data['nombre'], 
                        medico_data['celular'], 
                        medico_data['correo'],
                        medico_data['especialidad']
                    )
                    self.agregar_medico(medico)
            self.console.print(f"[green]Se han cargado {len(self.medicos)} médicos.[/green]")
        except Exception as e:
            self.console.print(f"[red]Error al cargar médicos: {e}[/red]")

    def cargar_pacientes(self):
        try:
            with open('pacientes.csv', 'r', encoding='utf-8') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv) 
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
            with open('citas.csv', 'r', encoding='utf-8') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)
                for fila in lector_csv:
                    paciente = self.buscar_paciente(fila[1])
                    medico = self.buscar_medico(fila[2])
                    if paciente and medico:
                        cita = Cita(paciente, medico, fila[0])
                        self.citas.append(cita)
                        medico.agenda.agregar_cita(cita)
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

    def buscar_medicos_por_especialidad(self, especialidad):
        return [m for m in self.medicos if m.especialidad == especialidad]

    def agendar_cita(self, paciente_id, especialidad, fecha):
        paciente = self.buscar_paciente(paciente_id)
        medicos = self.buscar_medicos_por_especialidad(especialidad)
        if not medicos:
            print(f"No hay médicos disponibles para la especialidad {especialidad}.")
            return
        
        for medico in medicos:
            if medico.verificar_disponibilidad(fecha):
                medico.agendar_cita(paciente, fecha)
                self.citas.append(Cita(paciente, medico, fecha))
                return
        print(f"No hay disponibilidad en la fecha {fecha}.")

    def cancelar_cita(self, paciente_id, fecha):
        paciente = self.buscar_paciente(paciente_id)
        cita = next((c for c in self.citas if c.paciente == paciente and c.fecha == fecha), None)
        if cita:
            cita.cancelar_cita()
            cita.medico.cancelar_cita(cita)
            self.citas.remove(cita)
        else:
            print("No se encontró la cita para cancelar.")

    def reprogramar_cita(self, paciente_id, fecha_actual, nueva_fecha):
        paciente = self.buscar_paciente(paciente_id)
        cita = next((c for c in self.citas if c.paciente == paciente and c.fecha == fecha_actual), None)
        if cita:
            if cita.medico.verificar_disponibilidad(nueva_fecha):
                cita.fecha = nueva_fecha
                print(f"Cita reprogramada para el {nueva_fecha}.")
            else:
                print("No hay disponibilidad en la nueva fecha.")
        else:
            print("No se encontró la cita para reprogramar.")



