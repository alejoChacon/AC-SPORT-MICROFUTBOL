document.addEventListener('DOMContentLoaded',()=>{

})

async function confirmacionInscripcion(inscripcion_pk,accion,boton) {    
    try{
        const fila = boton.closest('tr');
        const accionesContenedor = fila.querySelector('.acciones-celda');
        const contenedorMensaje = fila.querySelector('.message');
        // Feedback inmediato: deshabilitar botones
        const botones = accionesContenedor.querySelectorAll('button');
        botones.forEach(b => b.disabled = true);
        
        boton.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i>';
        const response = await fetch(`/api/validacion-inscripcion/`,{
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                'inscripcion_pk':inscripcion_pk,
                'accion':accion
            })
        })
        const data = await response.json();
        if (data.exito || data.message){
            // Animación de salida de los botones
            botones.forEach(b => {
                b.style.opacity = '0';
                setTimeout(() => b.style.display = 'none', 300);
                });
            // Aplicar estilo según acción
            fila.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            if (accion === 'aceptar'){
                fila.style.background = 'rgba(34, 197, 94, 0.05)';
                contenedorMensaje.innerHTML = `<span class="badge-status success"><i class="fas fa-check-double"></i> ${data.exito} </span>`
            } else {
                console.log('Aquí entro');
                fila.style.background = 'rgba(239, 68, 68, 0.08)';
                contenedorMensaje.innerHTML = `<span class="badge-status error"><i class="fas fa-times-circle"></i> ${data.message} </span>`;
            }
            equiposInscritos();
        } else if (data.error) {
            mostrarErrorToast(data.error, 'error');
            boton.disabled = false;
            boton.innerHTML = accion === 'aceptar' ? '<i class="fas fa-check"></i>' : '<i class="fas fa-times"></i>';
        }
    } catch(e){
        console.error("Error crítico:", e);
        mostrarErrorToast("No se pudo conectar con el servidor.", "error");
    }
}

const botonMostrar = document.querySelector('.btn-programar');
if (botonMostrar){
    botonMostrar.addEventListener('click',()=>{
        document.getElementById('formulario').style.display = 'block';
        document.getElementById('parrafito').style.display = 'none';
        botonMostrar.style.display = `none`;
    })
}

async function estadoTorneo(event){
    try{
        event.preventDefault();
        const formulario = document.getElementById('formulario');
        const formData = new FormData(formulario);
        const response = await fetch("../../api/torneo-estado/",{
            method: "POST",
            body: formData
        });
        const data = await response.json();
        if(data.error){
            mostrarErrorToast(data.error,'error');
            return;
        }
        mostrarErrorToast(data.exito,'exito');
        setTimeout(()=>{
            window.location.href = data.url;
        },3500)

    } catch(e){
        console.error(e);
    }
}

function cancelar(){
    document.getElementById('formulario').style.display = 'none';
    document.querySelector('.btn-programar').style.display = 'block';
    document.getElementById('parrafito').style.display = 'block';
}

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

async function equiposInscritos() {
    console.log(torneo_id)
    try{
        const containerEquiposGrid = document.querySelector('.equipos-grid');
        const response = await fetch(`/../../api/equipos-inscritos/${torneo_id}/`);
        const data = await response.json();
        console.log(data);
        if (data.error){
            containerEquiposGrid.innerHTML = `
                <p class="mensaje-vacio">${data.error}</p>
            `;
            return;
        }
        let html = ``;
        data.equipos.forEach(equipo => {
            html += `
                <div class="equipo-mini">
                    <img src="${equipo.foto}" alt="${equipo.nombre}">
                    <p>${equipo.nombre}</p>
                </div>
            `;
        })
        containerEquiposGrid.innerHTML = html;
    } catch(e){
        console.error(e);
    }
}

document.addEventListener('DOMContentLoaded',()=>{
    equiposInscritos();
})