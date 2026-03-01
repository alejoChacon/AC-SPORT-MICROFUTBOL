document.addEventListener('DOMContentLoaded', () => {
    const jugadores = document.querySelectorAll('.ficha-tactica');
    const posiciones = document.querySelectorAll('.posicion');
    const banquillo = document.getElementById('lista-suplentes');

    // Configurar Arrastre de Jugadores
    jugadores.forEach(jugador => {
        jugador.addEventListener('dragstart', e => {
            jugador.classList.add('dragging');
            e.dataTransfer.setData('text/plain', jugador.id);
        });

        jugador.addEventListener('dragend', () => {
            jugador.classList.remove('dragging');
        });
    });

    // Configurar Zonas de Soltado (Posiciones)
    posiciones.forEach(pos => {
        pos.addEventListener('dragover', e => {
            e.preventDefault();
            pos.style.borderColor = "#ffcc00";
            pos.style.background = "rgba(255, 204, 0, 0.1)";
        });

        pos.addEventListener('dragleave', () => {
            pos.style.borderColor = "rgba(255, 255, 255, 0.3)";
            pos.style.background = "transparent";
        });

        pos.addEventListener('drop', e => {
            e.preventDefault();
            resetPosStyles(pos);
            
            const idJugador = e.dataTransfer.getData('text');
            const jugadorElem = document.getElementById(idJugador);

            // CORRECCIÓN DEL BUG: Si ya hay un jugador, devolverlo al banquillo
            const jugadorExistente = pos.querySelector('.ficha-tactica');
            if (jugadorExistente) {
                banquillo.appendChild(jugadorExistente);
            }

            pos.appendChild(jugadorElem);
        });
    });

    // Permitir devolver jugadores al banquillo arrastrándolos de vuelta
    banquillo.addEventListener('dragover', e => e.preventDefault());
    banquillo.addEventListener('drop', e => {
        e.preventDefault();
        const idJugador = e.dataTransfer.getData('text');
        const jugadorElem = document.getElementById(idJugador);
        banquillo.appendChild(jugadorElem);
    });

    function resetPosStyles(el) {
        el.style.borderColor = "rgba(255, 255, 255, 0.3)";
        el.style.background = "transparent";
    }
});