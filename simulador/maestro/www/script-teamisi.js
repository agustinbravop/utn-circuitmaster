export function renderTeamISI(data) {
  const container = document.getElementById("TeamISI");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}
