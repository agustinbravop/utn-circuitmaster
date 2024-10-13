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

function renderClubTA(data) {
  const container = document.getElementById("ClubTA");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

function renderTeamISI(data) {
  const container = document.getElementById("TeamISI");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

function renderColapintos(data) {
  const container = document.getElementById("Colapintos");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

function renderBrogramadores(data) {
  const container = document.getElementById("Brogramadores");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

function renderLosOgata(data) {
  const container = document.getElementById("LosOgata");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

function renderMonteCarlo(data) {
  const container = document.getElementById("MonteCarlo");
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

/* data = { 
    "state": string,
    "input": string,
    "password": string,
    "has_daylight": bool,
    "remaining_attempts": int,
  } */
function renderRompecircuitos(data) {
  const container = document.getElementById("Rompecircuitos");
  const lockState = data.state || "BOOT_MODE";

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
            ${data.remaining_attempts || "-"}
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

function renderLosFachas(data) {
  const container = document.getElementById("LosFachas");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

const FETCH_INTERVAL_MS = 200;

// Buscar data nueva cada cierto intervalo
setInterval(fetchData, FETCH_INTERVAL_MS);
