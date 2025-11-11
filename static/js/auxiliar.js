document.addEventListener("DOMContentLoaded", () => {

    tablaposicion(torneo_pk,'A');
    CargarResultados(torneo_pk,"A");
    CargarPartidos(torneo_pk,"A");

    // Control del submenu
    const submenuBtns = document.querySelectorAll('.submenu-btn'); //Toma todas las pestañas del submenu
    const tabs = document.querySelectorAll('.tab-content'); //Coge todos los div llamados '.tab-content'

    submenuBtns.forEach(btn => { //recorre cada submenu
        btn.addEventListener('click', () => { // Entra a una pestaña del submenu mediante el recorrido y le agrega una accion
            submenuBtns.forEach(b => b.classList.remove('active')); // Borra el active de la clase de cada pestaña
            btn.classList.add('active'); // Pone active a la éstaña que le dimos click
            tabs.forEach(tab => tab.classList.remove('active')); //Borra el active de cada div llamado '.tab-content' (para que no se vea)
            document.getElementById(btn.dataset.tab).classList.add('active'); //Pone active al div que se encuentra por medio del id pero del data-tab
        });
    });

});

//Control de selector de grupo
const grupoBtns = document.querySelectorAll('.grupo-btn');
const tablas = document.querySelectorAll('.tabla-posiciones');

grupoBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        grupoBtns.forEach( b => b.classList.remove('active'));
        btn.classList.add("active");

        // limpiar tabla anterior
        document.getElementById("tabla-ajax").innerHTML = "<p>Cargando...</p>";

        tablaposicion(torneo_pk,btn.dataset.grupo);
        CargarResultados(torneo_pk,btn.dataset.grupo);
        CargarPartidos(torneo_pk,btn.dataset.grupo);

        //tablas.forEach(tabla => tabla.classList.remove('active'));
        //document.querySelector(`.grupo-${btn.dataset.grupo}`).classList.add('active');
    });
});

async function tablaposicion(torneo_pk,grupo) {
    try {
        const response = await fetch(`/torneo/api/posiciones/${torneo_pk}/${grupo}/`);
        const data = await response.json();
        if (data.error){
            alert(`Error: ${data.error}`)
        } else {
            console.log("Tabla Posiciones:",data.equipos) 
            const div = document.getElementById("tabla-ajax");
            if (data.equipos.length === 0) {
            div.innerHTML = `<p class="no-equipos">No hay equipos en el grupo ${grupo}</p>`;
            return;
            }
            let html = `
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Equipo</th>
                        <th>PTS</th>
                        <th>PJ</th>
                        <th>PG</th>
                        <th>PE</th>
                        <th>PP</th>
                        <th>GF</th>
                        <th>GC</th>
                        <th>DF</th>
                    </tr>
                </thead>
                <tbody>
            `;
            data.equipos.forEach((e,i) => {
                html += `
                <tr>
                    <td>${i + 1}</td>
                    <td>${e.equipo}</td>
                    <td>${e.puntos}</td>
                    <td>${e.pj}</td>
                    <td>${e.pg}</td>
                    <td>${e.pe}</td>
                    <td>${e.pp}</td>
                    <td>${e.gf}</td>
                    <td>${e.gc}</td>
                    <td>${e.dg}</td>
                </tr>
                `;
            })
            html += `</tbody></table>`;
            div.innerHTML = html;
        }
    } catch (error) {
        console.error("Error al cargar posiciones:",error);
    }
}

async function CargarResultados(torneo_pk,grupo) {
    try{
        const response = await fetch(`/torneo/api/resultados/${torneo_pk}/${grupo}/`);
        const data = await response.json();
        if (data.error) {
            console.error(data.error);
        } else {
            console.log("Resultados:",data.resultados);
            const div = document.getElementById("ajax-resultados");
            if (data.resultados.length === 0) {
                div.innerHTML = `<p>No hay resultados en el grupo ${grupo}</p>`
                return;
            }
            let html = ``;
            data.resultados.forEach(resultado => {
                html += `
                    <div class="resultado-card">
                        <div class="equipo">
                            <img src="${resultado.equipolocal_escudo}" alt="${resultado.equipolocal_nombre}">
                            <span>${resultado.equipolocal_nombre}</span>
                        </div>
                        <span class="marcador">${resultado.equipolocal_goles} - ${ resultado.equipoVisitante_goles }</span>
                        <div class="equipo">
                            <img src="${ resultado.equipoVisitante_escudo }" alt="${ resultado.equipoVisitante_nombre }">
                            <span>${resultado.equipoVisitante_nombre}</span>
                        </div>
                    </div>
                `;
            })
            div.innerHTML = html;
        }
    } catch (error){
        console.error(error);
    }
}

async function CargarPartidos(torneo_pk,grupo) {
    try{
        const response = await fetch(`/torneo/api/fixture/${torneo_pk}/${grupo}`);
        const data = await response.json();
        if (data.error){
            console.error(data.error);
            return;
        }
        console.log("Partidos:",data.fixtures)
        const div = document.getElementById("ajax-partidos");
        let html = ``;
        data.fixtures.forEach(partido => {
            html += `
                <div class="partido-card">
                    <div class="equipos">
                    <div class="equipo">
                        <img src="${ partido.localteamlogo }" alt="${ partido.localteam}">
                        <span> ${ partido.localteam} </span>
                    </div>
                    <span class="vs">VS</span>
                    <div class="equipo">
                        <img src=" ${partido.awayteamlogo}" alt=" ${ partido.awayteam } ">
                        <span> ${ partido.awayteam } </span>
                    </div>
                    </div>
                    <div class="info">
                    <p><i class="fas fa-calendar-day"></i> ${ partido.fecha_partido }</p>
                    <p><i class="fas fa-map-marker-alt"></i> ${ partido.cancha }</p>
                    </div>
                </div>
            `;
        })
        div.innerHTML = html;
    } catch (error){
        console.error(error)
    }
}