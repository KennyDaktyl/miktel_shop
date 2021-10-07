$(document).ready(function () {
    var cart_total_price = $('#cart_total_price');
    var cart_total_price_value = parseFloat(cart_total_price.data('total_price').replace(',', '.')).toFixed(2);
    
    var delivery_methods = $('.delivery_methods');
    delivery_methods.on("change", function () {
        var delivery_method_price = $(this).data('delivery_cost').replace(',','.');
        cart_total_price.text((parseFloat(delivery_method_price) + parseFloat(cart_total_price_value)).toFixed(2) + " PLN");
    });
});