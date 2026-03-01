document.addEventListener("DOMContentLoaded", () => {

    tablaposicion(torneo_pk,'A');

    // Control del submenu
    const submenuBtns = document.querySelectorAll('.submenu-btn'); //Toma todas las pestañas del submenu
    const tabs = document.querySelectorAll('.tab-content'); //Coge todos los div llamados '.tab-content'

    submenuBtns.forEach(btn => { //recorre cada submenu
        btn.addEventListener('click', () => { // Entra a una pestaña del submenu mediante el recorrido y le agrega una accion
            submenuBtns.forEach(b => b.classList.remove('active')); // Borra el active de la clase de cada pestaña
            btn.classList.add('active'); // Pone active a la éstaña que le dimos click
            
            tabs.forEach(tab => tab.classList.remove('active')); //Borra el active de cada div llamado '.tab-content' (para que no se vea)
            const tabId = btn.dataset.tab;
            document.getElementById(btn.dataset.tab).classList.add('active'); //Pone active al div que se encuentra por medio del id pero del data-tab
            
            const grupo = document.querySelector('.grupo-btn.active')?.dataset.grupo || 'A';
//(?) Si el elemento existe, accede a su propiedad . Si no existe, devuelve  sin romper el código.
//(|| 'A') Si lo de la izquierda es , , o vacío, usa  como valor por defecto.
            switch(tabId){
                case 'posiciones':
                    tablaposicion(torneo_pk,grupo);
                    break;
                case 'resultados':
                    const fecha1 = document.getElementById('fechas1').value;
                    console.log("Fecha: ",fecha1);
                    CargarResultados(torneo_pk,grupo,fecha1);
                    break;
                case 'partidos':
                    const fecha2 = document.getElementById('fechas2').value;
                    console.log("Fechas: ",fecha2);
                    CargarPartidos(torneo_pk,grupo,fecha2);
                    break;
                case 'goleadores':
                    CargarJugadores(torneo_pk);
                    break;
            }
        });
    });
});

//Control de selector de grupo
const grupoBtns = document.querySelectorAll('.grupo-btn');
//const tablas = document.querySelectorAll('.tabla-posiciones');

grupoBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        grupoBtns.forEach( b => b.classList.remove('active'));
        btn.classList.add("active");

        //const grupo = btn.dataset.grupo;
        const pestañaActiva = document.querySelector('.submenu-btn.active')?.dataset.tab;

        switch(pestañaActiva){
            case 'posiciones':
                tablaposicion(torneo_pk,btn.dataset.grupo);
                break;
            case 'resultados':
                const fecha1 = document.getElementById('fechas1').value;
                CargarResultados(torneo_pk,btn.dataset.grupo,fecha1);
                break;
            case 'partidos':
                const fecha2 = document.getElementById('fechas2').value;
                CargarPartidos(torneo_pk,btn.dataset.grupo,fecha2);
                break;
            case 'goleadores':
                CargarJugadores(torneo_pk);
                break;
        }
    });
});

//Control de fechas
const selectFechas = document.querySelectorAll('.torneo-select');

selectFechas.forEach(select => {
    select.addEventListener('change', () => {
        const fechaSeleccionada = select.value; // Obtiene el número de la fecha (o "" si es "Cualquier Fecha")
        const grupo_activo = document.querySelector('.grupo-btn.active')?.dataset.grupo || 'A';
        const pestañaActiva = document.querySelector('.submenu-btn.active')?.dataset.tab;
        if (pestañaActiva === 'partidos'){
            CargarPartidos(torneo_pk,grupo_activo,fechaSeleccionada);
        } else if(pestañaActiva === 'resultados'){
            CargarResultados(torneo_pk,grupo_activo,fechaSeleccionada);
        }
    })
})

async function tablaposicion(torneo_pk,grupo) {
    try {
        const response = await fetch(`/torneo/api/posiciones/${torneo_pk}/${grupo}/`);
        const data = await response.json();
        
        console.log("Tabla:",data.equipos);
        const div = document.getElementById("tabla-ajax");
        if (data.error){
            console.error(`Error: ${data.error}`);
            return;
        }
    
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
    } catch (error) {
        console.error("Error al cargar posiciones:",error);
    }
}

