$(document).ready(function () {
    
    if(window.location.pathname.includes('master/user/')){
        changeGroupSelect();
    }
});

$('form').find('input,  select, textarea,number').each(function () {
    
    if($(this).attr('type') !== 'checkbox'){
        $(this).addClass('form-control');
    }

    if($(this).attr('rows') !== 'undefined'){
        // $(this).attr('rows',4);
    }

    if($(this).attr('col')){
        if($(this).attr('type') == 'checkbox'){
            if($(this).attr('col-parent')){
                $(this).parent().parent().parent().parent().addClass($(this).attr('col'));
            }else{
                $(this).parent().parent().parent().addClass($(this).attr('col'));
                $(this).parent().addClass('pt-5 pl-3 font-weight-bold');
            }
        }else{
            $(this).parent().parent().parent().addClass($(this).attr('col'));
        }
    }
    if($(this).hasClass('filter-field')){
        $(this).parent().parent().addClass('col')
    };

});

function changeGroupSelect(element){
    $('#div_id_password').hide()
    $('#div_id_password1').find('ul').hide()

    if (element == undefined){
        group_id =  $('#group_id').val();
        showHideFields(group_id)
    }
    else{
        group_id =  $('#group_id').val();
        showHideFields(group_id)
    }

    function showHideFields(group_id){
        if(group_id == 1 || group_id == 2){
            $('#div_id_expert').show().parent().css('display','block');
            $('#div_id_student,#div_id_program,#div_id_batch').hide().parent().css('display','none');
        }else if(group_id == 3){
            $('#div_id_student').hide().parent().css('display','none');
            $('#div_id_expert,#div_id_program,#div_id_batch').show().parent().css('display','block');
        }else if(group_id == 4){
            $('#div_id_student,#div_id_program,#div_id_batch').hide().parent().css('display','none');
            $('#div_id_expert').show().parent().css('display','block');

        }else if(group_id == 5){
            $('#div_id_student').show().parent().css('display','block');
            $('#div_id_expert,#div_id_program,#div_id_batch').hide().parent().css('display','none');
        }else{
            $('#div_id_student,#div_id_program,#div_id_batch').hide().parent().css('display','none');
            $('#div_id_expert').show().parent().css('display','block');
        }
    }
}



