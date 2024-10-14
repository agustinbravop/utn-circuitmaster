export function renderLosOgata(data) {
  const container = document.getElementById("LosOgata");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `
     <div class="flex flex-col mt-2 bg-white p-4 rounded-lg">
        <p>Promedio de Volumen en dB: ${data.promedio_ruido}</p>
        <p>Volumen de la televisión: ${data.volumen_actual}</p>
        <p>¿Entro alguien?: ${
          data.entro_alguien === true ? "Ha entrado alguien" : "No entró nadie"
        }</p>
      </div>
`;
}
