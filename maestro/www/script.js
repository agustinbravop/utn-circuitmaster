/** Petición HTTP de la data al maestro. */
async function fetchData() {
  try {
    const response = await fetch("/data");
    const data = await response.json();
    renderData(data);
  } catch (error) {
    console.error("Error al buscar la data:", error);
  }
}

const ALL_TERMINALS = [
  "TeoriaDelDescontrol",
  "ClubTA",
  "TeamISI",
  "Colapintos",
  "Brogramadores",
  "LosOgata",
  "MonteCarlo",
  "Rompecircuitos",
  "LosFachas",
];

/** Renderizar la información disponible de cada equipo en su menu del dashboard. */
function renderData(data) {
  if (data.terminales_conectados) {
    for (const t of ALL_TERMINALS) {
      // Indicar si está desconectado o no
      const container = document.getElementById(t);
      if (data.terminales_conectados.includes(t)) {
        container.parentElement.classList.remove("disconnected");
        container.parentElement.classList.add("connected");
      } else {
        container.parentElement.classList.add("disconnected");
      }
    }
  }
  if (data.TeoriaDelDescontrol) {
    renderTeoriaDelDescontrol(data.TeoriaDelDescontrol);
  }
  if (data.ClubTA) {
    renderClubTA(data.ClubTA);
  }
  if (data.TeamISI) {
    renderTeamISI(data.TeamISI);
  }
  if (data.Colapintos) {
    renderColapintos(data.Colapintos);
  }
  if (data.Brogramadores) {
    renderBrogramadores(data.Brogramadores);
  }
  if (data.LosOgata) {
    renderLosOgata(data.LosOgata);
  }
  if (data.MonteCarlo) {
    renderMonteCarlo(data.MonteCarlo);
  }
  if (data.Rompecircuitos) {
    renderRompecircuitos(data.Rompecircuitos);
  }
  if (data.LosFachas) {
    renderLosFachas(data.LosFachas);
  }
}

