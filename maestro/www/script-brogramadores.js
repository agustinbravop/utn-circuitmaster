export function renderBrogramadores(data) {
  const container = document.getElementById("Brogramadores");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}
