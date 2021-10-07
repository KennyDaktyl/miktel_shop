$(document).ready(function () {
    var cart_total_price = $('#cart_total_price');
    var cart_total_price_value = parseFloat(cart_total_price.data('total_price').replace(',', '.')).toFixed(2);
    
    // var total = (parseFloat(cart_total_price_value) + parseFloat(delivery_method)).toFixed(2);

    $('#id_delivery_method').change(function(){
        var delivery_method_price = $('option:selected', this).data('delivery_cost');
        console.log(delivery_method_price);
        cart_total_price.text(((parseFloat(delivery_method_price) + parseFloat(cart_total_price_value)).toFixed(2)) + " PLN");
        console.log(delivery_method_price);
    });
});