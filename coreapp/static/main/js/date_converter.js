$(document).ready(function () {
    var mainInput = document.getElementsByClassName('input-nepali-date');
    // initiate datepicker only if nepali date class exists
    if(mainInput.length>0){
        mainInput.nepaliDatePicker({  
            ndpMonth: true,
            ndpYear: true,
            language: "english"
        });
    }
});

function fieldDateChange(element) {

    var selector_id = element.getAttribute('id');
    var related_id = element.getAttribute('relatedId');
    if(related_id == null){
        related_id = selector_id.replace('_bs','_ad')
    }

    if (selector_id !== null && related_id !== null) {

        $('#' + selector_id).nepaliDatePicker({
            ndpMonth: true,
            ndpYear: true,
            language: "english",
            onChange: function () {
                var date_bs_string = $('#' + selector_id).val();
                var date_ad_string = get_ad_date_string(date_bs_string);
                $('#' + related_id).val(date_ad_string);
            }
        });

        $('#' + selector_id).change(function () {
            // DateChange('#' + selector_id, '#' + related_id);
            var date_bs_string = $('#' + selector_id).val();
            var date_ad_string = get_ad_date_string(date_bs_string);
            $('#' + related_id).val(date_ad_string);
        });

        $('#' + related_id).change(function () {
            var date_ad_string = $('#' + related_id).val();
            var date_bs_string = get_bs_date_string(date_ad_string);
            $('#' + selector_id).val(date_bs_string);
        });

        var regexname = '^[0-9]*$';

        $('#' + selector_id).keyup(function (e) {
            let selected_value = $('#' + selector_id).val();
            if (e.key === '-' || e.key === '/') {
                if (selected_value.length > 10) {
                    $('#' + selector_id).val(selected_value.substr(0, 10));
                }
            } else {
                if (e.key.match(regexname)) {
                    if (selected_value.length > 10) {
                        $('#' + selector_id).val(selected_value.substr(0, 10));
                    }
                } else {
                    $('#' + selector_id).val(selected_value.substr(0, selected_value.length - 1));
                }
            }
        });
    }
}

function get_ad_date_string(date_bs_string) {
    var date_bs_object = NepaliFunctions.ConvertToDateObject(date_bs_string, "YYYY-MM-DD");
    var date_ad_object = NepaliFunctions.BS2AD(date_bs_object);
    return NepaliFunctions.ConvertDateFormat(date_ad_object, 'YYYY-MM-DD');
}

function get_bs_date_string(date_ad_string) {
    var date_ad_object = NepaliFunctions.ConvertToDateObject(date_ad_string, "YYYY-MM-DD");
    var date_bs_object = NepaliFunctions.AD2BS(date_ad_object);
    return NepaliFunctions.ConvertDateFormat(date_bs_object, 'YYYY-MM-DD');
}