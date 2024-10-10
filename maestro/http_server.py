from terminals import terminal_data
import uasyncio as asyncio
import ujson as json
import socket


async def run_http_server(ip: str, port: int):
    """Server HTTP para el monitoreo mediante un dashboard web."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(False)
    server_socket.bind((ip, port))
    server_socket.listen()

    print(f"Servidor HTTP escuchando en {ip}:{port}")
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            client_socket.settimeout(3)
            print(f"Conexión del dashboard web en: {client_address}")
            # Manejar la solicitud HTTP
            handle_http_request(client_socket)
            # Cerrar la conexión
            client_socket.close()
        except:
            # No hay conexiones disponibles
            await asyncio.sleep(0.3)


def handle_http_request(client_socket):
    """Atender una petición HTTP del dashboard web."""
    try:
        while True:
            try:
                request = client_socket.recv(1024)
            except OSError:
                # Desconexión por timeout
                break

            if request == b"":
                # Mensaje de desconexión
                break

            request = request.decode().split("\r\n")

            response = route_request(request)

            client_socket.send(response)
    except OSError as e:
        print(f"Error en el servidor HTTP: {e}")


def route_request(request):
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
            f"Content-Length: {len(content.encode())}\r\n" + \
            "Connection: close\r\n" + \
            "\r\n" + \
            f"{content}"

        return response.encode()
    except OSError:
        return "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n".encode()


def serve_data():
    """Responder con la data (en JSON) más reciente de los terminales."""
    try:
        json_data = json.dumps(terminal_data)  # Convertir a JSON
    except ValueError as e:
        # Manejar el caso de que el JSON esté mal formado
        print(f"Error al serializar JSON: {e}, '{terminal_data}'")
        return "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\nConnection: close\r\n\r\n".encode()

    # Sin el '+2' en el Content-Length el browser no lee el último '}'
    response = "HTTP/1.1 200 OK\r\n" + \
        "Content-Type: application/json\r\n" + \
        f"Content-Length: {len(json_data.encode())}\r\n" + \
        "Connection: close\r\n" + \
        "\r\n" + \
        f"{json_data}"

    return response.encode()