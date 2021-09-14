$(document).ready(function () {
    // var top = $('#top');
    // var nav = $('#nav');
    // var page = $('#page');
    // var footer = $('#footer');
    // var link_map = $('#link_map');
    // var navbarTogglerDemo03 = $('#navbarTogglerDemo03');

    // top_height = top.height();
    // nav_height = nav.height();
    // link_map_height = link_map.height();
   
    var menu_burger = $('#menu_burger');
    menu_burger.on("click", function () {
        menu_burger.toggleClass('red');
    });


    var arrow_keys = $('#arrow_keys');
    arrow_keys.on("click", function () {
        arrow_keys.toggleClass('rotate');
    });

    var arrow_stamp = $('#arrow_stamp');
    arrow_stamp.on("click", function () {
        arrow_stamp.toggleClass('rotate');
    });

    var arrow_grav = $('#arrow_grav');
    arrow_grav.on("click", function () {
        arrow_grav.toggleClass('rotate');
    });


    // var lastY;
    // $(window).bind('touchmove', function (e) {
    //     var currentY = e.originalEvent.touches[0].clientY;
    //     if (currentY > lastY) {
    //         top.removeClass('scroll_down');
    //         nav.removeClass('active');
    //     } else if (currentY < lastY) {
    //         top.addClass('scroll_down');
    //         nav.addClass('active');
    //     }
    //     lastY = currentY;
    // });

    // function refreshPage() {
    //     var page_y = $(document).scrollTop();
    //     window.location.href = window.location.href + '?page_y=' + page_y;
    // }
    // document.addEventListener("DOMContentLoaded", function (event) {
    //     var scrollpos = localStorage.getItem('scrollpos');
    //     if (scrollpos) window.scrollTo(0, scrollpos);
    // });

    // window.onbeforeunload = function (e) {
    //     localStorage.setItem('scrollpos', window.scrollY);
    // };

    // var dropdown_basket = $('#dropdown_basket');
    // var basket_div = $('#basket_div');
    // dropdown_basket.click(function () {
    //     basket_div.toggleClass('show');

    // });
})