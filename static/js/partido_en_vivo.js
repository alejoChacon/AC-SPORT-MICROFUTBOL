const DURACION_TIEMPO = 20 * 60;

let tiempoActual = 0;
let tiempoRestante = localStorage.getItem('match_timer') ? parseInt(localStorage.getItem('match_timer')) : tiempoActual;
let isRunning = localStorage.getItem('timer_running') === 'true';
let timerInterval;
let currentPeriod = localStorage.getItem('currentPeriod') ? parseInt(localStorage.getItem('currentPeriod')) : 1; //Primer tiempo = 1, segundo tiempo = 2

const display = document.getElementById('timer-display');
const btnPlayPause = document.getElementById('btn-play-pause');
const btnReset = document.getElementById('btn-reset-period');
const periodDisplay = document.querySelector('.period');
const botonGuardarActa = document.getElementById('btn-finalizar');
const botonPausarYSalir = document.querySelector('.auxiliar');

const csrftoken3 = getCookie("csrftoken");

const sonidoArbitrofalta = document.getElementById('arbitro-falta');

function updatePeriodText() {
    if (currentPeriod === 1){
        periodDisplay.textContent = '1er Tiempo';
    } else if (currentPeriod === 2){
        periodDisplay.textContent = '2do Tiempo';
    }
}

function updateDisplay() {
    let minutes = Math.floor(tiempoRestante / 60);
    let seconds = tiempoRestante % 60;
    display.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

    // Guardar en persistencia
    localStorage.setItem('match_timer', tiempoRestante);

    //Mientras el partido está en juego vamos a quitar el boton de Guardar Acta
    botonGuardarActa.style.display = 'none';

    if (tiempoRestante === DURACION_TIEMPO) {
        pauseTimer();
        sonidoArbitrofalta.play();
        alert("¡Final del tiempo!");

        if (currentPeriod === 1){
            // Crear Boton dinamico para iniciar el segundo tiempo
            const btnSecondhalf = document.createElement('button');
            btnSecondhalf.textContent = `Iniciar 2do Tiempo`
            btnSecondhalf.classList.add('btn-timer-ctrl');

            //insertar el boton en el DOM
            document.querySelector('.timer-controls').appendChild(btnSecondhalf);

            // Evento para reiniciar el cronometro
            btnSecondhalf.addEventListener('click', ()=> {
                localStorage.setItem('currentPeriod',2);
                currentPeriod = 2;
                tiempoRestante = tiempoActual;
                updatePeriodText();
                updateDisplay();
                startTimer()
                btnSecondhalf.remove(); //Quitar el boton después de usarlo
            })
        } else if (currentPeriod === 2){
            botonGuardarActa.style.display = 'flex';
            botonPausarYSalir.style.display = 'none';
        }
    }
}

function startTimer() {
    if (!isRunning) {
        isRunning = true;
        localStorage.setItem('timer_running', 'true');
        btnPlayPause.innerHTML = '<i class="fa-solid fa-pause"></i>';
        display.classList.remove('paused');
        
        timerInterval = setInterval(() => {
            tiempoRestante++;
            updateDisplay();
        }, 1000);
    }
}

function pauseTimer() {
    isRunning = false;
    localStorage.setItem('timer_running', 'false');
    btnPlayPause.innerHTML = '<i class="fa-solid fa-play"></i>';
    display.classList.add('paused');
    clearInterval(timerInterval);
}

btnPlayPause.addEventListener('click', () => {
    if (isRunning) pauseTimer();
    else startTimer();
});

btnReset.addEventListener('click', () => {
    if (confirm("¿Reiniciar el cronómetro de este tiempo?")) {
        pauseTimer();
        tiempoRestante = tiempoActual;
        updateDisplay();
    }
});

// Inicialización al cargar página
updateDisplay();
if (isRunning) {
    isRunning = false; // Reset temporal para que startTimer funcione
    startTimer();
} else {
    display.classList.add('paused');
}


async function accion(jugador_id,accion,locacion){
    try{
        let minuto = Math.floor(tiempoRestante / 60);
        const response = await fetch(`/../api/partido-en-vivo/`,{
            method : 'POST',
            headers : {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken3
            },
            body: JSON.stringify(
                {
                    'partido_id': partido_id,
                    'jugador_id': jugador_id,
                    'accion': accion,
                    'minuto': minuto,
                    'periodo': currentPeriod,
                    'locacion': locacion
                })
        });
        const data = await response.json();
        mostrarSucesosDelPartido(data.message);
        if (accion === 'gol'){
            marcadorEnVivo();
        }
    } catch(e){
        console.error(`Error al enviar el gol: ${e}`)
    }
}

function getCookie(name) {
    let cookieArr = document.cookie.split(";"); // separa todas las cookies

    for (let cookie of cookieArr) {
        let c = cookie.trim(); // quita espacios
        if (c.startsWith(name + "=")) {
            return c.substring(name.length + 1); // devuelve el valor
        }
    }
    return null; // si no existe
}

updatePeriodText();
mostrarSucesosDelPartidoIniciandoPartido();

