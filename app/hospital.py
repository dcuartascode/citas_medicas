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
        self.cargar_medicos()
        self.cargar_pacientes()
        self.cargar_citas()

    def cargar_medicos(self):
        try:
            with open(r"C:\Users\david\Desktop\Nueva carpeta\citas_medicas\datos\medicos.json", encoding='utf-8') as archivo:
                medicos_json = json.load(archivo)
                for medico_data in medicos_json:
                    if all(key in medico_data for key in ['id', 'nombre', 'celular', 'especialidad']):
                        medico = Medico(
                            medico_data['id'], 
                            medico_data['nombre'], 
                            medico_data['celular'], 
                            medico_data['especialidad']
                        )
                        self.medicos.append(medico)
                self.console.print(f"[green]Se han cargado {len(self.medicos)} médicos.[/green]")
        except FileNotFoundError:
            self.console.print("[red]El archivo medicos.json no fue encontrado.[/red]")
        except json.JSONDecodeError:
            self.console.print("[red]Error al parsear el archivo JSON. Verifique el formato del archivo.[/red]")
        except Exception as e:
            self.console.print(f"[red]Error inesperado al cargar médicos: {e}[/red]")

    def cargar_pacientes(self):
        try:
            with open(r"C:\Users\david\Desktop\Nueva carpeta\citas_medicas\datos\pacientes.csv", encoding='utf-8') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)  # Ignora el encabezado
                for fila in lector_csv:
                    paciente = Paciente(
                        fila[0],  # ID
                        fila[1],  # Nombre
                        fila[2],  # Celular
                        fila[3]   # Correo
                    )
                    self.agregar_paciente(paciente)
            self.console.print(f"[green]Se han cargado {len(self.pacientes)} pacientes.[/green]")
        except FileNotFoundError:
            self.console.print("[red]El archivo pacientes.csv no fue encontrado.[/red]")
        except Exception as e:
            self.console.print(f"[red]Error inesperado al cargar pacientes: {e}[/red]")

    def cargar_citas(self):
        try:
            with open(r"C:\Users\david\Desktop\Nueva carpeta\citas_medicas\datos\citas.csv", encoding='utf-8') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)  # Ignora el encabezado
                for fila in lector_csv:
                    paciente = self.buscar_paciente(fila[1])  # ID del paciente
                    medico = self.buscar_medico(fila[2])  # ID del médico
                    if paciente and medico:
                        cita = Cita(
                            paciente,
                            medico,
                            fila[0]  # Fecha de la cita
                        )
                        self.citas.append(cita) 
                        medico.agregar_cita(cita)  # Agregar a la agenda del médico
            self.console.print(f"[green]Se han cargado {len(self.citas)} citas.[/green]")
        except FileNotFoundError:
            self.console.print("[red]El archivo citas.csv no fue encontrado.[/red]")
        except Exception as e:
            self.console.print(f"[red]Error inesperado al cargar citas: {e}[/red]")

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

    def cancelar_cita(self, id_paciente, fecha_cita):
        paciente = self.buscar_paciente(id_paciente)
        if not paciente:
            self.console.print(f"[red]Paciente con identificación {id_paciente} no encontrado.[/red]")
            return False
        
        # Buscar la cita en las citas pendientes del paciente
        cita_a_cancelar = None
        for cita in self.citas:
            if cita.paciente == paciente and cita.fecha == fecha_cita:
                cita_a_cancelar = cita
                break

        if not cita_a_cancelar:
            self.console.print(f"[red]No se encontró una cita para el paciente {paciente.nombre} en la fecha {fecha_cita}.[/red]")
            return False

        # Cancelar la cita en la agenda del médico
        cita_a_cancelar.medico.cancelar_cita(cita_a_cancelar)
        
        # Remover la cita del listado de citas del hospital
        self.citas.remove(cita_a_cancelar)
        self.console.print(f"[green]La cita del paciente {paciente.nombre} con el Dr. {cita_a_cancelar.medico.nombre} para el {fecha_cita} ha sido cancelada.[/green]")
        return True

    # Mejora propia
    def reagendar_cita(self, id_paciente, fecha_actual, nueva_fecha):
        paciente = self.buscar_paciente(id_paciente)
        if not paciente:
            self.console.print(f"[red]Paciente con identificación {id_paciente} no encontrado.[/red]")
            return False
        cita_a_reagendar = None
        for cita in self.citas:
            if cita.paciente == paciente and cita.fecha == fecha_actual:
                cita_a_reagendar = cita
                break

        if not cita_a_reagendar:
            self.console.print(f"[red]No se encontró una cita para el paciente {paciente.nombre} en la fecha {fecha_actual}.[/red]")
            return False
        
        if cita_a_reagendar.medico.verificar_disponibilidad(nueva_fecha):
            cita_a_reagendar.fecha = nueva_fecha
            self.console.print(f"[green]La cita del paciente {paciente.nombre} ha sido reagendada a {nueva_fecha} con el Dr. {cita_a_reagendar.medico.nombre}.[/green]")
            return True
        else:
            self.console.print(f"[red]El médico {cita_a_reagendar.medico.nombre} no tiene disponibilidad en la nueva fecha {nueva_fecha}.[/red]")
            return False

    # Mejora propia
    def actualizar_paciente(self, id_paciente, nuevo_nombre=None, nuevo_celular=None, nuevo_correo=None):
        paciente = self.buscar_paciente(id_paciente)
        if paciente:
            if nuevo_nombre:
                paciente.nombre = nuevo_nombre
            if nuevo_celular:
                paciente.celular = nuevo_celular
            if nuevo_correo:
                paciente.correo = nuevo_correo
            self.console.print(f"[green]Información del paciente {paciente.identificacion} actualizada exitosamente.[/green]")
        else:
            self.console.print(f"[red]Paciente con identificación {id_paciente} no encontrado.[/red]")

    def actualizar_medico(self, id_medico, nuevo_nombre=None, nuevo_celular=None, nueva_especialidad=None):
        medico = self.buscar_medico(id_medico)
        if medico:
            if nuevo_nombre:
                medico.nombre = nuevo_nombre
            if nuevo_celular:
                medico.celular = nuevo_celular
            if nueva_especialidad:
                medico.especialidad = nueva_especialidad
            self.console.print(f"[green]Información del médico {medico.identificacion} actualizada exitosamente.[/green]")
        else:
            self.console.print(f"[red]Médico con identificación {id_medico} no encontrado.[/red]")
