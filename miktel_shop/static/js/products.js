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
    var total_price = $('#total_price');
    var total_price_modal = $('#total_price_modal');
    var len = $('#len');
    var len_mobile = $('#len_mobile');
    var add_product = $('#add_product');
    var len_modal = $('#len_modal');


    $('#form').on('keyup keypress', function (e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });

    add_product.on("click", function () {
        var qty = 1;
        $.ajax({
            url: url_address,
            type: "POST",
            data: {
                prod_id: prod_id,
                qty: qty,
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
            $('#add_qty').text(qty + 'szt.');
            console.log(in_stock, $('#in_stock_info').val(in_stock + 'szt.'));

        }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
    });
});