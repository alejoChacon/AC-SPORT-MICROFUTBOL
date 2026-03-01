// Variable global para el equipo
let webSocketMiEquipo = null;

document.addEventListener("DOMContentLoaded", () => {
    // 1. INICIALIZACIÓN DE DATOS SI HAY EQUIPO
    if (typeof equipo_pk !== 'undefined' && equipo_pk) {
        tabla(equipo_pk, "programado");
        estadisticas(equipo_pk);
        initWebSocket();

        // Filtros de tabla
        const filtros = document.querySelectorAll(".filtro");
        filtros.forEach(btn => {
            btn.addEventListener("click", () => {
                filtros.forEach(b => b.classList.remove("activo"));
                btn.classList.add("activo");
                tabla(equipo_pk, btn.dataset.filter);
            });
        });

        // 2. LÓGICA TÁCTICA (DRAG & DROP)
        initDragAndDrop();
        renderizarAlineacionGuardada();
    }
    else {
        initWebSocket();
    }
});

// Función para Estadísticas
async function estadisticas(equipo_pk) {
    try {
        const response = await fetch(`/mi-equipo/api/equipo_info/${equipo_pk}/`);
        const data = await response.json();
        const section = document.querySelector(".equipo-stats");
        section.innerHTML = `
            <div class="stat-card"><h3>Partidos</h3><p>${data.equipo_info.partidos_jugados}</p></div>
            <div class="stat-card"><h3>Victorias</h3><p>${data.equipo_info.partidos_ganados}</p></div>
            <div class="stat-card"><h3>Derrotas</h3><p>${data.equipo_info.partidos_perdidos}</p></div>
            <div class="stat-card"><h3>Empates</h3><p>${data.equipo_info.partidos_empatados}</p></div>
        `;
    } catch (error) { console.error("Error stats:", error); }
}

// Función para Tabla de Partidos
async function tabla(equipo_pk, estado) {
    try {
        const response = await fetch(`api/calendario-partidos/${equipo_pk}/${estado}/`);
        const data = await response.json();
        const tbody = document.querySelector(".tabla-partidos tbody");
        
        if (data.calendario_partidos.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">No hay partidos registrados.</td></tr>';
            return;
        }

        tbody.innerHTML = data.calendario_partidos.map(dato => `
            <tr>
                <td>${dato.fecha}</td>
                <td>${dato.rival}</td>
                <td>${dato.resultado}</td>
                <td>${dato.cancha}</td>
                <td>${dato.hora}</td>
            </tr>
        `).join('');
    } catch (error) { console.error("Error tabla:", error); }
}

// Lógica de Drag & Drop
function initDragAndDrop() {
    const jugadores = document.querySelectorAll('.ficha-tactica');
    const posiciones = document.querySelectorAll('.posicion');
    const banquillo = document.getElementById('lista-suplentes');

    jugadores.forEach(j => {
        j.addEventListener('dragstart', e => {
            j.classList.add('dragging');
            e.dataTransfer.setData('text/plain', j.id);
        });
        j.addEventListener('dragend', () => j.classList.remove('dragging'));
    });

    posiciones.forEach(pos => {
        pos.addEventListener('dragover', e => {
            e.preventDefault();
            pos.style.background = "rgba(255, 204, 0, 0.1)";
        });
        pos.addEventListener('dragleave', () => pos.style.background = "transparent");
        pos.addEventListener('drop', e => {
            e.preventDefault();
            pos.style.background = "transparent";
            const id = e.dataTransfer.getData('text');
            const el = document.getElementById(id);
            const existente = pos.querySelector('.ficha-tactica');
            if (existente) banquillo.appendChild(existente);
            pos.appendChild(el);
        });
    });

    banquillo.addEventListener('dragover', e => e.preventDefault());
    banquillo.addEventListener('drop', e => {
        const id = e.dataTransfer.getData('text');
        banquillo.appendChild(document.getElementById(id));
    });
}

// WebSocket y Búsqueda
function initWebSocket() {
    const url = `ws://${window.location.host}/ws/myteam/`;
    webSocketMiEquipo = new WebSocket(url);
    webSocketMiEquipo.onopen = () => console.log('Conectado a Mi Equipo');

    webSocketMiEquipo.onmessage = function(e){
    const data = JSON.parse(e.data);
    console.log('Datos: ',data.error);
    if (data.error){
        mostrarErrorToast(data.error);
        document.getElementById('jugadoresfree').style.display = 'none';
        document.getElementById('modal-jugadores').style.display = 'none';
        // Ocultaremos el div de los usuarios sin el equipo y el boton de agregar Jugadores

    }
}

}

