import wifi
import socketpool
import time
import ipaddress

# Datos para conectarse a la red WiFi.
WLAN_SSID = 'agus'
WLAN_PASSWORD = 'agustinb'

# Puerto para la interacción entre los terminales y el maestro.
BROADCAST_PORT = 10000

# Conecta el dispositivo a la red WiFi. Devuelve la dirección IP y la máscara de subred.
def connect_to_wlan(ssid, password):
    print("Conectando a WLAN...", end="")
    try:
        wifi.radio.connect(ssid, password)
        print(" Terminal conectado!")
    except ConnectionError:
        print("Error de conexión. Verifique las credenciales.")
        return None, None

    mac_address = ':'.join([f'{b:02x}' for b in wifi.radio.mac_address])
    ip_address = wifi.radio.ipv4_address
    subnet_mask = wifi.radio.ipv4_subnet
    print(f"MAC: {mac_address}, IP: {ip_address}, Máscara de subred: {subnet_mask}")
    return ip_address, subnet_mask


# Configurar socket UDP para escuchar mensajes de descubrimiento
def configure_udp_socket(pool):
    udp = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
    udp.bind(('0.0.0.0', BROADCAST_PORT))  # Escuchar en todas las interfaces de red
    return udp


# Configurar socket TCP para aceptar conexiones del maestro
def configure_tcp_socket(pool, terminal_ip):
    tcp = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    tcp.bind((terminal_ip, 12345))  # Escuchar en el puerto 12345
    tcp.listen(1)
    return tcp


# Esperar mensaje de descubrimiento del maestro
def listen_for_discovery_messages(udp, tcp, terminal_ip, sensor_data):
    buffer = bytearray(1024)
    while True:
        udp.settimeout(0)  # No bloquear la ejecución si no hay mensajes
        try:
            # Recibir mensajes de descubrimiento (UDP)
            size, addr = udp.recvfrom_into(buffer)  # Solo recibe el mensaje, no la dirección
            msg = buffer[:size]
            if msg == b"DISCOVER":
                print("Mensaje de descubrimiento recibido")
                response = f"TERMINAL {terminal_ip}"
                print(addr)
                udp.sendto(response.encode(), addr)
                print('Respondido con IP:', terminal_ip)
        except OSError:
            pass  # No se recibió ningún mensaje, continuar

        tcp.settimeout(0)  # No bloquear la ejecución si no hay conexiones
        try:
            # Aceptar conexiones TCP del maestro
            cl, addr = tcp.accept()
            print('Conexión TCP establecida con el maestro desde:', addr)

            # Enviar datos de los sensores al maestro
            data_str = f"temperatura:{sensor_data['temperatura']},humedad:{sensor_data['humedad']}"
            cl.send(data_str.encode())

            # Cerrar la conexión con el maestro
            cl.close()
        except OSError:
            pass  # Sin conexiones entrantes, continuar


# Simulando datos de sensor
sensor_data = {
    'temperatura': 25.0,
    'humedad': 50.0
}

# Crear un pool de sockets y conectar a la red Wi-Fi
pool = socketpool.SocketPool(wifi.radio)
ip_address, _ = connect_to_wlan(WLAN_SSID, WLAN_PASSWORD)

# Configurar los sockets UDP y TCP
if ip_address:
    udp = configure_udp_socket(pool)
    tcp = configure_tcp_socket(pool, str(ip_address))
    print('Esperando mensajes de descubrimiento y conexiones del maestro...')
    listen_for_discovery_messages(udp, tcp, str(ip_address), sensor_data)

