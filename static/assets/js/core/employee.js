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
            "url": "/employees/dt/employees",
        },
        "columnDefs": [
            {
                "targets": 0,
                "visible": false
            },
            {
                "targets": 4,
                "className": "text-center",
                "render": function(data, type, row){
                    return `<span class="badge badge-success">Active</span>`;
                }
            },
            {
                "targets": 5,
                "className": "text-center",
                "render": function(data, type, row){
                    return "";
                }
            },
        ]
    });
})(jQuery);