async function searchteam(event) {
    const componentDiv = document.querySelector('.show-team');
    document.querySelector('.no-equipo-card').style.display = 'none';
    document.getElementById('results-container').style.display = 'block';
    componentDiv.innerHTML = '<p class="loading">Buscando...</p>';

    try {
        const response = await fetch('api/searchteam/');
        const data = await response.json();
        componentDiv.innerHTML = data.map(e => `
            <div class="team-card-search">
                <div class="team-card-info">
                    <h3>${e[1]}</h3>
                    <p>Capitán: ${e[2] || 'Sin asignar'}</p>
                    <span class="badge-cupos">Cupos disponibles</span>
                </div>
                <button class="btn-solicitud" onclick="sendRequest(${e[0]})">Enviar Solicitud</button>
            </div>
        `).join('');
    } catch (e) { componentDiv.innerHTML = '<p>Error de conexión</p>'; }
}

function sendRequest(id) {
    if (webSocketMiEquipo && webSocketMiEquipo.readyState === WebSocket.OPEN) {
        webSocketMiEquipo.send(JSON.stringify({'equipo_id': id,'informacion':'jugador'}));
        document.getElementById('results-container').style.display = 'none';
        document.querySelector('.message-solicitud').innerHTML = `
            <div style="background: rgba(40,167,69,0.1); border: 1px solid #28a745; padding: 15px; border-radius: 10px; text-align: center;">
                <h4 style="color: #28a745; margin:0">¡Solicitud enviada!</h4>
                <p style="margin:5px 0 0 0; font-size:13px">Revisa tus notificaciones pronto.</p>
            </div>`;
    }
}

function cancelSearch() {
    document.getElementById('results-container').style.display = 'none';
    document.querySelector('.no-equipo-card').style.display = 'block';
}

const botonAlineacion = document.getElementById('guardar-alineacion');
if (botonAlineacion){
    botonAlineacion.addEventListener('click', ()=>{
        guardarAlineacion();
    })
}

function guardarAlineacion(){
    const posiciones = ["portero", "cierre", "ala-izq", "ala-der", "pivot"];
    const data = {};

    posiciones.forEach(posicion => {
        const contenedor = document.querySelector(`.posicion[data-pos="${posicion}"]`);
        const jugador = contenedor.querySelector('.ficha-tactica');
        data[posicion] = jugador ? jugador.id.replace('jugador-','') : null;
    });
    data['equipo_pk'] = equipo_pk;
    enviarAlServidor(data);
}

