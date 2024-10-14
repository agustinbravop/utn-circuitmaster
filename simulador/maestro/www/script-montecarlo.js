export function renderMonteCarlo(data) {
  const tableStyle = `
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      width: 100%;
      margin-top: 15px;
      font-family: Arial, sans-serif;
    `;

  const headerStyle = `
      display: flex;
      justify-content: center;
      align-items: center;
      border: 1px solid #ccc;
      background-color: #60e7b2;
      color: black;
      padding:10px;
      text-align: center;
      font-weight: bold;
    `;

  const elementStyle = `
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border: 1px solid #ccc;
      background-color: #ffffff;
      padding:10px;
      color: black;
      text-align: center;
    `;

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
        <div style="${tableStyle}">
            <div style="${headerStyle}">Estado del sistema</div>
            <div style="${headerStyle}">Alarma Activada</div>
            <div style="${elementStyle}">${estadoSistema}</div>
            <div style="${elementStyle}">${alarmaActivada}</div>
            <div style="${headerStyle}">Presencia Detectada</div>
            <div style="${headerStyle}">Boton de Corona</div>
            <div style="${elementStyle}">${objetoDetectado}</div>
            <div style="${elementStyle}">${botonCorona}</div>
        </div>
      </div>
    </div>`;
}
