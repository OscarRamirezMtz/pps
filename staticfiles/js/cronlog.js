function refreshCronLog() {
    $.ajax({
        url: '/ajax-cron-log/',
        success: function(data) {
            $('#cron-log-content').html(data.cron_log_content);
        },
    });
}

$(document).ready(function() {
    // Refrescar cada 5 segundos (5000 ms)
    setInterval(refreshCronLog, 5000);
});