async function CargarResultados(torneo_pk,grupo,fecha=null) {
    try{
        const div = document.getElementById("ajax-resultados");
        console.log("Tipo de fecha: ",typeof fecha, "Valor: ",fecha);
        if (fecha === '' || !fecha){
            div.innerHTML = `
                <p style='text-align:center; color:red'>
                    No se han jugado las primeras fechas del torneo. !Recuerda que ya están póoximas a jugarse!
                </p>     
            `;
            return;
        };
        
        const response = await fetch(`/torneo/api/resultados/${torneo_pk}/${grupo}/${fecha}/`);
        const data = await response.json();

        console.log("Resultados:",data.resultados);


        if (data.error) {
            div.innerHTML = `
                <p style='text-align:center; color:red'>
                    ${data.error} 
                </p>
            `;
            console.error(data.error);
            return;
        }

        if (!data.resultados || data.resultados.length === 0) {
            div.innerHTML = `<p>No hay resultados en el grupo ${grupo}</p>`;
            return;
        }

        let html = ``;
        data.resultados.forEach(resultado => {
            html += `
                <div class="resultado-card tarjeta">
                    <div class="resultado-body">
                        <div class="equipo equipo-local">
                            <img src="${resultado.equipolocal_escudo}" alt="${resultado.equipolocal_nombre}">
                            <span>${resultado.equipolocal_nombre}</span>
                        </div>
                        <span class="marcador">${resultado.equipolocal_goles} - ${resultado.equipoVisitante_goles}</span>
                        <div class="equipo equipo-visitante">
                            <img src="${resultado.equipoVisitante_escudo}" alt="${resultado.equipoVisitante_nombre}">
                            <span>${resultado.equipoVisitante_nombre}</span>
                        </div>
                    </div>
                </div>
            `;
        });

        div.innerHTML = html;
    } catch (error){
        console.error("Error al cargar el fixture",error);
    }
}

async function CargarPartidos(torneo_pk,grupo,fecha=null) {
    try{
        const response = await fetch(`/torneo/api/fixture/${torneo_pk}/${grupo}/${fecha}/`);
        const data = await response.json();

        console.table(data.fixtures);

        const div = document.getElementById("ajax-partidos");

        if (data.error){
            div.innerHTML = `
                <p style='text-align:center; color:red'> 
                    ${data.error} 
                </p>
            `;
            return;
        }

        let html = ``;
        data.fixtures.forEach(partido => {
            html += `
                <div class="partido-card">
                    <div class="partido-header">
                        <p><i class="fas fa-calendar-day"></i> ${partido.fecha_partido}</p>
                        <p><i class="fas fa-map-marker-alt"></i> ${partido.cancha}</p>
                    </div>
                    <div class="partido-body">
                        <div class="equipo equipo-local">
                            <img src="${ partido.localteamlogo }" alt="${ partido.localteam }">
                            <span> ${ partido.localteam } </span>
                        </div>
                        <span class="vs">VS</span>
                        <div class="equipo equipo-visitante">
                            <img src=" ${ partido.awayteamlogo }" alt=" ${ partido.awayteam } ">
                            <span> ${ partido.awayteam } </span>
                        </div>
                    </div>
                </div>
            `;
        })
        div.innerHTML = html;
    } catch (error){
        console.error("Error al cargar los partidos:",error)
    }
}

async function CargarJugadores(torneo_pk) {
    try{
        const response = await fetch(`/torneo/api/goleador/${torneo_pk}/`);
        const data = await response.json();

        console.log("Goleadores:",data.goleadores);
        const div = document.getElementById("anotadores");
        if (data.error){
            console.error(data.error);
            return;
        }

        if (!data.goleadores || data.goleadores.length === 0) {
            div.innerHTML = `
                <p style='text-align:center; color:red'>
                    No hay goleadores registrados.
                </p>
            `;
            return;
        }

        let html = `
            <h2 class="titulo-goleadores"> Goleadores destacados</h2>
                <table class="tabla-goleadores">
                    <thead>
                        <tr>
                        <th>#</th>
                        <th>Jugador</th>
                        <th>Equipo</th>
                        <th>Goles</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        data.goleadores.forEach((jugador,i) => {
            html += `
                <tr>
                    <td>${i+1}</td>
                    <td class="jugador-info">
                        <img src="${jugador.foto}" alt="${jugador.nombre}" class="jugador-foto">
                        <span>${jugador.nombre}</span>
                    </td>
                    <td class="equipo-info>
                        <img src="${jugador.escudo}" alt="${jugador.equipo}" class="equipo-escudo">
                        <span>${jugador.equipo}</span>
                    </td>
                    <td><strong>${jugador.goles}</strong></td>
                </tr>
            `;
        })
        html += `</tbody></table>`; 
        div.innerHTML = html;
    } catch(error){
        console.error("Error al cargar los goleadores:",error);
    }
}