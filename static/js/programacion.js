document.addEventListener('DOMContentLoaded',()=>{
    torneoEnJuego()
})

async function torneoEnJuego() {
    try{
        const div = document.querySelector('.tournament-select-wrapper');
        const response = await fetch(`/api/torneos-en-juego/`);
        const data = await response.json();
        if (data.error){
            console.error('Error: ',data.error);
            return;
        }
        let html = `
            <i class="fa-solid fa-trophy icon-gold"></i>
            <select id="torneo-selector" class="custom-select" onchange="cambiarTorneo(this.value)">
        `;
        data.message.forEach(torneo => {
            html += `
                <option value="${torneo[0]}"> ${torneo[1]} </option>
            `;
        });
        html += `</select>
            <i class="fa-solid fa-chevron-down arrow"></i>
        `;
        div.innerHTML = html
        torneo_pk = document.getElementById('torneo-selector').value;
        jornadas(torneo_pk);
        
    } catch(e){
        console.error(`Error: ${e}`);
    }
}

async function cambiarTorneo(torneo) {
    jornadas(torneo);
}

async function jornadas(torneo_id) {
    try{
        const anotherDiv = document.querySelector('.rounds-tabs-container');
        anotherDiv.innerHTML = `limpiando contenedor`;

        const response = await fetch(`/api/jornadas/${torneo_id}/`);
        const data = await response.json()
         
        let html = ``;
        data.jornadas.forEach((jornada,index) => {
            let isActive = index === 0 ? 'active' : '';
            html += `
                <button class="round-tab ${isActive}" 
                    onclick="filtrarJornada('${jornada}',${torneo_id}, this)"> 
                    Jornada ${jornada} 
                </button>
            `;
        })
        anotherDiv.innerHTML = html;
        if (data.jornadas.length > 0){
            filtrarJornada(data.jornadas[0],torneo_id,anotherDiv.querySelector('.round-tab.active'),)
        }
    } catch(e){
        console.error("Error cargando jornadas:", e);
    }
}

async function filtrarJornada(jornada,torneo_id, buton=null) {
    try {
        
        if (buton){
            // Primero manejamos el estado activo de los botone
            const allButons = document.querySelectorAll('.round-tab');
            allButons.forEach(btn=>btn.classList.remove('active')); // quitar active a todos
            buton.classList.add('active'); // activar el que se clickeó
        }

        const containerpartidos = document.getElementById('matches-container');
        let html = ``;
        
        const response = await fetch(`/api/partidos/${torneo_id}/${jornada}/`);
        const data = await response.json();

        console.log(data.partidos);
    
        data.partidos.forEach(partido => {
            
            // Condicional para el botón según estado
            let actionButton = ``;
            if (partido.estado === 'programado') {
                actionButton += `
                    <button class="btn-action-card" onclick="abrirModalEditar(${partido.id},'${partido.fecha}','${partido.cancha}','${partido.nombre_equipo_local}', '${partido.nombre_equipo_visitante}')">
                        <i class="fa-solid fa-pen"></i> Editar
                    </button>
                `;
            } else if (partido.estado === 'pendiente') {
                actionButton += `
                    <button class="btn-action-card highlight" 
                        onclick="abrirModalAgendar(${partido.id}, '${partido.nombre_equipo_local}', '${partido.nombre_equipo_visitante}')">
                        <i class="fa-regular fa-calendar-plus"></i> Agendar
                    </button>
                `;
            }

            html += `
                <div class="match-card programmed" data-jornada="${jornada}">
                    <div class="card-status status-${partido.estado}">
                        <i class="fa-solid fa-calendar-check"></i> ${partido.estado}
                    </div>
                    
                    <div class="teams-versus">
                        <div class="team">
                            <div class="team-logo">
                                <img src="${partido.escudo_equipo_local}" alt="${partido.nombre_equipo_local}">
                            </div>
                            <span class="team-name">${partido.nombre_equipo_local}</span>
                        </div>
                        <div class="vs">VS</div>
                        <div class="team">
                            <div class="team-logo">
                                <img src="${partido.escudo_equipo_visitante}" alt="${partido.nombre_equipo_visitante}">
                            </div>
                            <span class="team-name">${partido.nombre_equipo_visitante}</span>
                        </div>
                    </div>

                    <div class="match-details">
                        <div class="detail-row">
                            <i class="fa-regular fa-clock"></i>
                            <span> ${partido.fecha} </span>
                        </div>
                        <div class="detail-row">
                            <i class="fa-solid fa-map-pin"></i>
                            <span>${partido.cancha}</span>
                        </div>
                    </div>

                    ${actionButton}
                </div>
            `;
        })
        containerpartidos.innerHTML = html;
    } catch(e){
        console.error(`Se ha presentado un error antes de renderizar los equipos: ${e}`);
    }
}

