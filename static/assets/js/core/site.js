"use strict";

(function($) {
    "use strict";

    $('#tbl-equipments').DataTable({
        "dom": 'rtip',
        "pageLength": 20,
        "order": [[1, 'asc']],
        "processing": true,
        "serverSide": true,
        "autoWidth": false,
        "ordering": false,
        "ajax": {
            "url": "/sites/dt/sites",
        },
        "columnDefs": [
            {
                "targets": 0,
                "visible": false
            },
            {
                "targets": 10,
                "className": "text-center",
                "render": function(data, type, row){
                    return `<span class="badge badge-success">Active</span>`;
                }
            },
            {
                "targets": 11,
                "className": "text-center",
                "render": function(data, type, row){
                    return "";
                }
            },
        ]
    });
})(jQuery);
