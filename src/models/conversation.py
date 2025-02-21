class Conversation:
    def __init__(self):
        self.historial = []

    def add_interaction(self, ask, answer):
        self.historial.append({'pregunta': ask, 'respuesta': answer})

    def get_history(self):
        return self.historial

    def generate_message_for_model(self, initialContext):
        mensajes = [{"role": "system", "content": initialContext}]
        for interaccion in self.historial:
            mensajes.append({"role": "user", "content": interaccion['pregunta']})
            mensajes.append({"role": "assistant", "content": interaccion['respuesta']})
        return mensajes
