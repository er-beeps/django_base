let CUSTOMJS = {
    validate: (wrapperElement) => {
        let valid = true;
        $(wrapperElement).find('input, select, textarea,number').each(function () {
            /**
             * Validate if element has required attribute and no value/input given
             */
            if ($(this).attr('required') !== undefined && $(this).val() === "") {
                valid = false;
                $(this).addClass('is-invalid');
                if ($(this).next().hasClass('select2')) {
                    $(this).next().addClass('is-invalid');
                }
                const newElement = $("<span style='color:red;'>").text("This Field is Required.");
                $(this).after(newElement);
            }else if($(this).attr('data-min_length') !== undefined && $(this).val().length <= $(this).data('min_length')){
                valid = false;
                $(this).addClass('is-invalid');
                const newElement = $("<span style='color:red;'>").text(`minimum of ${$(this).data('min_length')} char required `);
                $(this).after(newElement);
            }
            else {
                $(this).removeClass('is-invalid');
            }
        });

        return valid;
    },
    tmpLoading: (text='Saving...',bool) => {
        let status = bool === true ? 'show' : 'hide';
        $.LoadingOverlay(status, { text:text });
    },

    reloadList: (item) => {
        let updateUrl;
        let params = {};

        let form = item.form;
        let slug;

        if(form){
            slug = form.getAttribute('slug');
        }else{
           let paths = location.pathname.split('/')
           slug = paths[paths[paths.length -1]]
        }

        let field = item.name;
        let value;
        if(field == 'page'){
            value = item.getAttribute('value');
        }else{
            value = item.value;
        }

        updateUrl = window.location.origin + window.location.pathname;
        fullUrl = window.location.href;

        // check if current url already contains some query parameters
        // if it contains , then just append the next parameters 
        if (fullUrl.includes("?")) {

            //check if the field already exists in current url
            // if exits just update the field value, and do not append to url
            if (fullUrl.includes(field)) {
                old_search_params = new URLSearchParams(location.search);

                //check if the selected field has value or not
                // if field value is empty, just remove the paramter from url
                if (value) {
                    old_search_params.set(field, value);
                    new_search_params = '?' + old_search_params.toString();
                } else {
                    old_search_params.delete(field);
                    new_search_params = old_search_params.toString();
                    //if new search params in empty, remove '?' from url
                    if (new_search_params != "") { 
                        new_search_params = '?' + new_search_params;
                    }
                }

                updateUrl = updateUrl + new_search_params;

            } else {
                updateUrl = fullUrl + '&' + field + '=' + value;
            }
            history.pushState({}, null, updateUrl);
            params = Object.fromEntries(new URLSearchParams(location.search));
            loadDatatableList(slug,params);
        } else {
            // if current url doesnot contains any query parameters, then add new paramaters
            if(value){
                updateUrl = updateUrl + '?' + field + '=' + value;
                history.pushState({}, null, updateUrl);
                params = Object.fromEntries(new URLSearchParams(location.search));
                loadDatatableList(slug, params);

            }
        }
        
    },

    clearFilter: (item) => {
        let slug = item.getAttribute('slug');

        if (slug != '' && window.location.href.includes('?')) {
            updateUrl = window.location.origin + window.location.pathname;
            
            $('.filter-field').val('').trigger('change');
            history.pushState({}, null, updateUrl);
            if(slug == 'exam_application'){
                location.reload();
            }else{
                loadDatatableList(slug);
            }
        }
    }
}
window.CUSTOMJS = CUSTOMJS;
