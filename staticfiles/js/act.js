// update_servers.js

$(document).ready(function () {
    var selectedOrig = $('#id_server_origen').val();
    var selectedDest = $('#id_server_destino').val();

    function updateServerChoices() {
        $.ajax({
            url: '/actualiza/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                // Guardar las selecciones actuales
                var selectedOrig = $('#id_server_origen').val();
                var selectedDest = $('#id_server_destino').val();

                // Limpiar y actualizar las opciones de los servidores
                $('#id_server_origen').empty();
                $('#id_server_destino').empty();
                $.each(data, function (index, server) {
                    $('#id_server_origen').append($('<option>', {
                        value: server.id,
                        text: server.nombre
                    }));
                    $('#id_server_destino').append($('<option>', {
                        value: server.id,
                        text: server.nombre
                    }));
                });

                // Restaurar las selecciones después de la actualización
                $('#id_server_origen').val(selectedOrig);
                $('#id_server_destino').val(selectedDest);
            }
        });
    }

    // Llamar a la función al cargar la página y cada 10 segundos
    updateServerChoices();
    setInterval(updateServerChoices, 10000);  // Actualizar cada 10 segundos
});
