$(document).ready(function () {
    window.onbeforeunload = function () {
        window.scrollTo(0, 0);
      }

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
        $('body').removeClass('frozen');
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
    intPositionNav = parseInt(nav_main.css('top').replace("px", ""));
    const nav_position_const = nav_position;

    $(window).on('scroll', function() {

        y_scroll_pos = window.pageYOffset;
        nav_position = nav_main.offset().top;
        var st = $(this).scrollTop();
        intPositionNav = parseInt(nav_main.css('top').replace("px", ""));
        
        if (intPositionNav < 100 ) {
            nav_main.css('top', "0px");
        } else {
            if (y_scroll_pos < nav_position_const) {
                nav_main.css('top', nav_position_const - y_scroll_pos + "px");
            };
        };

        if (y_scroll_pos < nav_position_const) {
            nav_main.css('top', nav_position_const - y_scroll_pos + "px");
        };
    });
    

    var nav_main_xl = $('#nav_main_xl');
    var nav_position_xl = nav_main_xl.offset().top;
    intPositionNavXl = parseInt(nav_main_xl.css('top').replace("px", ""));
    const nav_position_xl_const = nav_position_xl;

    $(window).on('scroll', function() {

        y_scroll_pos = window.pageYOffset;
        nav_position_xl = nav_main_xl.offset().top;
        var st = $(this).scrollTop();

        intPositionNavXl = parseInt(nav_main_xl.css('top').replace("px", ""));
       

        if (intPositionNavXl < 50 ) {
            nav_main_xl.css('top', "0px");
        } else {
            if (y_scroll_pos < nav_position_xl_const) {
                nav_main_xl.css('top', nav_position_xl_const - y_scroll_pos + "px");
            };
        };

        if (y_scroll_pos < nav_position_xl_const) {
            nav_main_xl.css('top', nav_position_xl_const - y_scroll_pos + "px");
        };
    });

    var nav_main = $('#nav_main');
    var navbarTogglerMenu = $('#navbarTogglerMenu');
    var main_nav_icon = $('i.main_nav_icon');
    var menu_burger = $('#menu_burger');

    main_nav_icon.each(function (e) {
        $(this).on("click", function () 
                        {
                        main_nav_icon.each(function (e) {
                            $(this).removeClass('red');
                            $(this).removeClass('show');
                            $(this).next().removeClass('show');
                        });
            $(this).addClass('red');
            $(this).addClass('show');
            $(this).next().addClass('show');
            menu_burger.removeClass('red');
            navbarTogglerMenu.removeClass('show');
            // console.log($(this));
            if ($(this).hasClass('show'))
                {
                    $('body').addClass('frozen');
                    console.log("ma");
                } else {
                    $('body').removeClass('frozen');
                    console.log("nie ma");
                }
        });
        // if ($(this).hasClass('show'))
        //  {
        //     $('body').addClass('frozen');
        // } else {
        //     $('body').removeClass('frozen');
        // }
        
    });
    
    menu_burger.on("click", function () {
        navbarTogglerMenu.toggleClass('show');
        menu_burger.toggleClass('red');
        main_nav_icon.each(function (e) {
            $(this).removeClass('red');
            $(this).removeClass('show');
            $(this).next().removeClass('show');
            });
        if (navbarTogglerMenu.hasClass('show')) {
            $('body').addClass('frozen');
        } else {
            $('body').removeClass('frozen');
        }
    });


    var wrapIconInfo = $('#wrapIconInfo');
    var heightwrapIconInfo = wrapIconInfo.css('height');

    var inIconInfo = $('#inIconInfo');
    inIconInfo.css('height', heightwrapIconInfo);

    var iconInfo = $('#iconInfo');
    iconInfo.css('height', heightwrapIconInfo);

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