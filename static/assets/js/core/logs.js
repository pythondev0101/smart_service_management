"use strict";

(function($) {
    "use strict";

    $('#logs-table').DataTable({
        "dom": 'rtip',
        "pageLength": 20,
        "order": [[1, 'asc']],
        "processing": true,
        "serverSide": true,
        "autoWidth": false,
        "ordering": false,
        "ajax": {
            "url": "/logs/dt/logs",
        },
        "columnDefs": [
            {
                "targets": 0,
                "visible": false
            }
        ]
    });
})(jQuery);