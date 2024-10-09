class Agenda:
    def __init__(self):
        self.citas_pendientes = []

    def agregar_cita(self, cita):
        self.citas_pendientes.append(cita)
        print(f"Cita agregada para el {cita.fecha} con el Dr. {cita.medico.nombre}")

    def verificar_disponibilidad(self, fecha):
        return fecha not in [cita.fecha for cita in self.citas_pendientes]