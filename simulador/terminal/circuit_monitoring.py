import wifi
import socketpool
import time
import ipaddress

# Conecta el dispositivo a la red WiFi. Devuelve la dirección IP y la máscara de subred.
def connect_to_wlan(ssid, password):
    mac_address = ':'.join([f'{b:02x}' for b in wifi.radio.mac_address])
    print(f"MAC: {mac_address}")
    print("Conectando a WLAN...", end="")
    try:
        wifi.radio.connect(ssid, password)
        print(" Terminal conectado!")
    except ConnectionError:
        print("Error de conexión. Verifique las credenciales.")
        return None, None

    ip_address = wifi.radio.ipv4_address
    subnet_mask = wifi.radio.ipv4_subnet
    print(f"IP: {ip_address}, Máscara de subred: {subnet_mask}")
    return ip_address, subnet_mask


# Configurar socket UDP para escuchar mensajes de descubrimiento
def configure_udp_socket(pool):
    udp = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
    udp.bind(('0.0.0.0', BROADCAST_PORT))  # Escuchar en todas las interfaces de red
    return udp


# Conectar al socket TCP del maestro
def connect_to_master_tcp_socket(pool, master_address):
    tcp = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    tcp.connect(master_address)
    tcp.listen(1)
    return tcp


# Esperar mensaje de descubrimiento del maestro
def listen_for_discovery_messages(udp, pool, terminal_ip, sensor_data):
    buffer = bytearray(1024)
    while True:
        udp.settimeout(0)  # No bloquear la ejecución si no hay mensajes
        try:
            # Recibir mensajes de descubrimiento (UDP)
            size, addr = udp.recvfrom_into(buffer)  # Solo recibe el mensaje, no la dirección
            msg = buffer[:size]
            if msg == b"DISCOVER":
                print("Mensaje de descubrimiento recibido")
                response = f"TERMINAL TeoriaDelDescontrol"
                tcp = connect_to_master_tcp_socket(pool, addr)
                print(addr)
                tcp.sendto(response.encode(), addr)
                print('Respondido con IP:', terminal_ip)
        except OSError:
            pass  # No se recibió ningún mensaje, continuar
        

# Simulando datos de sensor
sensor_data = {
    'temperatura': 25.0,
    'humedad': 50.0
}

# Datos para conectarse a la red WiFi.
WLAN_SSID = 'agus'
WLAN_PASSWORD = 'agustinb'

# Puerto para la interacción entre los terminales y el maestro.
BROADCAST_PORT = 10000
TCP_PORT = 10001

# Crear un pool de sockets y conectar a la red Wi-Fi
pool = socketpool.SocketPool(wifi.radio)
ip_address, _ = connect_to_wlan(WLAN_SSID, WLAN_PASSWORD)

# Configurar los sockets UDP y TCP
if ip_address:
    udp = configure_udp_socket(pool)
    print('Esperando mensajes de descubrimiento y conexiones del maestro...')
    listen_for_discovery_messages(udp, pool, str(ip_address), sensor_data)

def operar():
    pass

def main():
    operar()

