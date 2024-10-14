export function renderClubTA(data) {
  const container = document.getElementById("ClubTA");
  // Personalizar por el equipo correspondiente
  container.innerHTML = `
    <div class="flex flex-col mt-2 bg-white p-4 rounded-lg">
        <p>El color actual es: ${data.color}</p>
      </div>
  `;
}
