import network
import socket
import time
import ubinascii
import gc


def connect_to_wifi(ssid, password, max_retries=10):
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
        time.sleep(2)  # Esperar antes del próximo intento

    print()
    if wlan.isconnected():
        return wlan.ifconfig()
    else:
        return None


def ip_to_bytes(ip_string):
    """Convertir una dirección IP en formato string a una lista de bytes."""
    return [int(octet) for octet in ip_string.split(".")]


def bytes_to_ip(ip_bytes):
    """Convertir una lista de bytes a formato string IP."""
    return ".".join(str(b) for b in ip_bytes)


def calculate_broadcast(ip, mask):
    """Calcular la dirección de broadcast, necesaria para el descubrimiento de red."""
    ip_bytes = ip_to_bytes(ip)
    mask_bytes = ip_to_bytes(mask)
    broadcast_bytes = [(ip_bytes[i] | ~mask_bytes[i] & 0xFF) for i in range(4)]
    return bytes_to_ip(broadcast_bytes)


def configure_udp_socket():
    """Configurar un socket UDP para enviar un broadcast de descubrimiento de red."""
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return udp


def get_team_by_name(name):
    """Busca en el listado de equipos al que tiene el nombre dado."""
    for team in TEAMS:
        if team.name == name:
            return team
    return None


def discover_terminals(broadcast_ip, broadcast_port):
    """Enviar un mensaje de broadcast para descubrir a los controladores terminales."""
    udp = configure_udp_socket()
    udp.sendto(b"DISCOVER", (broadcast_ip, broadcast_port))

    terminals = []
    start_time = time.ticks_ms()  # Empezar el temporizador
    timeout_ms = 5000

    while time.ticks_diff(time.ticks_ms(), start_time) < timeout_ms:
        try:
            # Intentar leer 1024 bytes del socket UDP.
            response, addr = udp.recvfrom(1024)
            if response.startswith(b"TERMINAL"):
                _, team_name, port = response.decode().split(";")
                team = get_team_by_name(team_name)
                team.connect_to_terminal(addr[0], int(port))
                terminals.append((team, addr[0]))
                print(f"Terminal encontrado en {addr[0]}: {team}")
        except OSError:
            # Continuar si no hay mensajes disponibles
            pass

    if not terminals:
        print("No se encontraron dispositivos.")

    return terminals


class Team():
    def __init__(self, name):
        self.name = name

    def connect_to_terminal(self, terminal_ip, port):
        # Crear socket TCP
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Intentar conectarse al servidor TCP del terminal
        print(f"Conectando al terminal en {terminal_ip}:{port}...")
        self.tcp.connect((terminal_ip, port))

        # Enviar un mensaje al servidor TCP
        message = "Hola desde el maestro"
        self.tcp.send(message.encode())

        # Recibir la respuesta del servidor
        data = self.tcp.recv(1024)
        print(f"Respuesta del servidor: {data.decode()}")

        self.tcp.close()


TEAMS = [Team("TeoríaDelDescontrol"),
         Team("ClubTA"),
         Team("TeamISI"),
         Team("Colapintos"),
         Team("Brogramadores"),
         Team("LosOgata"),
         Team("MonteCarlo"),
         Team("Rompecircuitos"),
         Team("LosFachas")]

# Datos para conectarse a la red WiFi.
WLAN_SSID = "agus"
WLAN_PASSWORD = "agustinb"

# Datos para la interacción entre el maestro y los terminales.
BROADCAST_PORT = 10000


def monitoring():
    gc.collect()
    if_config = connect_to_wifi(WLAN_SSID, WLAN_PASSWORD)
    if if_config is None:
        print("Error al conectar a la red Wifi.")
        return None

    ip_address, subnet_mask, _, _ = if_config
    print(f"Conectado! IP: {ip_address}, Máscara de subred: {subnet_mask}")

    broadcast_ip = calculate_broadcast(ip_address, subnet_mask)
    print("Dirección de broadcast:", broadcast_ip)

    terminals = discover_terminals(broadcast_ip, BROADCAST_PORT)
    print("a", terminals)


monitoring()
