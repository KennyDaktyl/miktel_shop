$(document).ready(function () {
    window.onbeforeunload = function () {
        window.scrollTo(0, 0);
      }
      
    var navbarTogglerMenu = $('#navbarTogglerMenu');
    var main_nav_icon = $('i.main_nav_icon')
    main_nav_icon.each(function (e) {
        $(this).on("click", function () {
                        main_nav_icon.each(function (e) {
                            $(this).removeClass('red');
                            $(this).removeClass('show');
                            $(this).next().removeClass('show');
                            console.log($(this).next());
                        });
        $(this).addClass('red');
        $(this).addClass('show');
        $(this).next().addClass('show');
        if (nav_main.hasClass('fixed_menu')) {
            $(this).next().css('top', '50px');
            } else {
                $(this).next().css('top', '150px');
            };
        menu_burger.removeClass('red');
        navbarTogglerMenu.removeClass('show');
        });
    });
   
    var menu_burger = $('#menu_burger');
    menu_burger.on("click", function () {
        menu_burger.toggleClass('red');
        main_nav_icon.each(function (e) {
            $(this).removeClass('red');
            $(this).removeClass('show');
            $(this).next().removeClass('show');
            });
        if (nav_main.hasClass('fixed_menu')) {
            $(this).next().css('top', '50px');
            } else {
                $(this).next().css('top', '150px');
            };

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

    var SearchForm = $('#SearchForm');
    var closeSearchInput = $('#closeSearchInput');
    closeSearchInput.on("click", function () {
        SearchForm.removeClass('show');
        main_nav_icon.each(function (e) {
            $(this).removeClass('red');
            $(this).removeClass('show');
        });
    });

    var inputSearch = $('#inputSearch');
    var clearText = $('#clearText');

    inputSearch.keyup(function()
    {
        console.log(this);
    if ($(this).val().length > 0 ) {
        clearText.addClass('show');
        } else {
            clearText.removeClass('show');
        }
    });

    clearText.click(
        function(){
            inputSearch.val('');
            $(this).removeClass('show');
        });

    var nav_main = $('#nav_main');
    var nav_position = nav_main.offset().top;
    
    console.log(nav_position);
    
    $(window).on('scroll', function() {

        nav_main.css('top', '0px');
        var y_scroll_pos = window.pageYOffset;
        var st = $(this).scrollTop();
        var lastScrollTop = 0;
        if ((lastScrollTop < st) && (y_scroll_pos <= nav_position)) {
            nav_main.css('top', nav_position - y_scroll_pos);
            console.log(nav_position - y_scroll_pos);
        };

        if(y_scroll_pos >= nav_position) {
            nav_main.addClass('fixed_menu');
            nav_main.css('top', '0px');
           
        } else {
            nav_main.removeClass('fixed_menu');
            nav_main.css('top', '100px');
        }
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