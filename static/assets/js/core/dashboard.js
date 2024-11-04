"use strict";

(function($) {
    "use strict";

    $('#tbl_dashboard_projects').DataTable({
        "dom": 'rtip',
        "pageLength": 100,
        "order": [[1, 'asc']],
        "processing": true,
        "serverSide": true,
        "autoWidth": false,
        "ordering": false,
        "ajax": {
            "url": "/projects/dt/ongoing-projects",
            "data": function(d){
                d.page = 'dashboard'
            }
        },
        "columnDefs": [
            {
                "targets": 1,
                "render": function(data, type, row){
                    return `                    
                    <h6>${data[0]}</h6>
                    <p>${data[1]}</p>
                    `
                }
            },
            {
                "targets": 2,
                "className": "text-center",
                "render": function(data, type, row){
                    if (data == "ONGOING") {
                        return `<span class="badge badge-info">Ongoing</span>`
                    } else if (data == "COMPLETED") {
                        return `<span class="badge badge-success">Completed</span>`
                    }
                }
            }
        ]
    });
})(jQuery);