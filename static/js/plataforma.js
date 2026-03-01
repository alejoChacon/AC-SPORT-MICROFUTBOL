var url = `ws://${window.location.host}/ws/main/`;
var mainWebsocket = new WebSocket(url);
const notifSound = document.getElementById('notif-sound');

const notifBtn = document.getElementById('notification-btn');
const notifPanel = document.getElementById('notification-panel');
const notifList = document.getElementById('notif-list');
const badge = document.getElementById('notif-badge');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Obtener el token


mainWebsocket.onopen = function(e){
    console.log('Conexión establecida');
}

//datos a obtener
mainWebsocket.onmessage = function(e){
    const data = JSON.parse(e.data);

    // 1. Quitar el mensaje de "No hay mensajes" si existe
    const emptyMsg = notifList.querySelector('.empty-msg');
    if (emptyMsg) emptyMsg.remove();

    // 2. Crear el nuevo elemento de lista
    const li = document.createElement('li');
    li.className = 'notif-item';
    li.id = `notif-${data.notificacion_pk}`
    
    if (data.informacion === 'jugador'){
        // Ajusta 'data.message' según como lo envíe tu backend
        li.innerHTML = `
            <h4><strong>${data.jugador_send_request}</strong> ha solicitado unirse a tu equipo ${data.equipo}</h4>
            <small> Número de solicitud ${data.notificacion_pk} </small>
            <p style="font-size: 11px; color: var(--muted);">¿Te gustaría recibirlo?</p>
            <div class="notif-actions">
                <button type="button" class="btn-notif-accept" onclick="responderSolicitud(${data.equipo_pk},'aceptar',${data.jugador_send_pk},${data.notificacion_pk})">Sí</button>
                <button type="button" class="btn-notif-decline" onclick="responderSolicitud(${data.equipo_pk},'rechazar',${data.jugador_send_pk},${data.notificacion_pk})">No</button>
            </div>
            <span class="time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
        `;
    } else if(data.informacion === 'capitan'){
        console.log(data);
        // Ajusta 'data.message' según como lo envíe tu backend
        li.innerHTML = `
            <h4><strong>${data.capitan}</strong> quiere que tú hagas parte del equipo ${data.equipo}</h4>
            <small> Número de solicitud ${data.notificacion_pk} </small>
            <p style="font-size: 11px; color: var(--muted);">¿Te gustaría aceptar la invitación?</p>
            <div class="notif-actions">
                <button type="button" class="btn-notif-accept" onclick="responderSolicitud(${data.equipo_pk},'aceptar',${data.jugador_id},${data.notificacion_pk})"> Sí </button>
                <button type="button" class="btn-notif-decline" onclick="responderSolicitud(${data.equipo_pk},'rechazar',${data.jugador_id},${data.notificacion_pk})"> No </button>
            </div>
            <span class="time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
        `;
    }

    // 3. Insertar al principio de la lista
    notifList.prepend(li);
    
    if(badge) badge.style.display = 'block';

    window.requestAnimationFrame(() => {
        if(notifSound) {
            notifSound.currentTime = 0;
            notifSound.play().catch(e => console.log("El audio no pudo reproducirse automáticamente debido a políticas del navegador.") );
        }
        document.title = '(1) Nuevo mensaje - AC Sport';
    });
}

// Abrir/Cerrar panel
notifBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    notifPanel.classList.toggle('active');
    
    // Al abrir el panel, limpiamos el badge y el título
    if (notifPanel.classList.contains('active')) {
        badge.style.display = 'none';
        document.title = "AC Sport - Plataforma";
    }
});

// Cerrar panel al hacer clic fuera
document.addEventListener('click', function() {
    notifPanel.classList.remove('active');
});

// Botón Limpiar
document.getElementById('clear-notifs').addEventListener('click', function() {
    notifList.innerHTML = '<li class="empty-msg">No hay mensajes nuevos</li>';
});

//Quitar el punto rojo de la notificacion al darle click
document.getElementById('notification-btn').addEventListener('click',function(){
    const badge = document.getElementById('notif-badge');
    badge.style.display = 'none';
    document.title = "AC Sport - Plataforma";
});

async function responderSolicitud(equipo_id,accion,jugador_pk,notificacion_pk=null) {
    console.log(`Equipo id: ${equipo_id}, Accion: ${accion}, Jugador id: ${jugador_pk}, Notificacion id: ${notificacion_pk}`)
    try{
        const response = await fetch(`/solicitud-equipo/`,{
            method: 'POST',
            headers: {
                'Content-Type' : 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'equipo_pk':equipo_id,
                //'usuario':usuario,
                'usuario_pk':jugador_pk,
                'accion':accion,
                'notificaion_pk':notificacion_pk
            })
        })
        const data = await response.json();
        // --- MAGIA PARA EL MENSAJE ---
        if (data.message) {
            showToast(data.message);
            // Si la acción fue exitosa, removemos el ítem de la lista de notificaciones
            const item = document.getElementById(`notif-${notificacion_pk}`);
            if (item) {
                item.style.opacity = '0';
                setTimeout(() => item.remove(), 300);
            } else{
                console.log('Item no encontrado');
            }
        } else {
            showToast(data.error,'error');
            
            // Si la acción fue exitosa, removemos el ítem de la lista de notificaciones
            const item = document.getElementById(`notif-${notificacion_pk}`);
            if (item) {
                item.style.opacity = '0';
                setTimeout(() => item.remove(), 300);
            } else{
                console.log('Item no encontrado');
            }
        }
    }catch(error){
        console.error(error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const notifList = document.getElementById('notif-list');
    const badge = document.getElementById('notif-badge');
    
    // Si hay items que no sean el mensaje de "vacío", mostrar el badge
    if (notifList.querySelectorAll('.notif-item').length > 0) {
        badge.style.display = 'block';
    }
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