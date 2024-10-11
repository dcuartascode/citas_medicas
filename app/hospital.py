import json
import csv
with open(r"C:\Users\david\Desktop\Nueva carpeta\citas_medicas\app\medicos.json", 'r') as archivo:
    medicos_json = json.load(archivo)
    
with open(r"C:\Users\david\Desktop\Nueva carpeta\citas_medicas\app\pacientes.csv", 'r') as archivo:
    pacientes_csv = csv.reader(archivo)

with open(r"C:\Users\david\Desktop\Nueva carpeta\citas_medicas\app\citas.csv", 'r') as archivo:
    citas_csv = csv.reader(archivo)

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