class Cita:
    def __init__(self, paciente, medico, fecha):
        self.paciente = paciente
        self.medico = medico
        self.fecha = fecha
        self.motivo_cancelacion = None

    def cancelar_cita(self):
        self.motivo_cancelacion = "Cancelada"
        print(f"La cita con el Dr. {self.medico.nombre} ha sido cancelada.")