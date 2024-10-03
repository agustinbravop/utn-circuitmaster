import network
import socket
import time
import uasyncio as asyncio
import ubinascii as binascii
import ujson as json


async def connect_to_wifi(ssid: str, password: str, max_retries=5):
    """Conecta el dispositivo a Wifi. Devuelve la dirección IP y la máscara de subred."""
    # Configurar el WiFi en modo cliente (station)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    mac_address = binascii.hexlify(
        network.WLAN().config("mac"), ":").decode()
    print(f"MAC: {mac_address}")

    retries = 0
    print(f"Conectando a WiFi...", end="")
    while not wlan.isconnected() and retries < max_retries:
        print(".", end="")
        wlan.connect(ssid, password)
        retries += 1
        await asyncio.sleep(2)  # Esperar antes del próximo intento

    print()  # Termina la cadena de puntos suspensivos
    if wlan.isconnected():
        return wlan.ifconfig()
    else:
        return None


def calculate_broadcast(ip: str, mask: str):
    """Calcular la dirección de broadcast, necesaria para el descubrimiento de red."""
    ip_bytes = ip_to_bytes(ip)
    mask_bytes = ip_to_bytes(mask)
    broadcast_bytes = [(ip_bytes[i] | ~mask_bytes[i] & 0xFF) for i in range(4)]
    return bytes_to_ip(broadcast_bytes)


def ip_to_bytes(ip_string: str):
    """Convertir una dirección IP en formato string a una lista de bytes."""
    return [int(octet) for octet in ip_string.split(".")]


def bytes_to_ip(ip_bytes: list[int]):
    """Convertir una lista de bytes a formato string IP."""
    return ".".join(str(b) for b in ip_bytes)


async def discover_terminals(broadcast_ip: str, broadcast_port: int):
    """Enviar un mensaje de broadcast para descubrir a los controladores terminales."""
    # Crear un socket UDP
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Configurar el socket UDP para enviar un broadcast
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # No bloquear la ejecución si no hay mensajes
    udp.setblocking(False)

    # Configurar un temporizador con un timeout para el proceso de descubrimiento
    start_time = time.ticks_ms()
    timeout_ms = 8000

    print("Descubrimiento terminales...")
    while time.ticks_diff(time.ticks_ms(), start_time) < timeout_ms:
        try:
            udp.sendto(b"DISCOVER", (broadcast_ip, broadcast_port))

            # Intentar leer 1024 bytes del socket UDP
            response, addr = udp.recvfrom(1024)
            if response.startswith(b"TERMINAL"):
                _, terminal_name, port = response.decode().split(";")
                terminal = get_terminal_by_name(terminal_name)

                if terminal is None:
                    print("Error: nombre de terminal no conocido")
                    continue

                print(f"Encontrado a {terminal_name} en {addr[0]}:{port}")
                # TODO: conectar concurrentemente los varios terminales descubiertos.
                await terminal.connect_to_terminal(addr[0], int(port))
        except OSError:
            await asyncio.sleep(0.1)

    udp.close()
    print(f"Terminales descubiertos y conectados: {connected_terminals}")


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


async def run_http_server(ip: str, port: int):
    """Server HTTP para el monitoreo mediante un dashboard web."""
    server = await asyncio.start_server(handle_http_request, ip, port)
    print(f"Servidor HTTP escuchando en {ip}:{port}")
    await server.wait_closed()


async def handle_http_request(reader, writer):
    """Atender una petición HTTP."""
    try:
        while True:
            request = await reader.read(1024)

            if request == b"":
                # Mensaje de desconexión
                break

            request = request.decode().split("\r\n")

            # Obtener el header "Connection" si existe
            connection_type = "close"
            for header in request:
                if header.lower().startswith("connection:"):
                    connection_type = header.split(":")[1].strip().lower()

            response = request_router(request)

            if connection_type == "keep-alive":
                # Agregar encabezado Connection si el browser solicitó 'keep-alive'
                response.replace(
                    b"\r\n\r\n", "\r\nConnection: keep-alive\r\n\r\n".encode(), 1)

            writer.write(response)
            await writer.drain()

            if connection_type != "keep-alive":
                # Cerrar la conexión si no se especificó 'keep-alive'
                break
    except OSError as e:
        print(f"Error en el servidor HTTP: {e}")
    finally:
        writer.close()
        await writer.wait_closed()


def request_router(request):
    """Asocia un handler al método y path de la petición HTTP."""
    method, path, _ = request[0].split(" ")

    if method != "GET":
        return "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n".encode()

    if path == "/":
        return serve_file("/www/index.html", "text/html")
    elif path.endswith(".html"):
        return serve_file(f"/www{path}", "text/html")
    elif path.endswith(".css"):
        return serve_file(f"/www{path}", "text/css")
    elif path.endswith(".js"):
        return serve_file(
            f"/www{path}", "application/javascript")
    elif path == "/data":
        return serve_data()
    else:
        return "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n".encode()


def serve_file(path: str, content_type: str):
    """Responder con los archivos HTML, CSS o JS del servidor."""
    try:
        with open(path, "r") as file:
            content = file.read()

        response = "HTTP/1.1 200 OK\r\n" + \
            f"Content-Type: {content_type}\r\n" + \
            f"Content-Length: {len(content)}\r\n" + \
            "\r\n" + \
            f"{content}"""

        return response.encode()
    except OSError:
        return "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n".encode()


def serve_data():
    """Responder con la data (en JSON) más reciente de los terminales."""
    json_data = json.dumps(terminal_data)
    response = "HTTP/1.1 200 OK\r\n" + \
        "Content-Type: application/json\r\n" + \
        f"Content-Length: {len(json_data)}\r\n" + \
        "\r\n" + \
        f"{json_data}"""

    return response.encode()


# Datos para conectarse a la red WiFi.
WLAN_SSID = "agus"
WLAN_PASSWORD = "agustinb"

# Datos para las interfaces del maestro.
BROADCAST_PORT = 10000
HTTP_SERVER_PORT = 80

# Terminales a monitorear en la red (un terminal por cada equipo).
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
# TODO: validar si funciona bien con varios terminales.
connected_terminals: list[Terminal] = []

# Variable global con los datos recibidos de las terminales.
terminal_data = {}


async def master_monitoring():
    print("Controlador maestro")

    if_config = await connect_to_wifi(WLAN_SSID, WLAN_PASSWORD)
    if if_config is None:
        print("Error al conectar a la red Wifi.")
        return None

    ip_address, subnet_mask, _, _ = if_config
    print(f"Conectado! IP: {ip_address}, Máscara de subred: {subnet_mask}")

    broadcast_ip = calculate_broadcast(ip_address, subnet_mask)
    print("Dirección de broadcast:", broadcast_ip)

    await asyncio.gather(
        discover_terminals(broadcast_ip, BROADCAST_PORT),
        poll_terminal_data(),
        run_http_server(ip_address, HTTP_SERVER_PORT)
    )

asyncio.run(master_monitoring())
