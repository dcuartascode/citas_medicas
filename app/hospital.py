import csv
import json
import pprint

# Pretty printer para formato legible
pp = pprint.PrettyPrinter(indent=2)

# Definición de clases para Paciente y Medico
class Paciente:
    def __init__(self, nombre, identificacion, edad, genero, telefono):
        self.nombre = nombre
        self.identificacion = identificacion
        self.edad = edad
        self.genero = genero
        self.telefono = telefono

    def __repr__(self):
        return f'Paciente({self.nombre}, {self.identificacion}, {self.edad}, {self.genero}, {self.telefono})'


class Medico:
    def __init__(self, nombre, identificacion, especialidad):
        self.nombre = nombre
        self.identificacion = identificacion
        self.especialidad = especialidad

    def __repr__(self):
        return f'Medico({self.nombre}, {self.identificacion}, {self.especialidad})'


# Definición de la clase Hospital
class Hospital:
    def __init__(self):
        self.pacientes = []
        self.medicos = []

    def agregar_paciente(self, paciente):
        self.pacientes.append(paciente)

    def agregar_medico(self, medico):
        self.medicos.append(medico)

    def buscar_paciente(self, identificacion):
        return next((p for p in self.pacientes if p.identificacion == identificacion), None)

    def buscar_medico(self, identificacion):
        return next((m for m in self.medicos if m.identificacion == identificacion), None)


# Crear instancia del hospital
hospital = Hospital()

# Leer el archivo pacientes.csv y agregar los pacientes al hospital
with open("pacientes.csv", newline='', encoding='utf-8') as archivo_pacientes:
    fuente_pacientes = csv.reader(archivo_pacientes, delimiter=',')
    next(fuente_pacientes)  # Saltar la primera línea (encabezados)
    for linea in fuente_pacientes:
        if len(linea) == 5:  # Asegurarse de que la línea tiene 5 columnas
            nombre, identificacion, edad, genero, telefono = linea
            try:
                paciente = Paciente(nombre, identificacion, int(edad), genero, telefono)
                hospital.agregar_paciente(paciente)
            except ValueError as e:
                print(f"Error al convertir datos en la línea: {linea}. Error: {e}")
        else:
            print(f"Línea con formato incorrecto: {linea}")

# Leer el archivo medicos.json y agregar los médicos al hospital
with open('medicos.json', encoding='utf-8') as archivo_medicos:
    medicos_data = json.load(archivo_medicos)
    for medico_data in medicos_data:
        nombre = medico_data['nombre']
        identificacion = medico_data['identificacion']
        especialidad = medico_data['especialidad']
        medico = Medico(nombre, identificacion, especialidad)
        hospital.agregar_medico(medico)

# Verificar el contenido del hospital
print("Pacientes:")
pp.pprint(hospital.pacientes)

print("\nMedicos:")
pp.pprint(hospital.medicos)

# Ejemplo de búsqueda
print("\nBuscar Paciente con ID '12345':")
pp.pprint(hospital.buscar_paciente('12345'))

print("\nBuscar Medico con ID '98765':")
pp.pprint(hospital.buscar_medico('98765'))
