window.addEventListener('DOMContentLoaded', (event) => {
    var form = document.getElementById('search_form');
    var form_action = form.getAttribute('action');
    var search_input = document.getElementById('search');
    var link = document.getElementById('link');
    var div_link = document.getElementById('div_link');
    const domain = location.protocol + '//' + location.host
    const form_url = domain + "/produkty/szukaj_js";
    var clearText = document.getElementById('clearText');

    function newAElement(lp, product_url) {
        var newA = document.createElement("a");
        newA.classList.add("new_a", "mx-auto", "text-center", "text-dark", "border-bottom", "row", "d-flex", "align-items-center", "col-12");
        newA.setAttribute("id", lp);
        newA.value = lp;
        newA.setAttribute("href", product_url);
        newA.tabindex = lp;
        newA.style.min_height = '30px';
    return newA;  
    };

    function newPElement(name, price, qty){
        var newP = document.createElement("p");
        newP.innerHTML = "<strong class='text-primary'>" + name + "</strong>, " + price + " zł, " + qty;
        newP.classList.add("text-center", "text-dark", "m-0", "p-0", "col-10");
    return newP;
    };

    function newImageElement(image) {
        var newI = document.createElement("img");
        newI.setAttribute('src', image);
        newI.classList.add("image-fluid", "mini", "m-0", "p-0", "col-2");
        newI.style.height = '35px';
        newI.style.width = 'auto';
    return newI;
    }

    function getData(search, link, div_link){
        fetch(form_url + "?search=" + search, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                    },
        },
        ).then(response => {
        if (response.ok) {
            response.json().then(json => {
            if (json.length > 0) {
                div_link.classList.add("bg-white", "search_link", "border", "row");
                div_link.classList.remove('d-none');
                div_link.style.display = 'flex';
                link.innerHTML = '';
                for (var i = 0; i < json.length; i++) {
                    var lp = i + 1;
                    var product_url = domain + json[i].product_url;
                    var newA = newAElement(lp, product_url);
                    
                    // var sub_cat_type = json[i].sub_category_type['name'];
                    var name = json[i].name;
                    var price = json[i].price;
                    var qty = parseInt(json[i].qty);
                    var image = json[i].image;
                    if (qty == 0) {
                        qty = '<b class="text-danger">Brak</b>'
                    } else {
                        qty = '<b class="text-success">Dostępny</b>'
                    };
                    var newP = newPElement(name, price, qty);
                    var newImage = newImageElement(image);
                    newA.appendChild(newImage);
                    newA.appendChild(newP);
                    link.appendChild(newA);
                    }
                    link.style.display = 'flex';
            }
            else 
            {
                link.innerHTML = '';
                div_link.style.display = 'none';
                link.style.display = 'none';
            }
            });
        }
     });
    }
    search_input.addEventListener("keyup", function(e){
        if(search_input.value.length > 1) {
            var search = search_input.value;
            getData(search, link, div_link);
            
        } else {
            link.style.display = 'none';
            div_link.style.display ='none';
        };
     })

    var link_mobile = document.getElementById('link_mobile');
    var div_link_mobile = document.getElementById('div_link_mobile');
    div_link_mobile.style.display = 'none';
    var search_input_mobile = document.getElementById('inputSearch');
    
    search_input_mobile.addEventListener("keyup", function (e) {
        if (search_input_mobile.value.length > 1) {
            var search = search_input_mobile.value;
            getData(search, link_mobile, div_link_mobile);
            clearText.classList.add('show');
        } else {
            link_mobile.style.display = 'none';
            div_link_mobile.style.display = 'none';
            clearText.classList.remove('show');
        };
    });

    var SearchFormIcon = document.getElementById('SearchFormIcon');
    var SearchForm = document.getElementById('SearchForm');
    var main_nav_icon = document.querySelectorAll('i.main_nav_icon');
    SearchFormIcon.addEventListener("click", function (e) {
        inputSearch.focus();
    });
    clearText.addEventListener('click', function (e) {
        search_input_mobile.value = '';
        clearText.classList.remove('show');
        link.innerHTML = '';
    });
    var closeSearchInput = document.getElementById('closeSearchInput');
    closeSearchInput.addEventListener("click", function (e) {
        SearchForm.classList.remove('show');
        search_input_mobile.value = '';
        main_nav_icon.forEach(function (el) {
            el.classList.remove('red');
            el.classList.remove('show');
        });
        link.innerHTML = '';
        document.querySelector('body').classList.remove('frozen');
    });
}); 
