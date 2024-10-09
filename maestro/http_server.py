from terminals import terminal_data
import asyncio
import json


async def run_http_server(pool, ip: str, port: int):
    """Server HTTP para el monitoreo mediante un dashboard web."""
    server_socket = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    server_socket.setsockopt(pool.SOL_SOCKET, pool.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    server_socket.setblocking(False)
    print(f"Servidor HTTP escuchando en {ip}:{port}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Conexión aceptada de {client_address}")
            await handle_http_request(client_socket)
        except OSError:
            # No hay conexiones disponibles
            pass
        await asyncio.sleep(0.1)


async def handle_http_request(client_socket):
    """Atender una petición HTTP."""
    try:
        while True:
            buffer = bytearray(1024)
            try:
                length = client_socket.recv_into(buffer)
            except OSError:
                # No hay mensajes disponibles
                continue

            request = buffer[:length]

            if request == b"":
                # Mensaje de desconexión
                break

            request = request.decode().split("\r\n")

            # Obtener el header "Connection" si existe
            connection_type = "close"
            for header in request:
                if header.lower().startswith("connection:"):
                    connection_type = header.split(":")[1].strip().lower()

            response = route_request(request)

            if connection_type == "keep-alive":
                # Agregar encabezado Connection si el browser solicitó 'keep-alive'
                response.replace(
                    b"\r\n\r\n", "\r\nConnection: keep-alive\r\n\r\n".encode(), 1)

            client_socket.send(response)

            if connection_type != "keep-alive":
                # Cerrar la conexión si no se especificó 'keep-alive'
                break
            await asyncio.sleep(0.1)
    except OSError as e:
        print(f"Error en el servidor HTTP: {e}")
    finally:
        client_socket.close()


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
            f"Content-Length: {len(content)}\r\n" + \
            "\r\n" + \
            f"{content}"

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
        f"{json_data}"

    return response.encode()
