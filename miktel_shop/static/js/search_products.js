$(document).ready(function () {

var form = $('#search_form');
var form_action = form.attr('action');
var search_input = $('#search');

var link = $('#link');
var div_link = $('#div_link');
div_link.css('display', 'none');

const domain = location.protocol + '//' + location.host
const form_url = domain + "/produkty/szukaj_js";
search_input.keyup(function (event) {

    if ($(this).val().length > 1) {
        var search = $(this).val();

        function GetSearchResult() {
            result = "";
            $.ajax({
                url: form_url,
                async: true,
                type: "get",
                data: {
                    search: search,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                dataType: "json",
                success: function (data) {
                    result = JSON.parse(JSON.stringify(data));
                    link.text('');
                    console.log(result)
                    if (result.length > 0) {
                        link.css('display', 'flex');
                        div_link.css('display', 'flex');
                        for (var i = 0; i < result.length; i++) {
                            var lp = i + 1;
                            var product_url = domain + result[i].product_url;
                            var new_a = $('<a/>', {
                                class: 'new_a mx-auto text-center text-dark border-bottom row d-flex align-items-center row col-12',
                                value: lp,
                                tabindex: lp,
                                id: lp,
                                href: product_url,
                            });

                            var cat = result[i].sub_category_type.sub_category.category['name'];
                            // var sub_cat = result[i].sub_category_type.sub_category['name'];
                            var sub_cat_type = result[i].sub_category_type['name'];
                            // var brand = result[i].brand['name'];
                            var name = result[i].name;
                            var price = result[i].price;
                            var qty = parseInt(result[i].qty);
                            if (qty == 0) {
                                qty = '<b class="text-danger">Brak</b>'
                            } else {
                                qty = '<b class="text-success">Dostępny</b>'
                            }
                            var new_p = $('<p/>', {
                                html: sub_cat_type + ", <strong class='text-primary'>" + name + "</strong>, " + price + " zł, " + qty,
                                class: 'text-center text-dark m-0 p-0',
                                

                            });
                            
                            var image = result[i].image;
                            var new_img = $('<img/>', {
                                src: image,
                                class: 'image-fluid mini mr-2',
                                style: 'height: auto'

                            });
                            new_a.click(function () {
                                var url = $(this).attr('href');
                                $(location).attr('href',url);
                            });
                            new_img.prependTo(new_a);
                            new_p.appendTo(new_a);
                            new_a.css('min_height', '30px');
                            new_a.appendTo(link);
                        }
                    } else {
                        link.text('');
                        link.css('display', 'none');
                        div_link.css('display', 'none');
                    }
                }
            });
            return result;
        }

        result = GetSearchResult();
    } else {
        link.css('display', 'none');
        div_link.css('display', 'none');
    }
});

var j = -1;


$(document).keyup(function (e) {

    if (e.which === 40) {
        search_input.blur();
        $('a.new_a').each(function (el) {
            $(this).css("background", "white")
        });
        if (j < $('a.new_a').length) {
            j += 1;
        };
        var first_a = $('#' + j);
        first_a.css("background", "wheat")
    };


    if (e.which === 38) {
        search_input.blur();
        $('a.new_a').each(function (el) {
            $(this).css("background", "white")
        });
        if (j > 1) {
            j -= 1;
        };
        var first_a = $('#' + j);
        first_a.css("background", "wheat");
    };

    if (e.which === 13) {
        search_input.blur();
        $('#' + j).click();
    };
});

var link_mobile = $('#link_mobile');
var div_link_mobile = $('#div_link_mobile');
div_link_mobile.css('display', 'none');

var inputSearch = $('#inputSearch');
inputSearch.keyup(function (event) {

    if ($(this).val().length > 1) {
        var search = $(this).val();

        function GetSearchResult() {
            result = "";
            $.ajax({
                url: form_url,
                async: true,
                type: "GET",
                data: {
                    search: search,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                dataType: "json",
                success: function (data) {
                    result = JSON.parse(JSON.stringify(data));
                    link_mobile.text('');
                    if (result.length > 0) {
                        link_mobile.css('display', 'flex');
                        div_link_mobile.css('display', 'flex');
                        for (var i = 0; i < result.length; i++) {
                            var lp = i + 1;
                            var product_url = domain + result[i].product_url;
                            var new_a = $('<a/>', {
                                class: 'new_a mx-auto text-left text-dark border-bottom row d-flex align-items-center row col-12 m-0 p-0',
                                value: lp,
                                tabindex: lp,
                                id: lp,
                                href: product_url,
                            });

                            // var cat = result[i].sub_category_type.sub_category.category['name'];
                            var sub_cat = result[i].sub_category_type['name'];
                            var qty = parseInt(result[i].qty);
                            if (qty == 0) {
                                qty = '<b class="text-danger">Brak</b>'
                            } else {
                                qty = '<b class="text-success">Dostępny</b>'
                            }
                            // var sub_cat_type = result[i].sub_category_type['name'];
                            // var brand = result[i].brand['name'];
                            var name = result[i].name;
                            var price = result[i].price;
                            
                            var new_p = $('<p/>', {
                                html: sub_cat + ", " + "<strong class='text-primary'>" + name + "</strong>, " + price + " zł " + qty,
                                class: 'text-left text-dark m-0 p-0 pr-2 col-10',
                                

                            });
                            
                            var image = result[i].image;
                            var new_img = $('<img/>', {
                                src: image,
                                class: 'image-fluid mini pr-2 col-2 m-0',
                                style: 'height: auto'

                            });
                            new_a.click(function () {
                                var url = $(this).attr('href');
                                $(location).attr('href',url);
                            });
                            new_img.prependTo(new_a);
                            new_p.appendTo(new_a);
                            new_a.css('min_height', '30px');
                            new_a.appendTo(link_mobile);
                        }
                    } else {
                        link_mobile.text('');
                        link_mobile.css('display', 'none');
                        div_link_mobile.css('display', 'none');
                    }
                }
            });
            return result;
        }

        result = GetSearchResult();
    } else {
        link_mobile.text('');
        link_mobile.css('display', 'none');
        div_link_mobile.css('display', 'none');
    }
});


});