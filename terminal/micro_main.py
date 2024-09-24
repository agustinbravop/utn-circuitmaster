import network
import socket
import time
import ubinascii

# Datos para conectarse a la red WiFi.
WLAN_SSID = 'agus'
WLAN_PASSWORD = 'agustinb'

# Datos para la interacción entre los terminales y el maestro.
BROADCAST_PORT = 10000

# Conecta el dispositivo a la red WiFi. Devuelve la dirección IP y la máscara de subred.


def connect_to_wlan(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Conectando a WLAN...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
        pass

    print(" Terminal conectado!")
    mac_address = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    ip_address, subnet_mask, _, _ = wlan.ifconfig()
    print(f"MAC: {mac_address}, IP: {
          ip_address}, Máscara de subred: {subnet_mask}")
    return (ip_address, subnet_mask)


# Configurar socket UDP para escuchar mensajes de descubrimiento
def configure_udp_socket():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Escuchar en todas las interfaces de red
    udp.bind(('0.0.0.0', BROADCAST_PORT))
    return udp


# Configurar socket TCP para aceptar conexiones del maestro
def configure_tcp_socket(terminal_ip):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind((terminal_ip, 12345))  # Escuchar en el puerto 12345
    tcp.listen(1)
    return tcp


# Esperar mensaje de descubrimiento del maestro
def listen_for_discovery_messages(udp, tcp, terminal_ip, sensor_data):
    while True:
        udp.setblocking(False)  # No bloquear la ejecución si no hay mensajes
        try:
            msg, addr = udp.recvfrom(1024)
            if msg == b'DISCOVER':
                print('Mensaje de descubrimiento recibido de:', addr)
                response = f'TERMINAL {terminal_ip}'
                udp.sendto(response.encode(), addr)
                print('Respondido con IP:', terminal_ip)
        except OSError:
            pass  # No se recibió ningún mensaje, continuar

        # Aceptar conexiones TCP del maestro
        tcp.setblocking(False)  # No bloquear la ejecución si no hay conexiones
        try:
            cl, addr = tcp.accept()
            print('Conexión TCP establecida con el maestro desde:', addr)

            # Enviar datos de los sensores al maestro
            data_str = f"temperatura:{sensor_data['temperatura']},humedad:{
                sensor_data['humedad']}"
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

ip_address, _ = connect_to_wlan(WLAN_SSID, WLAN_PASSWORD)
udp = configure_udp_socket()
tcp = configure_tcp_socket(ip_address)
print('Esperando mensajes de descubrimiento y conexiones del maestro...')
listen_for_discovery_messages(udp, tcp, ip_address, sensor_data)
