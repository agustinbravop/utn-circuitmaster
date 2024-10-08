import uasyncio as asyncio
import micro_monitoring


async def operations():
    # Acá va todo el código específico del equipo.
    pass


def get_app_data():
    # Función que devuelve un `dict` con la data para el maestro.
    return {}


async def main():
    # Funcionamiento del equipo y monitoreo con el maestro se ejecutan concurrentemente.
    await asyncio.gather(
        operations(),
        micro_monitoring.monitoring(get_app_data)   # Monitoreo del maestro
    )

asyncio.run(main())
