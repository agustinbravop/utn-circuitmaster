import uasyncio as asyncio
import ujson as json
import socket


class Terminal():
    def __init__(self, name: str):
        self.name = name
        self.ip = None
        self.port = None

    def is_configured(self):
        """Da `True` si el maestro tiene los datos del servidor HTTP del terminal."""
        return self.ip is not None and self.port is not None

    async def configure_terminal(self, ip: str, port: int):
        """Conectar (mediante `asyncio`) al server TCP del terminal."""
        self.ip = ip
        self.port = port
        print(f"Configurado {self.name} en {ip}:{port}")
        # Agregarlo al arreglo global de terminales conectados
        connected_terminals.append(self)

    async def get_data(self):
        """Solicitar datos al servidor HTTP del terminal y los guarda en la variable global."""
        if not self.is_configured():
            # Terminal no conectado, no se puede monitorear
            return

        # Enviar petición al servidor
        request = "GET /data HTTP/1.1\r\nHost: {self.ip}\r\nConnection: close\r\n\r\n"
        reader, writer = await asyncio.open_connection(self.ip, self.port)

        try:
            writer.write(request.encode())  # Acumula el mensaje al buffer
            await writer.drain()            # Envía el buffer al stream

            data_json = await reader.read(4096)

            # Cerrar la conexión
            writer.close()
            await writer.wait_closed()

            # Extraer el cuerpo de la respuesta
            response = response.decode()
            body_start = response.find("\r\n\r\n") + 4
            response[body_start:]
            try:
                terminal_data[self.name] = json.loads(data_json)
            except ValueError as e:
                print(f"JSON inválido con {self.name}: {e}, '{data_json}'")
        except OSError as e:
            print(f"Error en la solicitud HTTP: {e}")
            writer.close()
            await writer.wait_closed()
            self.forget_terminal()
            return None

    def forget_terminal(self):
        """Borrar los datos del servidor HTTP del dispositivo terminal."""
        if not self.is_configured():
            # Ya está desconectado
            return

        self.ip = None
        self.port = None
        print(f"Desconfigurado {self.name}")
        # Quitarlo de la lista global de terminales conectados
        if self in connected_terminals:
            connected_terminals.remove(self)


# Terminales a monitorear en la red (un terminal por cada equipo)
ALL_TERMINALS = [Terminal("TeoríaDelDescontrol"),
                 Terminal("ClubTA"),
                 Terminal("TeamISI"),
                 Terminal("Colapintos"),
                 Terminal("Brogramadores"),
                 Terminal("LosOgata"),
                 Terminal("MonteCarlo"),
                 Terminal("Rompecircuitos"),
                 Terminal("LosFachas")]

# Variable global con los terminales actualmente conectados.
# TODO: validar si funciona bien con varios terminales
connected_terminals: list[Terminal] = []

# Variable global con los datos recibidos de los terminales
terminal_data = {}


def get_terminal_by_name(name: str):
    """Buscar el terminal con el nombre de equipo dado."""
    for terminal in ALL_TERMINALS:
        if terminal.name == name:
            return terminal
    return None


async def poll_terminal_data():
    """Polling de datos a todos los terminales encontrados y conectados."""
    interval_seconds = 1
    while True:
        tasks = [terminal.get_data() for terminal in connected_terminals]
        await asyncio.gather(*tasks)
        await asyncio.sleep(interval_seconds)
