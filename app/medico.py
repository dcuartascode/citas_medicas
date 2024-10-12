from persona import Persona
from agenda import Agenda
from cita import Cita

class Medico(Persona):
    def __init__(self, identificacion, nombre, celular, correo, especialidad):
        super().__init__(identificacion, nombre, celular, correo)
        self.especialidad = especialidad
        self.agenda = Agenda()

    def verificar_disponibilidad(self, fecha):
        return self.agenda.verificar_disponibilidad(fecha)

    def agendar_cita(self, paciente, fecha):
        if self.verificar_disponibilidad(fecha):
            cita = Cita(paciente, self, fecha)
            self.agenda.agregar_cita(cita)
            print(f"Cita agendada con el Dr. {self.nombre} para el paciente {paciente.nombre} en la fecha {fecha}.")
        else:
            print(f"No hay disponibilidad con el Dr. {self.nombre} en la fecha {fecha}")

    def cancelar_cita(self, cita):
        self.agenda.cancelar_cita(cita)
        print(f"Cita cancelada con el Dr. {self.nombre}.")