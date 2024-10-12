class Notificacion:
    def enviar_notificacion(self, metodo, mensaje):
        metodo.enviar_notificacion(mensaje)

class Correo(Notificacion):
    def enviar_notificacion(self, mensaje):
        print(f"Enviando correo: {mensaje}")

class Celular(Notificacion):
    def enviar_notificacion(self, mensaje):
        print(f"Enviando mensaje de texto: {mensaje}")

class Aplicacion(Notificacion):
    def enviar_notificacion(self, mensaje):
        print(f"Enviando notificación en la aplicación: {mensaje}")

class WhatsApp(Notificacion):
    def enviar_notificacion(self, mensaje):
        print(f"Enviando mensaje de WhatsApp: {mensaje}")