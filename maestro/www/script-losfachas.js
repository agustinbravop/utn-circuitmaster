export function renderLosFachas(data) {
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
