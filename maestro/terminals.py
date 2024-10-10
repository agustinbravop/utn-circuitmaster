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

    def configure_terminal(self, ip: str, port: int):
        """Conectar (mediante `asyncio`) al server TCP del terminal."""
        self.ip = ip
        self.port = port
        print(f"Configurado {self.name} en {ip}:{port}")
        # Agregarlo al arreglo global de terminales conectados
        connected_terminals.append(self)

    def get_data(self):
        """Solicitar datos al servidor HTTP del terminal y los guarda en la variable global."""
        if not self.is_configured():
            # Terminal no conectado, no se puede monitorear
            return

        addr_info = socket.getaddrinfo(self.ip, self.port)
        addr = addr_info[0][-1]
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.settimeout(0.2)

        try:
            client_socket.connect(addr)

            request = "GET /data HTTP/1.1\r\nHost: {self.ip}\r\nConnection: close\r\n\r\n"
            client_socket.send(request.encode())

            response = client_socket.recv(4096)

            client_socket.close()

            # Extraer el cuerpo de la respuesta
            response = response.decode()
            body_start = response.find("\r\n\r\n") + 4
            data_json = response[body_start:]
            try:
                terminal_data[self.name] = json.loads(data_json)
            except ValueError as e:
                print(f"JSON inválido con {self.name}: {e}, '{data_json}'")
        except OSError as e:
            print(f"Error en la solicitud al terminal: {e}")
            client_socket.close()
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
    interval_seconds = 0.3
    while True:
        for terminal in connected_terminals:
            terminal.get_data()
        await asyncio.sleep(interval_seconds)