async function enviarAlServidor(dataAlineacion) {
    try{
        const response = await fetch(`api/alineacion/`,{
            method: 'POST',
            headers:{
                "Content-Type":'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(dataAlineacion)
        });
        const data = await response.json();
        if (data.error){
            console.error(data.error);
            return;
        }
        mostrarErrorToast(data.exito,'exito');
        console.log(data);
    } catch(error){
        console.error(error);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function renderizarAlineacionGuardada() {
    //console.log(alineacionInicial); La alineacionInicial proviene del script del HTML
    Object.keys(alineacionInicial).forEach(posicion => {
        //console.log(posicion)
        const datos = alineacionInicial[posicion];
        //console.log(`Datos: ${datos}`);

        // Si la posición tiene un jugador asignado (id no vacío)
        if (datos.id) {
            const contenedorPosicion = document.querySelector(`.${posicion}`);
            
            if (contenedorPosicion) {
                const fichaHTML = `
                    <div class="ficha-tactica" draggable="true" id="jugador-${datos.id}">
                        <div class="foto-wrapper">
                            <img src="${datos.foto}">
                            <span class="dorsal">#${datos.dorsal}</span>
                        </div>
                        <span class="nombre-jugador">${datos.nombre}</span>
                    </div>
                `;
                contenedorPosicion.innerHTML += fichaHTML;
                
                // Importante: Volver a añadir el evento dragstart a la nueva ficha
                const nuevaFicha = contenedorPosicion.querySelector('.ficha-tactica');
                nuevaFicha.addEventListener('dragstart', e => {
                    nuevaFicha.classList.add('dragging');
                    e.dataTransfer.setData('text/plain', nuevaFicha.id);
                });
                nuevaFicha.addEventListener('dragend', () => nuevaFicha.classList.remove('dragging'));
            }
        }
    });
}

const botonMensaje = document.getElementById('mostrar-mensaje');
const divMessageDanger = document.getElementById('message-danger');

botonMensaje.addEventListener('click', ()=>{
    divMessageDanger.innerHTML = `
        <div class="alerta-premium">
            <div style="font-size: 40px; margin-bottom: 10px;">⚠️</div>
            <h3>¿Estás seguro que deseas abandonar el equipo?</h3>
            <p> 
            Perderás el acceso a estadísticas y calendario de próximos partidos. 
            Esta acción no se puede deshacer.</p>
            <div class="btn-group-alert">
                <button type="button" class="btn-cancelar-top" id="cancelar-salida">Volver atrás</button>
                <button type="button" class="btn-confirmar-top" onclick="abandonarEquipo(${equipo_pk})">Sí, abandonar</button>
            </div>
        </div>
    `;
    botonMensaje.style.display = 'none';

    document.getElementById('cancelar-salida').addEventListener('click',()=>{
        divMessageDanger.innerHTML = ``;
        botonMensaje.style.display = 'block'
    })
})


async function abandonarEquipo() {
    try{
        const response = await fetch(`leaving/team/`);
        const data = await response.json();
        if (data.error){
            alert("Error: " + data.error);
            return;
        }
        
        const alerta = document.querySelector('.alerta-premium');
        alerta.innerHTML = `
            <div style="font-size: 40px; margin-bottom: 10px;">✅</div>
            <h3>¡Hecho!</h3>
            <p>${data.exito}</p>
            <p>Redirigiendo...</p>
        `;

        setTimeout(() => {
            window.location.reload(); 
        }, 1500);
    } catch (e){
        console.error(e);
    }
}

const modal = document.getElementById('modal-jugadores');
const btnAbrir = document.getElementById('jugadoresfree');
const btnCerrar = document.getElementById('cerrar-modal');

async function abrirJugadoresFree() {
    const listaContenedor = document.getElementById('lista-libres')
    modal.style.display = 'block';
    // Limpiamos la lista y ponemos un cargando
    listaContenedor.innerHTML = '<p class="cargando">Buscando jugadores libres...</p>';
    try{
        const response = await fetch('api/show/freeplayer/');
        const data = await response.json();
        if (data.error){
            alert(data.e);
            return;
        }
        if (data.jugadores.length === 0) {
            listaContenedor.innerHTML = '<p>No hay jugadores disponibles en este momento.</p>';
            return;
        }
        // Limpiamos el mensaje de carga antes de iterar
        listaContenedor.innerHTML = '';
        data.jugadores.forEach(jugador => {
            // Desestructuramos la tupla según el orden de values_list en Django:
            // 0:id, 1:first_name, 2:last_name, 3:posicion, 4:foto
            const [id, firstName, lastName, posicion, foto] = jugador;
            // Validamos la foto: si es nula, ponemos la de defecto
            const fotoUrl = foto ? `/media/${foto}` : '/static/img/sin-foto.jpg';
            const item = document.createElement('div');
            item.className = 'jugador-item';
            item.innerHTML = `
                <div class="jugador-info-mini">
                    <img src="${fotoUrl}" class="foto-mini" alt="${firstName}">
                    <div>
                        <span class="nombre-jugador"><strong>${firstName} ${lastName}</strong></span>
                        <br>
                        <small class="posicion-tag">${posicion || 'Sin posición'}</small>
                    </div>
                </div>
                <button class="btn-agregar-jugador" onclick="agregarAlEquipo(${id})">
                    Agregar
                </button>
            `;
            listaContenedor.appendChild(item);
        })
    }catch(e){
        listaContenedor.innerHTML = '<p>Error al conectar con el servidor.</p>';
        console.error(e);
    }
}

function agregarAlEquipo(id_jugador){
    if (webSocketMiEquipo && webSocketMiEquipo.readyState === WebSocket.OPEN){
        webSocketMiEquipo.send(JSON.stringify({
            'equipo_id':equipo_pk,
            'jugador_id':id_jugador,
            'informacion':'capitan'
        }))
    }
}

// Cerrar modal
btnCerrar.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Cerrar si hacen click fuera del cuadro blanco
window.onclick = (event) => {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};

function mostrarErrorToast(mensaje,estilo=null) {
    const contenedor = document.getElementById('message-danger');
    
    // Crear el elemento del toast
    const toast = document.createElement('div');
    if (estilo === 'exito'){
        toast.className = 'toast-exito';    
    } else {
        toast.className = 'toast-error';
    }
    toast.innerHTML = `
        <span class="icon">⚠️</span>
        <span>${mensaje}</span>
    `;

    // Añadir al contenedor
    contenedor.appendChild(toast);

    // Programar la desaparición
    setTimeout(() => {
        toast.classList.add('toast-fade-out');
        // Esperar a que termine la animación de salida para borrarlo del DOM
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }, 3000); // 3000ms = 3 segundos
}