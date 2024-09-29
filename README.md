# utn-circuitmaster

Repositorio para el controlador maestro del laboratorio de microcontroladores de Tecnologías para la Automatización, UTN FRRe 2024.

El código MicroPython en `maestro/` sirve para el único microcontrolador maestro de la red. El código en `terminal/` contiene el boilerplate necesario para cada microcontrolador terminal, y deberá ser personalizado por cada grupo. Este repositorio se encarga del:

- **Descubrimiento de la red**: que el maestro y los terminales se vinculen automáticamente.
- **Polling**: desde el maestro, monitorear en tiempo real el estado de todos los terminales.
- **Dashboard**: desde un dashboard web, monitorear en tiempo real (mediante el maestro) el estado de los terminales de la red.

## Descubrimiento de la Red

