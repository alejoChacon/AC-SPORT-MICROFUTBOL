async function tabla(equipo_pk,estado) {
    try{
        const response = await fetch(`api/calendario-partidos/${equipo_pk}/${estado}/`);
        const data = await response.json();
        console.log(data.calendario_partidos);
        if(data.error){
            console.error(data.error);
            return;
        }
        const tabla = document.querySelector(".tabla-partidos");
        
        let html = ``;
        html += `
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Rival</th>
                    <th>Resultado</th>
                    <th>Cancha</th>
                    <th>Hora</th>
                </tr>
            </thead>
            <tbody>
        `;
        data.calendario_partidos.forEach(dato => {
            html += `
                <tr>
                    <td> ${dato.fecha} </td>
                    <td> ${dato.rival} </td>
                    <td> ${dato.resultado} </td>
                    <td> ${dato.cancha} </td>
                    <td> ${dato.hora} </td>
                </tr>
            `;
        });
        html += `</tbody> </table> `;
        tabla.innerHTML = html;
    }catch(error){
        console.error("Ha habido un error al mostrar la info:",error)
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if (equipo_pk){
        console.log(equipo_pk);
        tabla(equipo_pk,"programado");
        estadisticas(equipo_pk);
    
        const botonProgramado = document.querySelectorAll(".filtro");
        botonProgramado.forEach(btn => {
            btn.addEventListener("click", () => {
                botonProgramado.forEach(b => b.classList.remove("activo"));
                btn.classList.add("activo");
                estado = btn.dataset.filter;
                console.log(estado);
                tabla(equipo_pk,estado);
            })
        })
    } 
})

async function estadisticas(equipo_pk) {
    try{
        const response = await fetch(`/mi-equipo/api/equipo_info/${equipo_pk}/`);
        const data = await response.json();
        const section = document.querySelector(".equipo-stats");
        console.log(data.equipo_info)
        let html = `
            <div class="stat-card">
                <h3>Partidos Jugados</h3>
                <p> ${data.equipo_info.partidos_jugados} </p>
            </div>
            <div class="stat-card">
                    <h3>Victorias</h3>
                    <p> ${data.equipo_info.partidos_ganados} </p>
            </div>
            <div class="stat-card">
                    <h3>Derrotas</h3>
                    <p> ${data.equipo_info.partidos_perdidos} </p>
            </div>
            <div class="stat-card">
                    <h3>Empates</h3>
                    <p> ${data.equipo_info.partidos_empatados} </p>
            </div>
        `;
        section.innerHTML = html;
    } catch(error){
        console.error("No se ha podido cargar la informacion debido al error:", error)
    }
}

async function searchteam(event) {
    try{
        document.querySelector('.no-equipo-card').style.display = 'none';
        document.getElementById('results-container').style.display = 'block';
        const componentDiv = document.querySelector('.show-team');
        componentDiv.innerHTML = '<p class="loading">Buscando equipos disponibles...</p>'; // Feedback visual
        
        const response = await fetch('api/searchteam/');
        const data = await response.json();
        if (data.error || data.length === 0){
            componentDiv.innerHTML = '<p class="no-results">No se encontraron equipos con cupos disponibles.</p>';
            return;
        }

        componentDiv.innerHTML = ''; // Limpiar mensaje de carga

        data.forEach(e=>{
            // e[0] = id, e[1] = nombre, e[2] = nombre capitan (Porque es lista, si fuera diccionario recuerda que se usa e.id, e.nombre o e.capitan)
            componentDiv.innerHTML += `
            <div class="team-card-search">
                <div class="team-card-info">
                    <h3>${e[1]}</h3>
                    <p><strong>Capitán:</strong> ${e[2] || 'Sin asignar'}</p>
                    <span class="badge-cupos">Cupos disponibles</span>
                </div>
                <button class="btn-solicitud" onclick="sendRequest(${e[0]})">
                    Enviar Solicitud
                </button>
            </div>
            `;
        })

    } catch(error){
        console.error(error);
        document.querySelector('.show-team').innerHTML = '<p class="error">Error al conectar con el servidor.</p>';
    }
}

var url = `ws://${window.location.host}/ws/myteam/`;

var webSocketMiEquipo =  new WebSocket(url);

webSocketMiEquipo.onopen = function(e){
    console.log('Ha establecido conexion desde el apartado Mi Equipo!');
}

async function sendRequest(equipo_pk) {
    const id_equipo = equipo_pk;
    try{
        if (webSocketMiEquipo.readyState === WebSocket.OPEN){
            webSocketMiEquipo.send(JSON.stringify({
                'equipo_id':id_equipo,
            }))
            document.getElementById('results-container').style.display = 'none';
            const divMessage = document.querySelector('.message-solicitud');
            divMessage.innerHTML = `
                <div style="background: rgb(250,250,250,0,15); border: 1px solid #e0e0e0; padding: 16px; border-radius: 10px; text-align: center;">
                    <span style="background: #e8f5e9; color: #2e7d32; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Estado: Pendiente</span>
                    <h4 style="margin: 10px 0 5px 0; color: #45c122; font-size: 16px;">¡Solicitud en camino!</h4>
                    <p style="margin: 0; color: #ffffff; font-size: 13px; line-height: 1.5;">Hemos enviado tu perfil al capitán del equipo. <br> Por favor, mantente atento a tus notificaciones.</p>
                </div>
            `;
        }
    } catch(error){
        console.error(error);
    }
}

function cancelSearch(){
    document.getElementById('results-container').style.display = 'none';
    document.querySelector('.no-equipo-card').style.display = 'block';
}

