import asyncio  # Reemplazar por `asyncio` si utiliza CircuitPython
# Reemplazar por `circuit_monitoring` si utiliza CircuitPython
import micro_monitoring
import time


async def operations():
    # Acá va todo el código específico del equipo.
    pass


def get_app_data():
    # Función que devuelve un `dict` con la data para el maestro.
    return {"tiempo": time.time() % 100}


async def main():
    # Funcionamiento del equipo y monitoreo con el maestro se ejecutan concurrentemente.
    await asyncio.gather(
        operations(),
        micro_monitoring.monitoring(get_app_data)   # Monitoreo del maestro
    )

asyncio.run(main())
