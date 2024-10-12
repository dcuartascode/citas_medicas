from persona import Persona

class Paciente(Persona):
    def __init__(self, identificacion, nombre, celular, correo):
        super().__init__(identificacion, nombre, celular, correo)
        self.medico_preferencia = None

    def asignar_medico_preferencia(self, medico):
        self.medico_preferencia = medico
        print(f"El médico {medico.nombre} ha sido asignado como preferencia para el paciente {self.nombre}")

