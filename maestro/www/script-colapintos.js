export function renderColapintos(data) {
  const container = document.getElementById("Colapintos");

  // Estilos adicionales
  const tableStyle = `
    border-collapse: collapse;
    width: 100%;
    margin-top: 15px;
    font-family: Arial, sans-serif;
  `;

  const tdStyle = `
    border: 1px solid #dddddd;
    text-align: center;
    padding: 10px;
    background-color: #f9f9f9;
    color: #333;
  `;

  const thStyle = `
    border: 1px solid #dddddd;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    text-align: center;
  `;

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
      <table style="${tableStyle}">
        <tr>
          <th style="${thStyle}">Tiempo de espera</th>
          <th style="${thStyle}">Cantidad de personas</th>
        </tr>
        <tr>
          <td style="${tdStyle}">${data.tiempo_espera}</td>
          <td style="${tdStyle}">${data.cantidad}</td>
        </tr>
      </table>
    </div>
  </div>`;
}
