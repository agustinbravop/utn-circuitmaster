import uasyncio as asyncio
import ujson as json


class Terminal():
    def __init__(self, name: str):
        self.name = name

    def is_connected(self):
        """Da `True` si el maestro está conectado al server TCP del terminal."""
        return self.writer is not None

    async def connect_to_terminal(self, ip: str, port: int):
        """Conectar (mediante `asyncio`) al server TCP del terminal."""
        self.reader, self.writer = await asyncio.open_connection(ip, port)
        print(f"Conectado a {self.name} en {ip}:{port}")
        # Agregarlo al arreglo global de terminales conectados
        connected_terminals.append(self)

    async def get_data(self):
        """Solicitar datos al servidor TCP del terminal y los guarda en la variable global."""
        if not self.is_connected():
            # Terminal no conectado, no se puede monitorear
            return

        try:
            # Enviar petición al servidor
            message = "GETDATA"
            self.writer.write(message.encode())  # Acumula el mensaje al buffer
            await self.writer.drain()           # Envía el buffer al stream

            # Recibir la respuesta del servidor
            data_json = await self.reader.read(8192)

            if data_json == b"":
                # Mensaje de desconexión
                await self.close_connection()
                return
            try:
                terminal_data[self.name] = json.loads(data_json)
            except ValueError as e:
                print(f"JSON inválido con {self.name}: {e}, {data_json}")
        except Exception as e:
            print(f"Error con {self.name}: {e}")
            await self.close_connection()

    async def close_connection(self):
        """Cerrar la conexión con el server TCP del dispositivo terminal."""
        if self.is_connected():
            self.writer.close()
            await self.writer.wait_closed()
            self.writer = None
            self.reader = None
            # Quitarlo de la lista global de terminales conectados
            if self in connected_terminals:
                connected_terminals.remove(self)
        print(f"Desconectado de {self.name}")


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

# Variable global con los datos recibidos de las terminales
terminal_data = {}


def get_terminal_by_name(name: str):
    """Buscar la terminal con el nombre de equipo dado."""
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
