# import network
import socket
import asyncio
import binascii
import json
import sys
import psutil


async def connect_to_wifi(ssid: str, password: str, max_retries=5):
    """Conecta el dispositivo a Wifi. Devuelve la dirección IP y la máscara de subred."""
    # Configurar el WiFi en modo cliente (station)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    mac_address = binascii.hexlify(
        network.WLAN().config("mac"), ":").decode()
    print(f"MAC: {mac_address}")

    retries = 0
    print(f"Conectando a WiFi...")
    while not wlan.isconnected() and retries < max_retries:
        wlan.connect(ssid, password)
        retries += 1
        await asyncio.sleep(1)  # Esperar antes del próximo intento

    if wlan.isconnected():
        return wlan.ifconfig()
    else:
        return None


async def listen_for_discovery_messages(team_name: str, broadcast_port: int, http_port: int):
    """Esperar broadcast de descubrimiento del maestro."""
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Habilitar la opción SO_REUSEADDR para permitir reuso del puerto
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Escuchar en todas las interfaces de red
    udp.bind(("0.0.0.0", broadcast_port))
    # No bloquear la ejecución si no hay mensajes
    udp.setblocking(False)

    while True:
        try:
            msg, addr = udp.recvfrom(1024)
            if msg == b"DISCOVER":
                print("Mensaje de descubrimiento recibido de:", addr)
                response = f"TERMINAL;{team_name};{http_port}"
                udp.sendto(response.encode(), addr)

        except OSError:
            await asyncio.sleep(1)  # Ceder control si no hay mensajes

        await master_disconnected.wait()


async def start_http_server(port: int, get_app_data):
    """Iniciar un servidor HTTP para que el maestro pueda conectarse."""
    handler = await create_handler(get_app_data)
    server = await asyncio.start_server(handler, "0.0.0.0", port)
    await server.wait_closed()


async def create_handler(get_app_data):
    """Construye un handler HTTP que también puede obtener datos del terminal."""

    async def handle_client(reader, writer):
        """Manejar la conexión con el maestro de forma asincrónica."""
        new_request_recieved.set()
        master_disconnected.clear()

        try:
            request = await reader.read(1024)
            request_str = request.decode().strip()

            if "GET" in request_str:
                # Enviar la data del terminal
                json_data = json.dumps(get_app_data())
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {
                    len(json_data)}\r\n\r\n{json_data}"
                writer.write(response.encode())
                await writer.drain()
        except OSError as e:
            print(f"Error en la conexión: {e}")
            master_disconnected.set()
        finally:
            writer.close()
            await writer.wait_closed()

    return handle_client


async def check_master_connection():
    """Reinicia el descubrimiento del maestro si sucede un timeout en el servidor HTTP."""
    timeout_seconds = 5
    while True:
        # Si `new_request_recieved` no fue seteado por el HTTP handler, desconectar al maestro
        if not master_disconnected.is_set() and not new_request_recieved.is_set():
            print("Maestro desconectado. Volviendo a esperar broadcasts...")
            master_disconnected.set()
        new_request_recieved.clear()
        await asyncio.sleep(timeout_seconds)

# Datos para conectarse a la red WiFi.
# WLAN_SSID = sys.argv[1]
# WLAN_PASSWORD = sys.argv[2]

# Datos para la interacción entre los terminales y el maestro.
BROADCAST_PORT = int(sys.argv[1])
HTTP_SERVER_PORT = int(sys.argv[2])
TEAM_NAME = sys.argv[3]
print(sys.argv)

# Indica si el maestro está conectado. Si no lo está, se vuelve al descubrimiento
master_disconnected = asyncio.Event()
master_disconnected.set()  # Inicialmente el maestro está desconectado

# Indica si el maestro hizo una petición HTTP recientemente.
new_request_recieved = asyncio.Event()


async def monitoring(get_app_data):
    """Monitoreo asincrónico con el controlador maestro.
    `get_app_data` es una función llamada en cada poll. Debe retornar el `dict` a enviar al maestro."""
    print(f"Controlador {TEAM_NAME}")

    # if_config = await connect_to_wifi(WLAN_SSID, WLAN_PASSWORD)
    # if if_config is None:
    #     print("Error al conectar a la red Wifi.")
    #     return None

    # terminal_ip, subnet_mask, _, _ = if_config

    terminal_ip, subnet_mask = None, None
    addresses = psutil.net_if_addrs()
    if "Wi-Fi" in addresses:
        for addr in addresses["Wi-Fi"]:
            if addr.family == socket.AF_INET:
                ip_address = addr.address
                subnet_mask = addr.netmask

    if ip_address is None:
        print("Error al conectar a la red Wifi.")
        return

    print(f"Conectado! IP: {terminal_ip}, Máscara de subred: {subnet_mask}")

    print("Esperando mensajes de descubrimiento del maestro...")
    await asyncio.gather(
        listen_for_discovery_messages(
            TEAM_NAME, BROADCAST_PORT, HTTP_SERVER_PORT),
        start_http_server(HTTP_SERVER_PORT, get_app_data),
        check_master_connection()
    )
