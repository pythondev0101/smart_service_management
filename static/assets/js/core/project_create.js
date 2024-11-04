$(document).ready(function() {
    var selectedProvinceCode;
    var selectedCityCode;

    var dtSearchRigLine = $('#tbl-search-rig-line').DataTable({
        "dom": 'rtip',
        "fixedColumns": true,
        "select": true,
        "pageLength": 50,
        "order": [[1, 'asc']],
        "processing": true,
        "serverSide": true,
        "autoWidth": false,
        "ordering": false,
        "fnCreatedRow": function( nRow, aData, iDataIndex ) {
            $(nRow).attr('id',  `tr_${aData[0]}`);
        },
        "ajax": {
            "url": "/equipments/dt/equipments",
            "data": function(d){
                d.page = 'search-rig-line-modal'
            }
        },
        "columnDefs": [
            {
                "targets": 0,
                "visible": false
            },
            {
                "targets": 6,
                "className": "text-center",
                "render": function(data, type, row){
                    if (data == "AVAILABLE") {
                        return `<span class="badge badge-success">Available</span>`;
                    } else if (data == "DOWN") {
                        return `<span class="badge badge-danger">Down</span>`;
                    } else if (data == "ACTIVE") {
                        return `<span class="badge badge-primary">Active</span>`;
                    } else {
                        return "";
                    }
                }
            },
            {
                "targets": 7,
                "render": function(data, type, row){
                    return `
                        <button class="btn btn-primary btn-xs btn-select" type="button" data-original-title="btn btn-primary btn-xs" title="">Select</button>
                    `
                }
            }
        ]
    });

    $('#tbl-search-rig-line tbody').on('click', '.btn-select', function () {
        let row = dtSearchRigLine.row($(this).parents('tr')).data();
        let rigLineId = row[0];
        let rigLineName = row[2];

        selectEquipment(this, rigLineId, rigLineName);
    });

    $("#select_rig_line").select2({
        placeholder: "Select..."
    });

    $('#frm_project_create').on('submit', function() {
        $('input, select').prop('disabled', false);
    });

    $("#select_province").change(function(){
        let selected = $(this).find('option:selected');
        let code = selected.attr('code');

        $('#select_city')
        .empty()
        .append('<option value="">Select Barangay</option>');

        if (code == "000"){
            let cities = [
                {"code":"137601000","name":"City of Las Piñas"},
                {"code":"137602000","name":"City of Makati"},
                {"code":"137603000","name":"City of Muntinlupa"},
                {"code":"137604000","name":"City of Parañaque"},
                {"code":"137605000","name":"Pasay City"},
                {"code":"137606000","name":"Pateros"},
                {"code":"137607000","name":"City of Taguig"}
            ]
            cities.sort(function(a, b) {
                return a.name.localeCompare(b.name);
            });

            for (let i=0; i < cities.length; i++){
                let city = cities[i];
                $('#select_city').append($('<option>', {
                    value: city.name,
                    text: city.name,
                    selected: false,
                    code: city.code
                }));
            }
        } else {
            $.getJSON(`https://psgc.gitlab.io/api/provinces/${code}/cities-municipalities`, function(result){
                result.sort(function(a, b) {
                    return a.name.localeCompare(b.name);
                });
    
                for (let i=0; i < result.length; i++){
                    let city = result[i];
                    $('#select_city').append($('<option>', {
                        value: city.name,
                        text: city.name,
                        selected: false,
                        code: city.code
                    }));
                }
            });
        }
    });

    $("#select_city").change(function(){
        let selected = $(this).find('option:selected');
        let code = selected.attr('code');

        $.getJSON(`https://psgc.gitlab.io/api/cities-municipalities/${code}/barangays`, function(result){
            $('#select_barangay')
            .empty()
            .append('<option value="">Select Barangay</option>');

            result.sort(function(a, b) {
                return a.name.localeCompare(b.name);
            });

            for (let i=0; i < result.length; i++){
                let city = result[i];
                $('#select_barangay').append($('<option>', {
                    value: city.name,
                    text: city.name,
                    selected: false,
                    code: city.code
                }));
            }
        });
    });

    // INIT
    loadProjectEquipments(getProjectId());
    loadProvinces();


    function loadProjectEquipments(projectId){
        dtSearchRigLine.ajax.url(`/equipments/dt/equipments?project_id=${projectId}`).load();
        setTimeout(function(){
            $.getJSON(`/api/projects/${projectId}`, function(result){
                for (let i=0; i < result.equipments.length; i++){
                    let equipment = result.equipments[i];
                    let btn_select = $(`#tr_${equipment.id}`).find('.btn-select');
                    let rigLineId = equipment.id;
                    let rigLineName = equipment.machine_id;
                    selectEquipment(btn_select, rigLineId, rigLineName);
                }
            });
        },500);
    }
   
    function getProjectId(){
        let url = $(location).attr('href');
        let parts = url.split("/");
        let lastPart = parts[parts.length-1];
        return lastPart
    }
    
    function selectEquipment(row, rigLineId, rigLineName){
        if ($(row).text() == "Selected"){
            $(row).text("Select");
            $(row).addClass("btn-primary");
            $(row).removeClass("btn-info");
            $(`#select_rig_line option[value='${rigLineId}']`).remove();
            return;
        } else{
            $("#rig_line").val(rigLineId);
            $("#rig_line_name").val(rigLineName);

            $(row).text("Selected");
            $(row).addClass("btn-info");
            $(row).removeClass("btn-primary");
            $('#select_rig_line').append($('<option>', {
                value: rigLineId,
                text: rigLineName,
                selected: true
            }));
        }
    }

    function loadProvinces(){
        $.getJSON(`https://psgc.gitlab.io/api/provinces/`, function(result){
            result.push({"name": "Metro Manila", "code": "000"})

            result.sort(function(a, b) {
                return a.name.localeCompare(b.name);
            });


            for (let i=0; i < result.length; i++){
                let province = result[i];
                $('#select_province').append($('<option>', {
                    value: province.name,
                    text: province.name,
                    selected: false,
                    code: province.code
                }));
            }
        });
    }
});


