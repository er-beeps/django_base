$(document).ready(function () {

    var district_lc;
    var district_prm;
    var local_level_lc;
    var local_level_prm;
    let entry_id = $('#entry_id').val();
    if (entry_id) {
        $.ajax({
            url: '/master/get-district-locallevel/' + entry_id,
            type: "GET",
            success: function (data) {
                if (data.length > 0) {
                    district_prm = data[0].district_id;
                    district_lc = data[0].district_id;
                    local_level_prm = data[0].local_level_id;
                    local_level_lc = data[0].local_level_id;
                }
            }
        });
    }
    else {
        $("#id_district_prm").empty().append('<option value="">--Select Province First--</option>')
        $("#id_district_lc").empty().append('<option value="">--Select Province First--</option>')
        $("#id_local_level_prm").empty().append('<option value="">--Select District First--</option>')
        $("#id_local_level_lc").empty().append('<option value="">--Select District First--</option>')
    }
    $.urlParam = function (name) {
        try {
            var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
            return results[1] || 0;
        } catch {
            return null;
        }
    }

    setTimeout(() => {
        $("#id_province").trigger("change");
    }, 500);
    $('#id_province_lc').on('change', function () {
        getDistrict(this, district_lc);
    });
    $('#id_province_prm').on('change', function () {
        getDistrict(this, district_prm);
    });
    $('#id_district_lc').on('change', function () {
        getLocallevel(this, local_level_lc);
    });
    $('#id_district_prm').on('change', function () {
        getLocallevel(this, local_level_prm);
    });
});
function getDistrict(elem, x) {
    var districtName = ($(elem).attr('id')).replace('province', 'district');
    var locallevelName = ($(elem).attr('id')).replace('province', 'local_level');
    var districtSelectName = districtName.replace("id_", "");
    var stateID = $(elem).val();
    $('#' + districtName).append('<option value="">-- Loading...  --</option>');

    if (stateID) {
        $.ajax({
            url: '/master/get-districts/' + stateID,
            type: "GET",
            dataType: "json",
            success: function (data) {

                if (data) {
                    $('#' + districtName).empty().append('<option value="">--Select District--</option>');
                    $('#' + locallevelName).empty().append('<option value="">--Select District First--</option>');
                    var selected_id = x;
                    $.each(data, function (key, value) {
                        var selected = "";
                        if (selected_id == value.id) {
                            selected = "SELECTED";
                        }
                        $("select[name=" + districtSelectName + "]").append('<option class="form-control" value="' + value.id + '" ' + selected + '>' + value.name_en + '</option>');
                        if (selected == "") {
                            $('#' + districtName).trigger("change");
                            $('#' + locallevelName).trigger("change");
                        }
                    });
                } else {
                    $('#' + districtName).empty();
                    $('#' + locallevelName).empty();
                }
            }
        });
    } else {
        $('#' + districtName).empty().append('<option value="">--Select District--</option>');
        $('#' + locallevelName).empty().append('<option value="">--Select District First--</option>');
    }
};
function getLocallevel(elem, y) {
    var locallevelName = ($(elem).attr('id')).replace('district', 'local_level');
    var locallevelSelectName = locallevelName.replace("id_", "");
    var districtID = $(elem).val();

    if (districtID) {
        $('#' + locallevelName).append('<option value="">-- Loading...  --</option>');
        $.ajax({
            url: '/master/get-local-levels/' + districtID,
            type: "GET",
            dataType: "json",
            success: function (data) {
                if (data) {
                    $('#' + locallevelName).empty().append('<option value="">-- Select Local Level --</option>');
                    var selected_id = y;
                    $.each(data, function (key, value) {
                        var selected = "";
                        if (selected_id == value.id) {
                            selected = "SELECTED";
                        }
                        $(("select[name=" + locallevelSelectName + "]")).append('<option class="form-control" value="' + value.id + '" ' + selected + '>' + value.name_en + '</option>');
                        if (selected == "") {
                            $('#' + locallevelName).trigger("change");
                        }
                    });
                } else {
                    $('#' + locallevelName).empty();
                }
            }
        });
    } else {
        $('#' + locallevelName).empty().append('<option value="">-- Select District First--</option>');
    }
};