function renderTeoriaDelDescontrol(data) {
  const container = document.getElementById("TeoriaDelDescontrol");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

function renderTeamISI(data) {
  const container = document.getElementById("TeamISI");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}
const uiRompecircuitos = {
  DISABLED: ["DESHABILITADO", "🪫", "black"],
  BOOT_MODE: ["INICIALIZACIÓN", "🔑", "grey"],
  LOCKED: ["CERRADO", "🔒", "blue"],
  OPEN: ["ABIERTO", "✅", "green"],
  ALARMED: ["ALARMADO", "🚨", "red"],
};

/* dataRompecircuitos = { 
    "state": string,
    "input": string,
    "password": string,
    "has_daylight": bool,
    "remaining_attempts": int,
  } */
function renderRompecircuitos(data) {
  const container = document.getElementById("Rompecircuitos");
  const lockState = data.state ?? "BOOT_MODE";

  container.innerHTML = `<div
    style="display: flex; gap: 10px; justify-content: center; padding: 10px 0px;"
  >
    <div style="width: 45%;">
      <p style="margin: none; text-align: center;">Estado: <span style="color: ${
        uiRompecircuitos[lockState][2]
      };">${uiRompecircuitos[lockState][0]}</span></p>
      <div style="display: flex; gap: 10px; justify-content: center;">
        <div style="font-size: 60px; margin: none;">
          ${uiRompecircuitos[lockState][1]}
        </div>
        <svg
          style="width: 70px; height: 70px; margin-top: 10px;"
          id="Layer_1"
          data-name="Layer 1"
          xmlns="http://www.w3.org/2000/svg"
          fill="${uiRompecircuitos[lockState][2]}"
          viewBox="0 0 115.04 122.88"
        >
          <title>diode-led-light</title>
          <path
            d="M88.89,50.07v27h8.45a2.11,2.11,0,0,1,2.1,2.11V96.43a2.11,2.11,0,0,1-2.1,2.11H80.7v21a3.38,3.38,0,0,1-3.37,3.37H74.17a3.39,3.39,0,0,1-3.38-3.38v-21H44.25v21a3.38,3.38,0,0,1-3.37,3.37H37.72a3.4,3.4,0,0,1-3.38-3.38v-21H17.71a2.11,2.11,0,0,1-2.11-2.11V79.21a2.11,2.11,0,0,1,2.11-2.11h8.44v-27c0-16.22,8.14-26.65,18.56-31.25a32,32,0,0,1,25.62,0c10.42,4.6,18.56,15,18.56,31.25ZM18.6,34.5a3.68,3.68,0,1,1-2,7.09l-13.91-4a3.68,3.68,0,0,1,2-7.09l13.91,4Zm79.85,7.09a3.68,3.68,0,0,1-2-7.09l13.91-4a3.69,3.69,0,0,1,2,7.09l-13.92,4Zm-67-31.85a3.67,3.67,0,1,1-5.27,5.12L17.82,6.24a3.68,3.68,0,0,1,5.27-5.13l8.35,8.63Zm57.23,5.33a3.67,3.67,0,1,1-5.26-5.13L92,1.11a3.68,3.68,0,0,1,5.27,5.13l-8.55,8.83ZM52.45,30.49a2.63,2.63,0,1,1,1.54,5c-5.61,1.74-8.84,4.39-10.67,7.85-1.92,3.65-2.47,8.37-2.62,14a2.62,2.62,0,1,1-5.24-.13c.17-6.34.83-11.77,3.21-16.29,2.48-4.69,6.66-8.21,13.78-10.42Zm34,50.83H19.81v13H95.23v-13Zm-2.86-5.26v-26c0-13.81-6.76-22.62-15.41-26.43a26.74,26.74,0,0,0-21.38,0c-8.65,3.81-15.41,12.62-15.41,26.43v26Z"
          />
        </svg>
      </div>
    </div
    <div style="width: 55%;">
      <table style="border-collapse: collapse; padding-top: 15px;">
        <tr>
          <td style="border: 1px solid black; padding: 7px;">Input actual</td>
          <td style="border: 1px solid black; padding: 7px;">
            ${data.input || "-"}
          </td>
        </tr>
        <tr>
          <td style="border: 1px solid black; padding: 7px;">PIN</td>
          <td style="border: 1px solid black; padding: 7px;">
            ${data.password || "-"}
          </td>
        </tr>
        <tr>
          <td style="border: 1px solid black; padding: 7px;">
            Intentos restantes
          </td>
          <td style="border: 1px solid black; padding: 7px;">
            ${data.remaining_attempts ?? "-"}
          </td>
        </tr>
        <tr>
          <td style="border: 1px solid black; padding: 7px;">
            Nivel de iluminación
          </td>
          <td style="border: 1px solid black; padding: 7px;">
            ${data.has_daylight ? "🌞" : "💤"}
          </td>
        </tr>
      </table>
    </div>
  </div>`;
}

function renderMonteCarlo(data) {
  const container = document.getElementById("MonteCarlo");

  const estadoSistema =
    data.estado === "B"
      ? `Bloqueado <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="24" height="24" fill="white"/>
    <path d="M6 19V11C6 10.4477 6.44772 10 7 10H17C17.5523 10 18 10.4477 18 11V19C18 19.5523 17.5523 20 17 20H7C6.44772 20 6 19.5523 6 19Z" stroke="#000000" stroke-linejoin="round"/>
    <circle cx="12" cy="15" r="2" stroke="#000000" stroke-linejoin="round"/>
    <path d="M8 10V8C8 5.79086 9.79086 4 12 4C14.2091 4 16 5.79086 16 8V10H8Z" stroke="#000000" stroke-linejoin="round"/>
    </svg>`
      : data.estado === "D"
      ? `Desbloqueado <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="24" fill="white"/>
        <path d="M6 19V11C6 10.4477 6.44772 10 7 10H17C17.5523 10 18 10.4477 18 11V19C18 19.5523 17.5523 20 17 20H7C6.44772 20 6 19.5523 6 19Z" stroke="#000000" stroke-linejoin="round"/>
        <circle cx="12" cy="15" r="2" stroke="#000000" stroke-linejoin="round"/>
        <path d="M16 10V6.5C16 5.11929 17.1193 4 18.5 4V4V4C19.8807 4 21 5.11929 21 6.5V10" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`
      : `Alerta <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="24" fill="white"/>
        <circle cx="7" cy="12" r="0.5" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="12" cy="12" r="0.5" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="17" cy="12" r="0.5" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`;

  const alarmaActivada = data.alarmaActivada
    ? `Si <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g clip-path="url(#clip0_15_159)">
    <rect width="24" height="24" fill="white"/>
    <path d="M9.5 19C8.89555 19 7.01237 19 5.61714 19C4.87375 19 4.39116 18.2177 4.72361 17.5528L5.57771 15.8446C5.85542 15.2892 6 14.6774 6 14.0564C6 13.2867 6 12.1434 6 11C6 9 7 5 12 5C17 5 18 9 18 11C18 12.1434 18 13.2867 18 14.0564C18 14.6774 18.1446 15.2892 18.4223 15.8446L19.2764 17.5528C19.6088 18.2177 19.1253 19 18.382 19H14.5M9.5 19C9.5 21 10.5 22 12 22C13.5 22 14.5 21 14.5 19M9.5 19C11.0621 19 14.5 19 14.5 19" stroke="#000000" stroke-linejoin="round"/>
    <path d="M12 5V3" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <defs>
    <clipPath id="clip0_15_159">
    <rect width="24" height="24" fill="white"/>
    </clipPath>
    </defs>
    </svg>`
    : `No <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g clip-path="url(#clip0_15_166)">
    <rect width="24" height="24" fill="white"/>
    <path d="M6 15C6 15 6 13 6 11C6 9 7 5 12 5C13.5723 5 14.749 5.39552 15.6235 6M9.5 19C9.5 21 10.5 22 12 22C13.5 22 14.5 21 14.5 19M9.5 19C11.0621 19 14.5 19 14.5 19M9.5 19C9.14909 19 8.36719 19 7.5 19M14.5 19H18.382C19.1253 19 19.6088 18.2177 19.2764 17.5528L18 15C18 15 18 13 18 11C18 10.3755 17.9025 9.55594 17.6161 8.72408" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M12 5V3" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M21 3L3 21" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <defs>
    <clipPath id="clip0_15_166">
    <rect width="24" height="24" fill="white"/>
    </clipPath>
    </defs>
    </svg>`;

  const objetoDetectado = data.objetoDetectado
    ? `Presente <svg width="16px" height="16px" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="8" cy="8" r="8" fill="#60e7b2"/>
    </svg>`
    : `Ausente <svg width="16px" height="16px" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="8" cy="8" r="8" fill="#e76060"/>
    </svg>`;

  const botonCorona = data.botonCorona
    ? `Presionado <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="24" height="24" fill="white"/>
    <path d="M7 13.4545L8.97619 15.3409C9.36262 15.7098 9.97072 15.7098 10.3571 15.3409L17 9" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="12" cy="12" r="9" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`
    : `No presionado <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="24" height="24" fill="white"/>
    <path d="M7 12H17" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="12" cy="12" r="9" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`;

  container.innerHTML = `<div
      style="display: flex; gap: 10px; justify-content: center; padding: 10px 0px;">
      
      
      <div style="width: 100%;">
        <div class="montecarlo-table">
            <div class="montecarlo-header">Estado del sistema</div>
            <div class="montecarlo-header">Alarma Activada</div>
            <div class="montecarlo-element">${estadoSistema}</div>
            <div class="montecarlo-element">${alarmaActivada}</div>
            <div class="montecarlo-header">Presencia Detectada</div>
            <div class="montecarlo-header">Boton de Corona</div>
            <div class="montecarlo-element">${objetoDetectado}</div>
            <div class="montecarlo-element">${botonCorona}</div>
        </div>
      </div>
    </div>`;
}

function renderLosOgata(data) {
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

function renderLosFachas(data) {
  const container = document.getElementById("LosFachas");
  const temp = data.temp;
  const hum = data.hum;
  let tempCol = "lime";
  let humCol = "lime";
  if (temp > 25) tempCol = "red";
  if (temp <= 18) tempCol = "cyan";

  // Set color based on humidity (optional, you can expand this part)
  if (hum > 75) humCol = "red";
  if (hum <= 60) humCol = "cyan";
  // Personalizar por el equipo correspondiente
  container.innerHTML = `
        <div style="color: black; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
            <h1>Monitoreo de Temperatura y Humedad</h1>
            <div style="font-size: 24px; margin-bottom: 20px; padding: 8px; background-color: ${tempCol}; border: 1px solid black; border-radius: 12px;">
                Temperatura: <span id="temperature">${temp}</span> °C
            </div>
            <div style="font-size: 24px; margin-bottom: 20px; padding: 8px; background-color: ${humCol}; border: 1px solid black; border-radius: 12px;">
                Humedad: <span id="humidity">${hum}</span> %
            </div>
        </div>`;
}

function renderColapintos(data) {
  const container = document.getElementById("Colapintos");

  // Actualizamos el HTML con estilos
  container.innerHTML = `<div
    style="display: flex; gap: 10px; justify-content: center; padding: 10px 0px;"
  >
    <div >
      
      <div style="display: flex; gap: 10px; justify-content: center;">
      
          <title>diode-led-light</title>
          <path
            d="M88.89,50.07v27h8.45a2.11,2.11,0,0,1,2.1,2.11V96.43a2.11,2.11,0,0,1-2.1,2.11H80.7v21a3.38,3.38,0,0,1-3.37,3.37H74.17a3.39,3.39,0,0,1-3.38-3.38v-21H44.25v21a3.38,3.38,0,0,1-3.37,3.37H37.72a3.4,3.4,0,0,1-3.38-3.38v-21H17.71a2.11,2.11,0,0,1-2.11-2.11V79.21a2.11,2.11,0,0,1,2.11-2.11h8.44v-27c0-16.22,8.14-26.65,18.56-31.25a32,32,0,0,1,25.62,0c10.42,4.6,18.56,15,18.56,31.25ZM18.6,34.5a3.68,3.68,0,1,1-2,7.09l-13.91-4a3.68,3.68,0,0,1,2-7.09l13.91,4Zm79.85,7.09a3.68,3.68,0,0,1-2-7.09l13.91-4a3.69,3.69,0,0,1,2,7.09l-13.92,4Zm-67-31.85a3.67,3.67,0,1,1-5.27,5.12L17.82,6.24a3.68,3.68,0,0,1,5.27-5.13l8.35,8.63Zm57.23,5.33a3.67,3.67,0,1,1-5.26-5.13L92,1.11a3.68,3.68,0,0,1,5.27,5.13l-8.55,8.83ZM52.45,30.49a2.63,2.63,0,1,1,1.54,5c-5.61,1.74-8.84,4.39-10.67,7.85-1.92,3.65-2.47,8.37-2.62,14a2.62,2.62,0,1,1-5.24-.13c.17-6.34.83-11.77,3.21-16.29,2.48-4.69,6.66-8.21,13.78-10.42Zm34,50.83H19.81v13H95.23v-13Zm-2.86-5.26v-26c0-13.81-6.76-22.62-15.41-26.43a26.74,26.74,0,0,0-21.38,0c-8.65,3.81-15.41,12.62-15.41,26.43v26Z"
          />
        </svg>
      </div>
    </div>
    <div style="width: 55%;">
      <table class="colapintos-table">
        <tr>
          <th class="colapintos-th">Tiempo de espera</th>
          <th class="colapintos-th">Cantidad de personas</th>
        </tr>
        <tr>
          <td class="colapintos-td">${data.tiempo_espera}</td>
          <td class="colapintos-td">${data.cantidad}</td>
        </tr>
      </table>
    </div>
  </div>`;
}

function renderClubTA(data) {
  const container = document.getElementById("ClubTA");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `
    <div class="flex flex-col mt-2 bg-white p-4 rounded-lg">
        <p>El color actual es: ${data.color}</p>
      </div>
  `;
}

function renderBrogramadores(data) {
  const container = document.getElementById("Brogramadores");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

const FETCH_INTERVAL_MS = 500;

// Buscar data nueva cada cierto intervalo
setInterval(fetchData, FETCH_INTERVAL_MS);
