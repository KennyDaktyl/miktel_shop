window.addEventListener('DOMContentLoaded', (event) => {
    var nav_main = document.getElementById('nav_main');
    var navbarTogglerMenu = document.getElementById('navbarTogglerMenu');
    var main_nav_icon = document.querySelectorAll('i.main_nav_icon');
    var menu_burger = document.getElementById('menu_burger');
    var body = document.querySelector('body');

    menu_burger.addEventListener("click", function (e) {
        navbarTogglerMenu.classList.toggle('show');
        menu_burger.classList.toggle('red');
        main_nav_icon.forEach(function (el) {
            el.classList.remove('red');
            el.classList.remove('show');
        });
        if (navbarTogglerMenu.classList.contains('show')) {
            body.classList.add('frozen');
        } else {
            body.classList.remove('frozen');
        }
    });

    main_nav_icon.forEach(function (el) {
        el.addEventListener("click", function (e) 
            {
            main_nav_icon.forEach(function (el) {
                el.classList.remove('red');
                el.classList.remove('show');
            });
            el.classList.add('red');
            el.classList.add('show');
            menu_burger.classList.remove('red');
            navbarTogglerMenu.classList.remove('show');
            if (el.classList.contains('show'))
                {
                body.classList.add('frozen');
            } else {
                body.classList.remove('frozen');
            }
        });
    });
    
    var menuToggle = document.querySelectorAll('ul.menuToggle');
    menuToggle.forEach(function (el) {
        el.addEventListener("click", function (e) {
            var el_id = el.getAttribute('id').replace('cat', '');
            var arrow = document.getElementById('arrow' + el_id);
            arrow.classList.toggle('rotate');
        })
    });

    window.onbeforeunload = function () {
        window.scrollTo(0, 0);
    }
    var header_top = document.getElementById('top');
    var nav_main = document.getElementById('nav_main');
    var nav_main_xl = document.getElementById('nav_main_xl');

    intPositionNav = parseInt(nav_main.style.top.replace("px", ""));
    window.addEventListener('scroll', function (e) {
        y_scroll_pos = window.pageYOffset;
        if (y_scroll_pos > 0) {
            header_top.classList.add('fixed_menu');
            nav_main.classList.add('fixed_menu');

        }
        if (y_scroll_pos < 50) {
            header_top.classList.remove('fixed_menu');
            nav_main.classList.remove('fixed_menu');
            nav_main_xl.style.top = "0px";
        }
    });

    var nav_main_xl = document.getElementById('nav_main_xl');
    var nav_position_xl = nav_main_xl.offsetTop;
    intPositionNavXl = parseInt(nav_main_xl.style.top.replace("px", ""));
    var nav_position_xl_const = nav_position_xl;

    window.addEventListener('scroll', function (e) {
        y_scroll_pos = window.pageYOffset;
        nav_position_xl = nav_main_xl.offsetTop;
        intPositionNavXl = parseInt(nav_main_xl.style.top.replace("px", ""));
        if (intPositionNavXl < 50) {
            nav_main_xl.style.top = "0px";
        } else {
            if (y_scroll_pos < nav_position_xl_const) {
                nav_main_xl.style.top = nav_position_xl_const - y_scroll_pos + "px";
            };
        };

        if (y_scroll_pos < nav_position_xl_const) {
            nav_main_xl.style.top = nav_position_xl_const - y_scroll_pos + "px";
        };
    });
    document.addEventListener('keyup', pageDown);
    function pageDown(e) {
        if (e.keyCode === 34) {
            header_top.classList.add('fixed_menu');
            nav_main.classList.add('fixed_menu');
            nav_main_xl.style.top = "0px";
        }
        if (e.keyCode === 33) {
            header_top.classList.remove('fixed_menu');
            nav_main.classList.remove('fixed_menu');
        }
    };
});
