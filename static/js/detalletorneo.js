const botonInscribirse = document.querySelector(".btn-inscribirse");
const FormularioInscribir = document.getElementById("inscribir");

botonInscribirse.addEventListener("click", () => {
    FormularioInscribir.style.display = 'block';
    botonInscribirse.style.display = "none";
})

function cancelar(){
    FormularioInscribir.style.display = 'none';
    botonInscribirse.style.display = "block"
}

async function Inscribir(event) {
    event.preventDefault();

    const formulario = FormularioInscribir;

    const formData = new FormData(formulario);

    try{
        const response = await fetch("/api/inscripcion/",{
            method: "POST",
            body:formData
        });
        const data = await response.json();

        if(data.error){
            console.error(data.error);
        }
        formulario.reset();
        cancelar();

        console.log(data.message);
    }catch(error){
        console.error("Ha habido una falla antes de registrar la inscripcion:",error);
    }
}