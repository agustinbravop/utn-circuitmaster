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

/** Renderizar la información disponible de cada equipo en su menu del dashboard. */
function renderData(data) {
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

function renderRompecircuitos(data) {
  const container = document.getElementById("Rompecircuitos");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

function renderLosFachas(data) {
  const container = document.getElementById("LosFachas");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

const FETCH_INTERVAL_MS = 1000;

// Buscar data nueva cada cierto intervalo
setInterval(fetchData, FETCH_INTERVAL_MS);
