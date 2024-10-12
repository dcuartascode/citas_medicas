class Agenda:
    def __init__(self):
        self.citas_pendientes = []

    def agregar_cita(self, cita):
        self.citas_pendientes.append(cita)

    def cancelar_cita(self, cita):
        if cita in self.citas_pendientes:
            self.citas_pendientes.remove(cita)
            print("Cita cancelada correctamente.")
        else:
            print("La cita no se encuentra en la agenda.")

    def verificar_disponibilidad(self, fecha):
        for cita in self.citas_pendientes:
            if cita.fecha == fecha:
                return False
        return True


