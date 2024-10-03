async function fetchData() {
  try {
    const response = await fetch("/data");
    const data = await response.json();
    const container = document.getElementById("data-container");
    container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

// Buscar data nueva cada cierto intervalo (milisegundos).
setInterval(fetchData, 1000);
