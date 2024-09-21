import network
import socket
import time
import ubinascii

# Datos para conectarse a la red WiFi.
WLAN_SSID = 'agus'
WLAN_PASSWORD = 'agustinb'

# Datos para la interacción entre el maestro y los terminales.
BROADCAST_PORT = 10000

# Conecta el dispositivo a la red WiFi. Devuelve la dirección IP y la máscara de subred.
def connect_to_wlan(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)    

    print("Conectando a WLAN...", end="")
    while not wlan.isconnected():
        print(".",end="")
        time.sleep(1)
        pass

    print(" Maestro conectado!")
    mac_address = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    ip_address, subnet_mask, _, _ = wlan.ifconfig()
    print(f"MAC: {mac_address}, IP: {ip_address}, Máscara de subred: {subnet_mask}")
    return (ip_address, subnet_mask)


# Convierte una dirección IP en formato string a una lista de bytes.
def ip_to_bytes(ip_string):
    return [int(octet) for octet in ip_string.split('.')]


# Convierte una lista de bytes a formato string IP.
def bytes_to_ip(ip_bytes):
    return '.'.join(str(b) for b in ip_bytes)


# Calcula la dirección de broadcast, necesaria para el descubrimiento de red.
def calculate_broadcast(ip, mask):
    ip_bytes = ip_to_bytes(ip)
    mask_bytes = ip_to_bytes(mask)
    broadcast_bytes = [(ip_bytes[i] | ~mask_bytes[i] & 0xFF) for i in range(4)]
    return bytes_to_ip(broadcast_bytes)


# Configura un socket UDP para enviar un broadcast de descubrimiento de red.
def configure_udp_socket():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return udp


# Envia un mensaje de broadcast para descubrir a los controladores terminales.
def discover_terminals(broadcast_ip, broadcast_port):
    udp = configure_udp_socket()
    udp.sendto(b'DISCOVER', (broadcast_ip, broadcast_port))

    terminals = []
    start_time = time.ticks_ms()	# Empezar el temporizador
    timeout = 5000  				# Timeout de 5 segundos (5000 ms)
    
    while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
        try:
            # Intentar leer 1024 bytes del socket UDP.
            response, addr = udp.recvfrom(1024)
            if response.startswith(b"TERMINAL"):
                terminal_ip = response.decode().split()[1]
                terminals.append(terminal_ip)
                print(f"Terminal encontrado en {addr[0]}: {terminal_ip}")
        except OSError:
            # Continuar si no hay mensajes disponibles
            pass

    if not terminals:
        print("No se encontraron dispositivos.")
    
    return terminals


# Conecta con cada terminal mediante TCP y obtiene los datos de los sensores.
def get_sensor_data(terminal_ip):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp.connect((terminal_ip, 12345))
        print(f'Conectado al terminal en {terminal_ip}')
        
        # Recibir datos del terminal
        data = tcp.recv(1024)
        print(f'Datos recibidos del terminal {terminal_ip}: {data.decode()}')
        
    except Exception as e:
        print(f'Error al conectar con {terminal_ip}: {e}')
    finally:
        tcp.close()


ip_address, subnet_mask = connect_to_wlan(WLAN_SSID, WLAN_PASSWORD)
broadcast_ip = calculate_broadcast(ip_address, subnet_mask)
terminals = discover_terminals(broadcast_ip, BROADCAST_PORT)
print('Dirección de broadcast:', broadcast_ip)

# Hacer polling a los terminales descubiertos
for terminal_ip in terminals:
    get_sensor_data(terminal_ip)
