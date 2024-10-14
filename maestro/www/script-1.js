import {
  renderBrogramadores,
  renderColapintos,
  renderLosOgata,
} from "./script-2.js";
import {
  renderLosFachas,
  renderRompecircuitos,
} from "./script-3.js";
import {
  renderMonteCarlo,
} from "./script-4.js";

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

const FETCH_INTERVAL_MS = 500;

// Buscar data nueva cada cierto intervalo
setInterval(fetchData, FETCH_INTERVAL_MS);
