from terminals import terminal_data
import uasyncio as asyncio
import ujson as json


async def run_http_server(ip: str, port: int):
    """Server HTTP para el monitoreo mediante un dashboard web."""
    server = await asyncio.start_server(handle_http_request, ip, port)
    print(f"Servidor HTTP escuchando en {ip}:{port}")
    await server.wait_closed()


async def handle_http_request(reader, writer):
    """Atender una petición HTTP del dashboard web."""
    try:
        while True:
            request = await reader.read(1024)

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

            writer.write(response)
            await writer.drain()

            if connection_type != "keep-alive":
                # Cerrar la conexión si no se especificó 'keep-alive'
                break
    except OSError as e:
        print(f"Error en el servidor HTTP: {e}")
    finally:
        writer.close()
        await writer.wait_closed()


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
    try:
        json_data = json.dumps(terminal_data)  # Convertir a JSON
    except ValueError as e:
        # Manejar el caso de que el JSON esté mal formado
        print(f"Error al serializar JSON: {e}, '{terminal_data}'")
        return "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\nConnection: close\r\n\r\n".encode()

    # Sin el '+2' en el Content-Length el browser no lee el último '}'
    response = "HTTP/1.1 200 OK\r\n" + \
        "Content-Type: application/json\r\n" + \
        f"Content-Length: {len(json_data)+2}\r\n" + \
        "\r\n" + \
        f"{json_data}"

    return response.encode()
