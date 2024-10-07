import uasyncio as asyncio
import micro_monitoring


async def operations():
    pass


def get_app_data():
    pass


async def main():
    await asyncio.gather(
        operations(),                               # Código específico a cada grupo
        micro_monitoring.monitoring(get_app_data)   # Monitoreo del maestro
    )

asyncio.run(main())
