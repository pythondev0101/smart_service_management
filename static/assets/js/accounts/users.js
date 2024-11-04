"use strict";

(function($) {
    "use strict";

    $('#users-table').DataTable({
        "dom": 'rtip',
        "pageLength": 20,
        "order": [[1, 'asc']],
        "processing": true,
        "serverSide": true,
        "autoWidth": false,
        "ordering": false,
        "ajax": {
            "url": "/accounts/dt/users",
        },
        "columnDefs": [
            {
                "targets": 0,
                "visible": false
            },
            {
                "targets": 1,
                "render": function(data, type, row){
                    return `                    
                    <a href="/users/${row[0]}">
                        ${data}
                    </a>
                    `
                }
            },
            {
                "targets": 4,
                "render": function(data, type, row){
                    return `
                    <a href="/users/${row[0]}/delete" class="btn btn-danger btn-xs" type="button" data-original-title="btn btn-danger btn-xs" title="">Delete</a>
                    `
                }
            },
        ]
    });
})(jQuery);