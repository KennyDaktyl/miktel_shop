$(document).ready(function () {
    window.onbeforeunload = function () {
        window.scrollTo(0, 0);
    }

    var img_corousel_first = $('#carousel0').addClass('active');
    var indicator_corousel_first = $('#indicator0').addClass('active');

    var menuToggle = $('ul.menuToggle');
    menuToggle.each(function (e) {
        $(this).on("click", function () {
            var this_id = $(this).attr('id').replace('cat','');
            var arrow = $('#arrow' + this_id);
            arrow.toggleClass('rotate');
        }); 
    });

    var SearchFormIcon = $('#SearchFormIcon');
    var inputSearch = $('#inputSearch');

    SearchFormIcon.on("click", function () {
        inputSearch.focus();
    });
    
    var SearchForm = $('#SearchForm');
    var closeSearchInput = $('#closeSearchInput');
    closeSearchInput.on("click", function () {
        SearchForm.removeClass('show');
        main_nav_icon.each(function (e) {
            $(this).removeClass('red');
            $(this).removeClass('show');
        });
        // $('body').removeClass('frozen');
    });
    inputSearch
    var clearText = $('#clearText');

    inputSearch.keyup(function()
    {
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

    var header_top = $('#top');
    var nav_main = $('#nav_main');
    intPositionNav = parseInt(nav_main.css('top').replace("px", ""));

    $(window).on('scroll', function() {
        var st = $(this).scrollTop();
       
        if (st > 0) {
            header_top.addClass('fixed_menu');
            nav_main.addClass('fixed_menu'); 
        } 

        if (st < 50) {
            header_top.removeClass('fixed_menu');
            nav_main.removeClass('fixed_menu'); 
        } 
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
       

        if (intPositionNavXl < 80 ) {
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
            if ($(this).hasClass('show'))
                {
                    $('body').addClass('frozen');
                } else {
                    $('body').removeClass('frozen');
                }
        });
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
})