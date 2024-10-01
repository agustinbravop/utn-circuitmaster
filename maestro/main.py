import network
import socket
import time
import uasyncio as asyncio
import ubinascii


async def connect_to_wifi(ssid, password, max_retries=10):
    """Conecta el dispositivo a Wifi. Devuelve la dirección IP y la máscara de subred."""
    # Configurar el WiFi en modo cliente (station)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    mac_address = ubinascii.hexlify(network.WLAN().config("mac"), ":").decode()
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


def ip_to_bytes(ip_string: str):
    """Convertir una dirección IP en formato string a una lista de bytes."""
    return [int(octet) for octet in ip_string.split(".")]


def bytes_to_ip(ip_bytes: list[int]):
    """Convertir una lista de bytes a formato string IP."""
    return ".".join(str(b) for b in ip_bytes)


def calculate_broadcast(ip: str, mask: str):
    """Calcular la dirección de broadcast, necesaria para el descubrimiento de red."""
    ip_bytes = ip_to_bytes(ip)
    mask_bytes = ip_to_bytes(mask)
    broadcast_bytes = [(ip_bytes[i] | ~mask_bytes[i] & 0xFF) for i in range(4)]
    return bytes_to_ip(broadcast_bytes)


def get_terminal_by_name(name):
    """Buscar la terminal con el nombre de equipo dado."""
    for terminal in ALL_TERMINALS:
        if terminal.name == name:
            return terminal
    return None


async def discover_terminals(broadcast_ip, broadcast_port):
    """Enviar un mensaje de broadcast para descubrir a los controladores terminales. Para cada terminal encontrado devuelve su nombre, IP y puerto del servidor TCP."""
    # Crear un socket UDP
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Configurar el socket UDP para enviar un broadcast
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # No bloquear la ejecución si no hay mensajes
    udp.setblocking(False)

    udp.sendto(b"DISCOVER", (broadcast_ip, broadcast_port))

    # Configurar un temporizador con un timeout para el proceso de descubrimiento
    start_time = time.ticks_ms()
    timeout_ms = 5000
    found_terminals: list[tuple[Terminal, str, int]] = []

    while time.ticks_diff(time.ticks_ms(), start_time) < timeout_ms:
        try:
            # Intentar leer 1024 bytes del socket UDP
            response, addr = udp.recvfrom(1024)
            if response.startswith(b"TERMINAL"):
                _, terminal_name, port = response.decode().split(";")
                terminal = get_terminal_by_name(terminal_name)

                if terminal is None:
                    print("Error: nombre de terminal no conocido")
                    continue

                found_terminals.append((terminal, addr[0], int(port)))
                print(f"Encontrado a {terminal_name} en {addr[0]}:{port}")
        except OSError:
            # Ceder el control si no hay mensajes disponibles
            await asyncio.sleep(0.01)

    udp.close()
    return found_terminals


class Terminal():
    def __init__(self, name):
        self.name = name

    async def connect_to_terminal(self, ip, port):
        """Conectar (mediante `asyncio`) al server TCP del terminal."""
        self.reader, self.writer = await asyncio.open_connection(ip, port)
        print(f"Conectado a {self.name} en {ip}:{port}")

    async def get_data(self):
        """Solicitar datos al servidor TCP del terminal (polling)."""
        if not self.writer:
            # Terminal no conectado, no se puede monitorear
            return

        try:
            # Enviar petición al servidor
            message = "Hola desde el maestro"
            self.writer.write(message.encode())  # Acumula el mensaje al buffer
            await self.writer.drain()           # Envía el buffer al stream

            # Recibir la respuesta del servidor
            data = await self.reader.read(1024)
            print(f"Respuesta del servidor: {data.decode()}")
        except Exception as e:
            print(f"Error con {self.name}: {e}")

    async def close_connection(self):
        """Cerrar la conexión con el server TCP del dispositivo terminal."""
        self.writer.close()
        await self.writer.wait_closed()


async def poll_terminal_data(terminals: list[Terminal]):
    """Polling de datos a todos los terminales encontrados."""
    interval_seconds = 1
    while True:
        tasks = [terminal.get_data() for terminal in terminals]
        await asyncio.gather(*tasks)
        await asyncio.sleep(interval_seconds)

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

# Datos para conectarse a la red WiFi.
WLAN_SSID = "agus"
WLAN_PASSWORD = "agustinb"

# Datos para la interacción entre el maestro y los terminales.
BROADCAST_PORT = 10000


async def master_monitoring():
    if_config = await connect_to_wifi(WLAN_SSID, WLAN_PASSWORD)
    if if_config is None:
        print("Error al conectar a la red Wifi.")
        return None

    ip_address, subnet_mask, _, _ = if_config
    print(f"Conectado! IP: {ip_address}, Máscara de subred: {subnet_mask}")

    broadcast_ip = calculate_broadcast(ip_address, subnet_mask)
    print("Dirección de broadcast:", broadcast_ip)

    print("Descubrimiento terminales...")
    found_terminals = await discover_terminals(broadcast_ip, BROADCAST_PORT)
    terminals = [t[0] for t in found_terminals]
    print("Terminales descubiertas:", [t.name for t in terminals])

    # Conectar el maestro a cada terminal de manera concurrente
    async_tasks = []
    for terminal, ip, port in found_terminals:
        async_tasks.append(terminal.connect_to_terminal(ip, port))

    await asyncio.gather(*async_tasks)

    # Monitorear los terminales encontrados
    await poll_terminal_data(terminals)


asyncio.run(master_monitoring())
