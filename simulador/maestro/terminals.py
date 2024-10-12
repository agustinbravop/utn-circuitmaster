import asyncio
import json


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
        terminal_data["terminales_conectados"].append(self.name)
        print(f"Configurado {self.name} en {ip}:{port}")

    async def get_data(self):
        """Solicitar datos al servidor HTTP del terminal y los guarda en la variable global."""
        if not self.is_configured():
            # Terminal no conectado, no se puede monitorear
            return

        try:
            reader, writer = await asyncio.open_connection(self.ip, self.port)
        except OSError as e:
            print(f"Error al conectarse a {self.name}: {e}")
            self.forget_terminal()
            return

        try:
            request = "GET /data HTTP/1.1\r\nHost: {self.ip}\r\nConnection: close\r\n\r\n"
            writer.write(request.encode())
            await writer.drain()
        except OSError as e:
            print(f"Error al escribir a {self.name}: {e}")
            self.forget_terminal()
            writer.close()
            await writer.wait_closed()
            return

        try:
            response = await reader.read()
            writer.close()
            await writer.wait_closed()
        except OSError as e:
            print(f"Error en la solicitud a {self.name}: {e}")
            self.forget_terminal()
            writer.close()
            await writer.wait_closed()
            return

        # Extraer el cuerpo de la respuesta
        response = response.decode()
        body_start = response.find("\r\n\r\n") + 4
        data_json = response[body_start:]
        try:
            terminal_data[self.name] = json.loads(data_json)
            return
        except ValueError as e:
            print(f"JSON inválido con {self.name}: {e}, '{data_json}'")

        writer.close()
        await writer.wait_closed()

    def forget_terminal(self):
        """Borrar los datos del servidor HTTP del dispositivo terminal."""
        if not self.is_configured():
            # Ya está desconectado
            return

        self.ip = None
        self.port = None
        terminal_data["terminales_conectados"].remove(self.name)
        print(f"Desconfigurado {self.name}")


# Terminales a monitorear en la red (un terminal por cada equipo)
ALL_TERMINALS = [Terminal("TeoriaDelDescontrol"),
                 Terminal("ClubTA"),
                 Terminal("TeamISI"),
                 Terminal("Colapintos"),
                 Terminal("Brogramadores"),
                 Terminal("LosOgata"),
                 Terminal("MonteCarlo"),
                 Terminal("Rompecircuitos"),
                 Terminal("LosFachas")]

# Variable global con los datos recibidos de los terminales
# `terminles_conectados` es un arreglo de los nombres de equipos conectados.
terminal_data = {
    "terminales_conectados": []
}


def get_terminal_by_name(name: str):
    """Buscar el terminal con el nombre de equipo dado."""
    for terminal in ALL_TERMINALS:
        if terminal.name == name:
            return terminal
    return None


async def poll_terminal_data():
    """Polling de datos a todos los terminales encontrados y conectados."""
    while True:
        try:
            # De a tres para no saturar el límite de 5 conexiones TCP simultáneas
            await asyncio.gather(
                ALL_TERMINALS[0].get_data(),
                ALL_TERMINALS[1].get_data(),
                ALL_TERMINALS[2].get_data(),
            )
            await asyncio.gather(
                ALL_TERMINALS[3].get_data(),
                ALL_TERMINALS[4].get_data(),
                ALL_TERMINALS[5].get_data(),
            )
            await asyncio.gather(
                ALL_TERMINALS[6].get_data(),
                ALL_TERMINALS[7].get_data(),
                ALL_TERMINALS[8].get_data(),
            )
        except Exception as e:
            print(f"Error en el polling: {e}")
            pass
