let counter = 0;
const actPorPagina = 5;
print('hola');

document.addEventListener('DOMContentLoaded', function () {
    load();
});

window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
};

function load() {
    const start = counter;
    const end = counter + actPorPagina;
    counter = end;
    fetch(`/proyectos/actualizaciones?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(data => {
            data.actualizaciones.forEach(agregar_actualizacion);
        });
}

function agregar_actualizacion(data) {
    const actualizacion = document.createElement('div');
    actualizacion.className = 'contenido';
    const proyecto = document.createElement('h4');
    const link = document.createElement('a');
    link.innerHTML = data.proyecto.nombre;
    link.href = `/proyectos/${data.proyecto.nombre}/proyecto`;
    proyecto.append(link);
    actualizacion.append(proyecto);
    const timestamp = document.createElement('p');
    timestamp.className = 'timestamp';
    timestamp.innerHTML = data.fecha;
    actualizacion.append(proyecto)
    const texto = document.createElement('p');
    texto.innerHTML = data.descripcion;
    actualizacion.append(texto);
    if(data.hasOwnproperty('imagen')){
        const logo = document.createElement('div');
        logo.className = 'logop';
        const imagen = document.createElement('img');
        imagen.src = data.imagen.url;
        imagen.id = 'limage';
        imagen.alt = 'My Image'
        logo.append(imagen);
        actualizacion.append(logo);
    }
    const actualizaciones = document.getElementById('actualizaciones');
    actualizaciones.append(actualizacion);
    const space = document.createElement('div');
    space.className = 'space';
    actualizaciones.append(space);
}