document.addEventListener('DOMContentLoaded', () => {
    const buscarServidorForm = document.getElementById('buscarServidorForm');
    const eliminarServidorForm = document.getElementById('eliminarServidorForm');
    const insertarServidorForm = document.getElementById('insertarServidorForm');



    // Verificar si los formularios existen
    if (!buscarServidorForm || !modificarServidorForm || !eliminarServidorForm || !insertarServidorForm) {
        console.error('Uno o más formularios no se encuentran en el DOM');
        return;
    }




    // Manejar la búsqueda del servidor
    buscarServidorForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        console.log('Formulario de búsqueda enviado');

        const formData = new FormData(buscarServidorForm);
        const data = new URLSearchParams(formData).toString();

        try {
            const response = await fetch('/buscar_servidor', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: data
            });

            if (response.ok) {
                const result = await response.json();
                document.getElementById('nombre_servidor_modificar').value = result.nombre_servidor || '';
                document.getElementById('capacidad_almacenamiento_modificar').value = result.capacidad_almacenamiento || '';
                document.getElementById('sistema_operativo_modificar').value = result.sistema_operativo || '';
                document.getElementById('seguridad_modificar').value = result.seguridad || '';
                document.getElementById('estado_modificar').value = result.estado || '';
                document.getElementById('temperatura_modificar').value = result.temperatura || '';
                document.getElementById('hora_respaldo_modificar').value = result.hora_respaldo || '';

                document.getElementById('resultadoBusqueda').innerHTML = '<p>Datos del servidor cargados en el formulario de modificación.</p>';
            } else {
                document.getElementById('resultadoBusqueda').innerHTML = 'Error al buscar el servidor';
            }
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('resultadoBusqueda').innerHTML = 'Error en la solicitud';
        }
    });








    // Manejar la eliminación del servidor
    document.getElementById('eliminarServidorBtn').addEventListener('click', async () => {
        console.log('Formulario de eliminación enviado');
        const formData = new FormData(eliminarServidorForm);
        const data = new URLSearchParams(formData).toString();

        try {
            const response = await fetch('/eliminar_servidor', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: data
            });

            const result = await response.json();
            document.getElementById('resultadoEliminacion').innerHTML = 'Eliminación realizada';
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('resultadoEliminacion').innerHTML = 'Error en la solicitud';
        }
    });








    // Manejar la inserción del servidor
    document.getElementById('insertarServidorBtn').addEventListener('click', async () => {
        console.log('Formulario de inserción enviado');
        const formData = new FormData(insertarServidorForm);
        const data = new URLSearchParams(formData).toString();

        try {
            const response = await fetch('/insertar_servidor', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: data
            });

            const result = await response.json();
            document.getElementById('resultadoInsercion').innerHTML = result.message || 'Inserción realizada';
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('resultadoInsercion').innerHTML = 'Error en la solicitud';
        }
    });







document.getElementById('modificarServidorBtn').addEventListener('click', async () => {
        const modificarServidorForm = document.getElementById('modificarServidorForm');
        const formData = new FormData(modificarServidorForm);
        const data = new URLSearchParams(formData).toString();

        try {
            const response = await fetch('/modificar_servidor', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: data
            });

            const result = await response.json();
            document.getElementById('resultadoModificacion').innerHTML = result.message;
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('resultadoModificacion').innerHTML = 'Error en la solicitud';
        }
    });







});