// Manejo del Modal
const modal = document.getElementById('modal-programacion');

function abrirModalAgendar(matchId, equipoA, equipoB) {

    console.log(`Id_partido ${matchId}, equipoA ${equipoA} VS equipoB ${equipoB}`);

    document.getElementById('modal-match-id').value = matchId;
    document.getElementById('modal-team-a').innerText = equipoA;
    document.getElementById('modal-team-b').innerText = equipoB;
    
    // Limpiar campos previos
    document.querySelector('input[name="fecha"]').value = '';
    document.querySelector('input[name="hora"]').value = '';
    
    modal.classList.add('active');

}

async function AgendarPartido(event) {
    try {
        event.preventDefault()
        const response = await fetch(`/api/partido-agenda/`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body : JSON.stringify({
                'partido_id':document.getElementById('modal-match-id').value,
                'fecha':document.getElementById('id_fecha').value,
                'hora':document.getElementById('id_hora').value,
                'cancha':document.getElementById('id_cancha').value
            })
        });
        
        const data = await response.json()

        console.log(data);
        

        let formulario = document.getElementById('form-agendar');
        formulario.reset();
        cerrarModal();

        if (data.error){
            showToast(data.error,'error');
            return;
        }

        let torneo_id = document.getElementById('torneo-selector').value;
        let jornada = document.querySelector('.match-card.programmed').dataset.jornada;
        filtrarJornada(jornada,torneo_id, buton=null);

        showToast(data.message);
    } catch(e){
        console.error(`Ha ocurrido un error al enviar los datos: ${e}`)
    }
}

function abrirModalEditar(matchId,fecha_completa,cancha,equipoLocal,equipoVisitante) {
    console.log(`PArtido id : ${matchId} | fecha : ${fecha_completa} | cancha: ${cancha}`);

    const [fecha, horaConZona] = fecha_completa.split('T');
    const hora = horaConZona.replace('Z','');
    console.log(fecha,hora);

    document.getElementById('modal-team-a').innerHTML = equipoLocal;
    document.getElementById('modal-team-b').innerHTML = equipoVisitante;

    // Aquí deberías (idealmente) traer los datos actuales via fetch
    // Para el ejemplo, abrimos el modal genérico
    document.getElementById('modal-match-id').value = matchId;
    document.getElementById('id_cancha').value = cancha;
    document.getElementById('id_fecha').value = fecha;
    document.getElementById('id_hora').value = hora;
    modal.classList.add('active');
}

function cerrarModal() {
    modal.classList.remove('active');
}

// Cerrar al dar click fuera del modal
modal.addEventListener('click', (e) => {
    if (e.target === modal) cerrarModal();
});

// Función profesional para mostrar el Toast
function showToast(text, type = "success") {
    
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast-message';
    
    // Si es error, cambiamos el color del borde
    if (type === "error") toast.style.borderColor = "#ff5252";

    toast.innerHTML = `
        <span>${text}</span>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-left:15px; opacity:0.5">
            <path d="M20 6L9 17l-5-5" />
        </svg>
    `;

    container.appendChild(toast);

    // Desaparecer después de 4 segundos
    setTimeout(() => {
        toast.classList.add('fade-out');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}