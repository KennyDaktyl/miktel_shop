$(document).ready(function () {

    var email_input = $('#id_email');
    function isEmail(email) {
        var EmailRegex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        return EmailRegex.test(email);
      }

    var postCode_input = $('#id_zip_code');
    function isPostCode(postCode) {
        var PostCodeRegEx = /^\d{2}-\d{3}$/;
        return PostCodeRegEx.test(postCode);
    }

    var nip_number = $('#id_nip_number');
    function isVat(vatNumber) {
        var vatNumberRegEx = /^\d{10}$/;
        return vatNumberRegEx.test(vatNumber);
    }

    var input_password = $('#id_password');
    var show_password = $('#show_password');
    var input_field = $('.input-group input');

    show_password.on("mousedown", function () 
    {
        if('password' == input_password.attr('type')){
            input_password.prop('type', 'text');

       } else {
            input_password.prop('type', 'password');
       }
    });

    var input_password2 = $('#id_password2');
    var show_password2 = $('#show_password2');

    

    show_password2.on("mousedown", function () 
    {
        if('password' == input_password2.attr('type')){
            input_password2.prop('type', 'text');
       } else {
            input_password2.prop('type', 'password');
       };
    });

    input_password2.keyup(function(){
        if ($(this).val() === input_password.val()) {
            $(this).removeClass('table-danger');
            input_password.removeClass('table-danger');

            input_password.addClass('table-success');
            $(this).addClass('table-success');
            } else {
                $(this).removeClass('table-success');
                input_password.removeClass('table-seccess');
                input_password.addClass('table-danger');
                $(this).addClass('table-danger');
        }
    });

    input_field.keyup(function() {
        if (($(this).val().length === 0) && ($(this).attr('required') === 'required') && ($(this).attr('id') != "id_zip_code") && $(this).attr('id') != "id_email") { //if password field is empty            
            
            $(this).removeClass('table-success');
            $(this).addClass('table-danger');
            console.log($(this).attr('id'));

        } else {
            $(this).removeClass('table-danger');
            $(this).addClass('table-success');
            console.log($(this).attr('id'));
        }
    });

    email_input.keyup(function(){
        if (isEmail($(this).val())) {
            email_input.removeClass('table-danger');
            email_input.addClass('table-success');
        } else {
            email_input.removeClass('table-success');
            email_input.addClass('table-danger');
        }
    });

    

    postCode_input.keyup(function(){
        if (isPostCode($(this).val())) {
            postCode_input.removeClass('table-danger');
            postCode_input.addClass('table-success');
        } else {
            postCode_input.removeClass('table-success');
            postCode_input.addClass('table-danger');
        }
    });

    nip_number.keyup(function(){
        if (isVat($(this).val())) {
            nip_number.removeClass('table-danger');
            nip_number.addClass('table-success');
        } else {
            nip_number.removeClass('table-success');
            nip_number.addClass('table-danger');
        }
    });

    if (input_password.val() === input_password2.val()) {
        input_password.removeClass('table-danger');
        input_password2.removeClass('table-danger');
        input_password.addClass('table-success');
        input_password2.addClass('table-success');
         } else {
        input_password.removeClass('table-success');
        input_password.removeClass('table-seccess');
        input_password2.addClass('table-danger');
        input_password2.addClass('table-danger');
    }

    input_password2.keyup(function(){
        if ($(this).val() === input_password.val()) {
            $(this).removeClass('table-danger');
            input_password.removeClass('table-danger');

            input_password.addClass('table-success');
            $(this).addClass('table-success');
            } else {
                $(this).removeClass('table-success');
                input_password.removeClass('table-seccess');
                input_password.addClass('table-danger');
                $(this).addClass('table-danger');
        }
    });

    console.log(input_password.val(), input_password2.val())
});