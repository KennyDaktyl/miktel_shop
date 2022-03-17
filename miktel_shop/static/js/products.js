$(document).ready(function () {
    window.onbeforeunload = function () {
        window.scrollTo(0, 0);
    }

    var products_div = $('div.product');

    products_div.each(function (e) {
        $(this).on("mouseover", function () {
            $(this).children().addClass('show');
        });

        $(this).on("mouseout", function () {
            $(this).children().removeClass('show');
        });
    }); 

    var url_address = '/koszyk/dodaj_produkt/'
    var add_product = $('#add_product');
    var prod_id = $('#prod_id').val();
    var qty = $('#qty');
    var total_price = $('#total_price');
    var total_price_modal = $('#total_price_modal');
    var len = $('#len');
    var len_mobile = $('#len_mobile');
    var add_product = $('#add_product');
    var len_modal = $('#len_modal');
    var ifMobile = false;

    $('#form').on('keyup keypress', function (e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });

    var qty_value = qty.val();
    qty.bind('keyup change click', function (e) {
       qty_value = $(this).val(); 
    });

    console.log('OK');
    add_product.on("click", function () {
        console.log('OK-2');
        $.ajax({
            url: url_address,
            type: "POST",
            data: {
                prod_id: prod_id,
                qty: qty_value,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
        }).done(function (result) {
            var result_js = $.parseJSON(result);
            var result_total = result_js['total'];
            result_total = result_total.toFixed(2);
            total_price.text(result_total+' PLN');
            total_price_modal.text(result_total+' PLN');
            len.text(result_js['len'] + 'szt.');
            len_mobile.text(result_js['len']);
            len_modal.text(result_js['len']);
            in_stock = result_js['in_stock'];
            $('#qty').val(1);
            $('#qty').attr({
                "max": in_stock,
                "min": 1
            });
            $('#in_stock_info').text(in_stock + 'szt.');
            $('#add_qty').text(qty_value + 'szt.');

        }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
    });

    var customizeForDevice = function(){
        var ua = navigator.userAgent;
        var checker = {
          iphone: ua.match(/(iPhone|iPod|iPad)/),
          blackberry: ua.match(/BlackBerry/),
          android: ua.match(/Android/)
        };
        if (checker.android){
            ifMobile = true;
        }
        else if (checker.iphone){
            ifMobile = true;
        }
        else if (checker.blackberry){
            ifMobile = true;
        }
        
        if (parseInt(screen.width) >= 992 ) {
            ifMobile = true
            } else {
                ifMobile=false
            };
        return ifMobile;
    }
    customizeForDevice()    

    var sub_cat_type = $('#sub_cat_type');
    var sub_cat = $('#sub_cat');
    var cat = $('#cat');
    var ul_submenu = $('ul.SubCat');
    
    ul_submenu.each(function (e) {
        if ($(this).attr('id').replace('SubMenu', '') == cat.val()) {
            if (ifMobile) {
                $(this).addClass('show');
            } 
            var active_sub_cat = $('#SubCat' + sub_cat.val());
            active_sub_cat.css('color', 'red');
            $(this).siblings().css('background-color', 'red');
            $(this).siblings().css('color', 'white');
        }
    }); 

    var customizeForDevice = function(){
        var ua = navigator.userAgent;
        var checker = {
          iphone: ua.match(/(iPhone|iPod|iPad)/),
          blackberry: ua.match(/BlackBerry/),
          android: ua.match(/Android/)
        };
        if (checker.android){
            ifMobile = true;
        }
        else if (checker.iphone){
            ifMobile = true;
        }
        else if (checker.blackberry){
            ifMobile = true;
        }
        else {
            if( screen.width <= 992 ) {ifMobile = true} else {ifMobile=false};
        }
        return ifMobile;
    }
    customizeForDevice()    
    
    var ul_type_menu = $('ul.TypeSubCat');
    ul_type_menu.each(function (e) {
        if ($(this).attr('id').replace('TypeSubMenu', '') == sub_cat.val()) {
            $(this).addClass('show');
            var active_type_sub_cat = $('#TypeSubCat' + sub_cat_type.val());
            active_type_sub_cat.css('color', 'red');
        };
    }); 
});


// products_div.forEach(function (el) {
//     el.addEventListener("mouseover", function (e) {
//         // el.children.ClassList.add('show');
//         var showOption = el.querySelectorAll(":scope > showOption");
//         console.log(showOption);
//     });

//     el.addEventListener("mouseout", function (e) {
//         el.children.ClassList.remove('show');
//     });
// });

// var url_address = '/koszyk/dodaj_produkt/'
// var add_product = document.getElementById('add_product');
// var prod_id = document.getElementById('prod_id').value;
// var qty = document.getElementById('qty');
// var total_price = document.getElementById('total_price');
// var total_price_modal = document.getElementById('total_price_modal');
// var len = document.getElementById('len');
// var len_mobile = document.getElementById('len_mobile');
// var add_product = document.getElementById('add_product');
// var len_modal = document.getElementById('len_modal');
// var ifMobile = false;