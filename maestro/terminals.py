import asyncio
import json


class Terminal():
    def __init__(self, name: str):
        self.name = name
        self.socket = None

    def is_connected(self):
        """Da `True` si el maestro está conectado al server TCP del terminal."""
        return self.socket is not None

    async def connect_to_terminal(self, pool, ip: str, port: int):
        """Conectar (mediante `asyncio`) al server TCP del terminal."""
        try:
            self.socket = pool.socket(
                pool.AF_INET, pool.SOCK_STREAM)
            self.socket.setsockopt(pool.SOL_SOCKET, pool.SO_REUSEADDR, 1)

            # Tiempo de espera para operaciones de socket
            self.socket.connect((ip, port))
            self.socket.setblocking(False)
            print(f"Conectado a {self.name} en {ip}:{port}")
            # Agregarlo al arreglo global de terminales conectados
            connected_terminals.append(self)
            print([t.name for t in connected_terminals])
        except OSError as e:
            print(f"Error al conectarse a {self.name}: {e}")
            self.socket = None

    async def get_data(self):
        """Solicitar datos al servidor TCP del terminal y los guarda en la variable global."""
        if not self.is_connected():
            # Terminal no conectado, no se puede monitorear
            return

        try:
            # Enviar petición al servidor
            message = "GETDATA"
            self.socket.send(message.encode())

            # Recibir la respuesta del servidor
            buffer = bytearray(4096)
            try:
                length = self.socket.recv_into(buffer)
            except OSError:
                # No hay mensaje disponible
                return

            data_json = buffer[:length].decode()

            if data_json == "":
                # Mensaje de desconexión
                await self.close_connection()
                return

            try:
                terminal_data[self.name] = json.loads(data_json)
            except ValueError as e:
                print(f"JSON inválido con {self.name}: {e}, '{data_json}'")
        except OSError as e:
            print(f"Error con {self.name}: {e}")
            await self.close_connection()

    async def close_connection(self):
        """Cerrar la conexión con el server TCP del dispositivo terminal."""
        if not self.is_connected():
            # Ya está desconectado
            return

        self.socket.close()
        self.socket = None
        print(f"Desconectado de {self.name}")
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
