"use strict";

(function($) {
    "use strict";

    $('#tbl-ongoing-projects').DataTable({
        "dom": 'rtip',
        "pageLength": 20,
        "order": [[1, 'asc']],
        "processing": true,
        "serverSide": true,
        "autoWidth": false,
        "ordering": false,
        "ajax": {
            "url": "/projects/dt/ongoing-projects",
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
                    <a href="/projects/${row[0]}">
                        <h6>${data[0]}</h6>
                    </a>
                    <p>${data[1]}</p>
                    `
                }
            },
            {
                "targets": 8,
                "className": "text-center",
                "render": function(data, type, row){
                    if (data == "ONGOING") {
                        return `<span class="badge badge-info">Ongoing</span>`
                    } else if (data == "COMPLETED") {
                        return `<span class="badge badge-success">Completed</span>`
                    }
                }
            },
        ]
    });
})(jQuery);
