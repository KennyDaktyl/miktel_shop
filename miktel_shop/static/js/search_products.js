window.addEventListener('DOMContentLoaded', (event) => {
    var form = document.getElementById('search_form');
    var form_action = form.getAttribute('action');
    var search_input = document.getElementById('search');
    var link = document.getElementById('link');
    var div_link = document.getElementById('div_link');
    const domain = location.protocol + '//' + location.host
    const form_url = domain + "/produkty/szukaj_js";

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

    function newPElement(sub_cat_type, name, price, qty){
        var newP = document.createElement("p");
        newP.innerHTML = sub_cat_type + ", <strong class='text-primary'>" + name + "</strong>, " + price + " zł, " + qty;
        newP.classList.add("text-center", "text-dark", "m-0", "p-0");
    return newP;
    };

    function newImageElement(image) {
        var newI = document.createElement("img");
        newI.setAttribute('src', image);
        newI.classList.add("image-fluid", "mini", "mr-2");
        newI.style.height = 'auto';
    return newI;
    }

    function getData(search){
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
                    
                    var sub_cat_type = json[i].sub_category_type['name'];
                    var name = json[i].name;
                    var price = json[i].price;
                    var qty = parseInt(json[i].qty);
                    var image = json[i].image;
                    if (qty == 0) {
                        qty = '<b class="text-danger">Brak</b>'
                    } else {
                        qty = '<b class="text-success">Dostępny</b>'
                    };
                    var newP = newPElement(sub_cat_type, name, price, qty);
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

    function blurElement() {
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
    };

    var j = 1;
    search_input.addEventListener("keyup", function(e){
        if(search_input.value.length > 1) {
            var search = search_input.value;
            getData(search);
            
        } else {
            link.style.display = 'none';
            div_link.style.display ='none';
        };
        // if (e.key === "ArrowDown") {
        //     var aLink = document.querySelectorAll('a.new_a');
        //     aLink.forEach(function(el) {
        //         el.style.background = "white";
        //         });
        //     if (j < aLink.length) {
        //         var firstALink = document.getElementById(j);
        //         firstALink.style.background = "wheat";
        //         }
        //     }
        // if (e.key === "ArrowUp") {
        //     search_input.blur();
        //     var aLink = document.querySelectorAll('a.new_a');
        //     aLink.forEach(function(el) {
        //         el.style.background = "white";
        //         });
        //     if (j > 1) {
        //         j -= 1;
        //     };
        //     var firstALink = document.getElementById(j);
        //     firstALink.style.background = "wheat";
        // };
        // if (e.key === "Enter") {
        //     search_input.blur();
        //     var overALink = document.getElementById(j);
        //     overALink.click();
        // };
    })
}); 



// $(document).keyup(function (e) {

//    


//     if (e.which === 38) {
//         search_input.blur();
//         $('a.new_a').each(function (el) {
//             $(this).css("background", "white")
//         });
//         if (j > 1) {
//             j -= 1;
//         };
//         var first_a = $('#' + j);
//         first_a.css("background", "wheat");
//     };

//     if (e.which === 13) {
//         search_input.blur();
//         $('#' + j).click();
//     };
// });

// var link_mobile = $('#link_mobile');
// var div_link_mobile = $('#div_link_mobile');
// div_link_mobile.css('display', 'none');

// var inputSearch = $('#inputSearch');
// inputSearch.keyup(function (event) {

//     if ($(this).val().length > 1) {
//         var search = $(this).val();

//         function GetSearchResult() {
//             result = "";
//             $.ajax({
//                 url: form_url,
//                 async: true,
//                 type: "GET",
//                 data: {
//                     search: search,
//                     csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
//                 },
//                 dataType: "json",
//                 success: function (data) {
//                     result = JSON.parse(JSON.stringify(data));
//                     link_mobile.text('');
//                     if (result.length > 0) {
//                         link_mobile.css('display', 'flex');
//                         div_link_mobile.css('display', 'flex');
//                         for (var i = 0; i < result.length; i++) {
//                             var lp = i + 1;
//                             var product_url = domain + result[i].product_url;
//                             var new_a = $('<a/>', {
//                                 class: 'new_a mx-auto text-left text-dark border-bottom row d-flex align-items-center row col-12 m-0 p-0',
//                                 value: lp,
//                                 tabindex: lp,
//                                 id: lp,
//                                 href: product_url,
//                             });

//                             // var cat = result[i].sub_category_type.sub_category.category['name'];
//                             var sub_cat = result[i].sub_category_type['name'];
//                             var qty = parseInt(result[i].qty);
//                             if (qty == 0) {
//                                 qty = '<b class="text-danger">Brak</b>'
//                             } else {
//                                 qty = '<b class="text-success">Dostępny</b>'
//                             }
//                             // var sub_cat_type = result[i].sub_category_type['name'];
//                             // var brand = result[i].brand['name'];
//                             var name = result[i].name;
//                             var price = result[i].price;
                            
//                             var new_p = $('<p/>', {
//                                 html: sub_cat + ", " + "<strong class='text-primary'>" + name + "</strong>, " + price + " zł " + qty,
//                                 class: 'text-left text-dark m-0 p-0 pr-2 col-10',
                                

//                             });
                            
//                             var image = result[i].image;
//                             var new_img = $('<img/>', {
//                                 src: image,
//                                 class: 'image-fluid mini pr-2 col-2 m-0',
//                                 style: 'height: auto'

//                             });
//                             new_a.click(function () {
//                                 var url = $(this).attr('href');
//                                 $(location).attr('href',url);
//                             });
//                             new_img.prependTo(new_a);
//                             new_p.appendTo(new_a);
//                             new_a.css('min_height', '30px');
//                             new_a.appendTo(link_mobile);
//                         }
//                     } else {
//                         link_mobile.text('');
//                         link_mobile.css('display', 'none');
//                         div_link_mobile.css('display', 'none');
//                     }
//                 }
//             });
//             return result;
//         }

//         result = GetSearchResult();
//     } else {
//         link_mobile.text('');
//         link_mobile.css('display', 'none');
//         div_link_mobile.css('display', 'none');
//     }
// });
// });