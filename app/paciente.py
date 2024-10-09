from agenda import Agenda
from cita import Cita

class Paciente(Persona):
    def __init__(self, identificacion, nombre, celular, correo):
        super().__init__(identificacion, nombre, celular)
        self.correo = correo
        self.medico_preferencia = None
        self.agenda = Agenda()

    def asignar_medico_preferencia(self, medico):
        self.medico_preferencia = medico
        print(f"El médico {medico.nombre} ha sido asignado como preferencia para el paciente {self.nombre}")

    def pedir_cita(self, medico, fecha, motivo):
        if medico.verificar_disponibilidad(fecha):
            nueva_cita = Cita(self, medico, fecha)
            medico.agenda.agregar_cita(nueva_cita)
            self.agenda.agregar_cita(nueva_cita)
            print(f"Cita solicitada para el {fecha} con el Dr. {medico.nombre}")
        else:
            print(f"No hay disponibilidad con el Dr. {medico.nombre} en la fecha {fecha}")

    def cancelar_cita(self, cita):
        cita.cancelar_cita()
        print(f"Cita cancelada por el paciente {self.nombre}")