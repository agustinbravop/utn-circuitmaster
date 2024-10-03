import uasyncio as asyncio
import micro_monitoring


async def operations():
    pass


async def main():
    await asyncio.gather(
        operations(),                   # Código específico a cada grupo
        micro_monitoring.monitoring()   # Código para la comunicación con el maestro
    )

asyncio.run(main())
