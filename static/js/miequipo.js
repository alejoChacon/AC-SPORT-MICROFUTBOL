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