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


def configure_udp_broadcast_socket():
    """Configurar socket UDP para escuchar mensajes de descubrimiento."""
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Escuchar en todas las interfaces de red
    udp.bind(("0.0.0.0", BROADCAST_PORT))
    return udp


def configure_tcp_server_socket(port):
    """Configurar socket para un servidor TCP."""
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # `SO_REUSEADDR` permite hacer soft reboot del programa sin pisar el socket activo.
    # Ref: https://stackoverflow.com/questions/3229860/what-is-the-meaning-of-so-reuseaddr-setsockopt-option-linux
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp.bind(("", port))
    tcp.listen()
    return tcp


def listen_for_discovery_messages(team_name, port):
    """Esperar broadcast de descubrimiento del maestro."""
    udp = configure_udp_broadcast_socket()

    while True:
        # No bloquear la ejecución si no hay mensajes
        udp.setblocking(False)
        try:
            msg, addr = udp.recvfrom(1024)
            if msg == b"DISCOVER":
                print("Mensaje de descubrimiento recibido de:", addr)
                response = f"TERMINAL;{team_name};{port}"
                udp.sendto(response.encode(), addr)
                print("Respondido con: ", response)
                return
        except OSError:
            pass  # No se recibió ningún mensaje, continuar


def start_tcp_server(port):
    tcp = configure_tcp_server_socket(port)

    while True:
        conn, addr = tcp.accept()  # Aceptar conexión entrante
        print(f"Conexión TCP establecida con {addr}")

        # Recibir datos del maestro
        data = conn.recv(1024)
        print(f"Mensaje recibido: {data.decode()}")

        # Enviar una respuesta de vuelta
        response = "Datos recibidos en el terminal."
        conn.send(response.encode())

        conn.close()  # Cerrar la conexión


# Datos para conectarse a la red WiFi.
WLAN_SSID = "agus"
WLAN_PASSWORD = "agustinb"

# Datos para la interacción entre los terminales y el maestro.
BROADCAST_PORT = 10000
TCP_SERVER_PORT = 10001
TEAM_NAME = "Rompecircuitos"

# Simulando datos de sensor
sensor_data = {
    "temperatura": 25.0,
    "humedad": 50.0
}


def master_monitoring():
    gc.collect()
    if_config = connect_to_wifi(WLAN_SSID, WLAN_PASSWORD)
    if if_config is None:
        print("Error al conectar a la red Wifi.")
        return None

    terminal_ip, subnet_mask, _, _ = if_config
    print(f"Conectado! IP: {terminal_ip}, Máscara de subred: {subnet_mask}")

    print("Esperando mensajes de descubrimiento y conexiones del maestro...")
    listen_for_discovery_messages(TEAM_NAME, TCP_SERVER_PORT)
    start_tcp_server(TCP_SERVER_PORT)


master_monitoring()
