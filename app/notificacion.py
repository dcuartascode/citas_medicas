class Notificacion:
    def enviar_notificacion(self, metodo, mensaje):
        metodo.enviar_notificacion(mensaje)

class WhatsApp(Notificacion):
    def enviar_notificacion(self, mensaje):
        print(f"Enviando mensaje de WhatsApp: {mensaje}")