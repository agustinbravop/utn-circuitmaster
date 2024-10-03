# utn-circuitmaster

Repositorio para el controlador maestro del laboratorio de microcontroladores de Tecnologías para la Automatización, UTN FRRe 2024.

El código MicroPython en `maestro/` sirve para el único microcontrolador maestro de la red. El código en `terminal/` contiene el boilerplate necesario para cada microcontrolador terminal, y deberá ser personalizado por cada equipo para que se pueda adaptar al código específico de ese equipo. Este repositorio se encarga del:

- **Descubrimiento de la red**: que el maestro y los terminales se vinculen automáticamente.
- **Polling**: desde el maestro, monitorear en tiempo real el estado de todos los terminales.
- **Dashboard**: desde un dashboard web, monitorear en tiempo real (mediante el maestro) el estado de los terminales de la red.

Se utiliza la librería `asyncio` para la ejecución concurrente de:

- En el maestro: el servidor HTTP, el descubrimiento de la red, y la conexión con cada terminal.
- En cada terminal: la escucha de mensajes de descubrimiento, el servidor TCP, y el código específico del equipo.

Nota: los archivos `/terminal/micro_monitoring.py` y `/terminal/circuit_monitoring.py` están orientados específicamente para MicroPython y CircuitPython respectivamente. Cumplen la misma funcionalidad, aunque equipo debe usar el que corresponde al runtime que utiliza.

## Conexión a WiFi

Al iniciarse los dispositivos, intentan conectarse a una red WiFi local cuyo `WLAN_SSID` y `WLAN_PASSWORD` se indican en constantes globales en los archivos `/maestro/main.py` y `/terminal/{circuit|micro}_monitoring.py`.

Es necesario que estén conectados a la red local para poder comunicarse con el resto de controladores.

## Descubrimiento de la Red

El maestro envía periódicamente un mensaje de broadcast UDP en la red local. Si un terminal detecta uno de estos broadcasts, le responde al maestro con un UDP dirigido que incluye el nombre del equipo, la dirección IP, y el puerto, del servidor TCP del terminal. Con esta información, el maestro se conecta (como cliente) al servidor TCP del terminal.

Si el maestro se desconecta, el terminal vuelve al "modo descubrimiento" y a esperar mensajes de broadcasts nuevamente.

## Polling del Maestro a los Terminales

El maestro tiene en todo momento un listado de los terminales que existen y los que están actualmente conectados. La conexión TCP con cada terminal permite periódicamente muestrear los datos (en formato JSON) que cada equipo considera representativo de su terminal. Estos datos son concentrados en una variable global.

## Monitoreo Mediante Dashboard Web

El maestro contiene un servidor HTTP/1.1 que ante una petición `GET /` devuelve una página web definida en `/maestro/www`. Esta página web tiene un código JavaScript `/maestro/www/script.js` que cada cierto intervalo de tiempo hace una petición `GET /data` al servidor, actualizando la información que presenta en el navegador. El servidor del maestro devuelve en formato JSON un objeto con los datos más recientes de cada terminal en la red.