function mostrarSucesosDelPartido(lista){
    
    const divChan = document.querySelector('.timeline-box');
    let html = ``;
    lista.forEach(incidente => {
        if (incidente.tipo === 'gol'){
            html += `
                <div class="event-record">
                    <span class="evt-min">  ${incidente.minuto}'</span>
                    <i class="fa-solid fa-futbol" style="color: var(--accent);"></i>
                    <span class="evt-desc">Gol de <b> ${incidente.jugador} </b> (${incidente.equipo})</span>
                    <button class="btn-delete-evt" onclick="eliminarSucesoDelPartido(${incidente.pk},'gol')"> &times; </button>
                </div>
            `;
        } else if(incidente.tipo === 'amarilla'){
            html += `
                <div class="event-record">
                    <span class="evt-min"> ${incidente.minuto}' </span>
                    <div class="card-mini yellow"></div>
                    <span class="evt-desc">Amarilla para <b> ${incidente.jugador} </b></span>
                    <button class="btn-delete-evt" onclick="eliminarSucesoDelPartido(${incidente.pk})">&times;</button>
                </div>
            `;
        } else if(incidente.tipo === 'azul'){
            html += `
                <div class="event-record">
                    <span class="evt-min"> ${incidente.minuto}' </span>
                    <div class="card-mini blue"></div>
                    <span class="evt-desc">Azul para <b> ${incidente.jugador} </b></span>
                    <button class="btn-delete-evt" onclick="eliminarSucesoDelPartido(${incidente.pk})">&times;</button>
                </div>
            `;
        } else if(incidente.tipo === 'roja'){
            html += `
                <div class="event-record">
                    <span class="evt-min"> ${incidente.minuto}' </span>
                    <div class="card-mini red"></div>
                    <span class="evt-desc">Roja para <b> ${incidente.jugador} </b></span>
                    <button class="btn-delete-evt" onclick="eliminarSucesoDelPartido(${incidente.pk})">&times;</button>
                </div>
            `;
        }
    });
    divChan.innerHTML = html;
}

async function eliminarSucesoDelPartido(pk,accion=null) {
    try {
        const response = await fetch(`/../api/deleting-sucesos-en-vivo/`,{
            method:'POST',
            headers:{
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken3,
            },
            body: JSON.stringify({
                'incidencia_pk':pk,
                'partido_pk':partido_id
            })
        });
        const data = await response.json();
        console.log(data);
        mostrarSucesosDelPartido(data.datos);
        if (accion === 'gol'){
            marcadorEnVivo();
        }    
    } catch(e){
        console.error("Error al enviar los datos: ",e);
    }
}

async function marcadorEnVivo() {
    try{
        let marcador_local = document.getElementById('score-local');
        let marcador_visitante = document.getElementById('score-visitante');
        const response = await fetch(`/../api/marcador-en-vivo/${partido_id}/`);
        const data = await response.json();
        marcador_local.innerHTML = `${data.dato.marcador_local}`;
        marcador_visitante.innerHTML = `${data.dato.marcador_visitante}`;
    } catch(e){
        console.error('Error al obtener los datos: ',e)
    }
}

async function guardarActa() {
    try{
        let segundosRestantes = 5;
        const alerta = document.getElementById('message-alerta');

        botonGuardarActa.style.display = 'none';

        const respone = await fetch(`/../api/saving-acta/game-live/`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken3
            },
            body: JSON.stringify({
                'partido_pk':partido_id
            })
        });
        const data = await respone.json();
        console.log(data);

        if (data.exito){
            
            alerta.classList.add('show');
            alerta.innerHTML = `¡Acta guardada! Redirigiendo en <b>${segundosRestantes}</b> segundos...`;
            
            //Actualizar el contador cada segundo usando setInterval
            const intervalo = setInterval( ()=>{
                segundosRestantes --;
                alerta.innerHTML = `¡Acta guardada! Redirigiendo en <b>${segundosRestantes}</b> segundos...`;
                
                if (segundosRestantes<=0){
                    clearInterval(intervalo); //Detiene el reloj
                } 
            },1000)

            mostrarNotificacion(data.exito);

            setTimeout(()=>{
                window.location.href = `${data.url}`;
            },5000)

        } else if (data.error){
            alerta.classList.remove('show');
            mostrarNotificacion(data.error);
            return;
        }
    } catch(e){
        console.error('Error antes de guardar el acta: ',e);
    }
}

function mostrarNotificacion(mensaje) {
    const alerta = document.getElementById('message-guardar-acta');
    
    // 1. Insertar el mensaje
    alerta.textContent = mensaje;
    
    // 2. Mostrar la paleta añadiendo la clase CSS
    alerta.classList.add('show');
    
    // 3. Ocultarla automáticamente después de 3 segundos
    setTimeout(() => {
        alerta.classList.remove('show');
    }, 3000);
}

async function mostrarSucesosDelPartidoIniciandoPartido() {
    try{
        const response = await fetch(`/../api/incidencia-partido/${partido_id}/`);
        const data = await response.json();
        if (data.message){
            mostrarSucesosDelPartido(data.message);
        }
    } catch(e){
        console.error(e);
    }
}