const modalActa = document.getElementById('modal-acta');
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-upload');

function abrirCargaActa(matchId) {
    // Aquí podrías hacer fetch para traer nombres de equipos reales
    modalActa.classList.add('active');
}

function cerrarModal() {
    modalActa.classList.remove('active');
}

// Upload Drag & Drop simulado
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#cba241';
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'rgba(255,255,255,0.1)';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#4ade80';
    dropZone.querySelector('p').innerText = "Archivo listo para subir";
    dropZone.querySelector('i').className = "fa-solid fa-check";
});