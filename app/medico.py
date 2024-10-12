from agenda import Agenda
from persona import Persona

class Medico(Persona):
    def __init__(self, identificacion, nombre, celular, especialidad):
        super().__init__(identificacion, nombre, celular)  # Llama al constructor de Persona
        self.especialidad = especialidad
        self.agenda = Agenda()

    def verificar_disponibilidad(self, fecha):
        return self.agenda.verificar_disponibilidad(fecha)

    def agregar_cita(self, cita):
        self.agenda.agregar_cita(cita)

    def cancelar_cita(self, cita):
        self.agenda.cancelar_cita(cita)


