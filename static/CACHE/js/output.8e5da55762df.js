$(document).ready(function(){window.onbeforeunload=function(){window.scrollTo(0,0);}
var img_corousel_first=$('#carousel0').addClass('active');var indicator_corousel_first=$('#indicator0').addClass('active');var menuToggle=$('ul.menuToggle');menuToggle.each(function(e){$(this).on("click",function(){var this_id=$(this).attr('id').replace('cat','');var arrow=$('#arrow'+this_id);arrow.toggleClass('rotate');});});var SearchForm=$('#SearchForm');var closeSearchInput=$('#closeSearchInput');closeSearchInput.on("click",function(){SearchForm.removeClass('show');main_nav_icon.each(function(e){$(this).removeClass('red');$(this).removeClass('show');});});var inputSearch=$('#inputSearch');var clearText=$('#clearText');inputSearch.keyup(function()
{if($(this).val().length>0){clearText.addClass('show');}else{clearText.removeClass('show');}});clearText.click(function(){inputSearch.val('');$(this).removeClass('show');});var header_top=$('#top');var nav_main=$('#nav_main');intPositionNav=parseInt(nav_main.css('top').replace("px",""));$(window).on('scroll',function(){var st=$(this).scrollTop();if(st>0){header_top.addClass('fixed_menu');nav_main.addClass('fixed_menu');}
if(st<50){header_top.removeClass('fixed_menu');nav_main.removeClass('fixed_menu');}});var nav_main_xl=$('#nav_main_xl');var nav_position_xl=nav_main_xl.offset().top;intPositionNavXl=parseInt(nav_main_xl.css('top').replace("px",""));const nav_position_xl_const=nav_position_xl;$(window).on('scroll',function(){y_scroll_pos=window.pageYOffset;nav_position_xl=nav_main_xl.offset().top;var st=$(this).scrollTop();intPositionNavXl=parseInt(nav_main_xl.css('top').replace("px",""));if(intPositionNavXl<80){nav_main_xl.css('top',"0px");}else{if(y_scroll_pos<nav_position_xl_const){nav_main_xl.css('top',nav_position_xl_const-y_scroll_pos+"px");};};if(y_scroll_pos<nav_position_xl_const){nav_main_xl.css('top',nav_position_xl_const-y_scroll_pos+"px");};});var nav_main=$('#nav_main');var navbarTogglerMenu=$('#navbarTogglerMenu');var main_nav_icon=$('i.main_nav_icon');var menu_burger=$('#menu_burger');main_nav_icon.each(function(e){$(this).on("click",function()
{main_nav_icon.each(function(e){$(this).removeClass('red');$(this).removeClass('show');$(this).next().removeClass('show');});$(this).addClass('red');$(this).addClass('show');$(this).next().addClass('show');menu_burger.removeClass('red');navbarTogglerMenu.removeClass('show');if($(this).hasClass('show'))
{$('body').addClass('frozen');console.log("ma");}else{$('body').removeClass('frozen');console.log("nie ma");}});});menu_burger.on("click",function(){navbarTogglerMenu.toggleClass('show');menu_burger.toggleClass('red');main_nav_icon.each(function(e){$(this).removeClass('red');$(this).removeClass('show');$(this).next().removeClass('show');});if(navbarTogglerMenu.hasClass('show')){$('body').addClass('frozen');}else{$('body').removeClass('frozen');}});var wrapIconInfo=$('#wrapIconInfo');var heightwrapIconInfo=wrapIconInfo.css('height');var inIconInfo=$('#inIconInfo');inIconInfo.css('height',heightwrapIconInfo);var iconInfo=$('#iconInfo');iconInfo.css('height',heightwrapIconInfo);});$(document).ready(function(){var form=$('#search_form');var form_action=form.attr('action');var search_input=$('#search');var link=$('#link');var div_link=$('#div_link');div_link.css('display','none');const domain=location.protocol+'//'+location.host
const form_url=domain+"/sklep_online/szukaj_js";search_input.keyup(function(event){if($(this).val().length>1){var search=$(this).val();function GetSearchResult(){result="";$.ajax({url:form_url,async:true,type:"get",data:{search:search,csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()},dataType:"json",success:function(data){result=JSON.parse(JSON.stringify(data));link.text('');if(result.length>0){link.css('display','flex');div_link.css('display','flex');for(var i=0;i<result.length;i++){var lp=i+1;var product_url=domain+result[i].product_url;var new_a=$('<a/>',{class:'new_a mx-auto text-center text-dark border-bottom row d-flex align-items-center row',value:lp,tabindex:lp,id:lp,href:product_url,});var cat=result[i].sub_category_type.sub_category.category['name'];var sub_cat=result[i].sub_category_type.sub_category['name'];var sub_cat_type=result[i].sub_category_type['name'];var name=result[i].name;var price=result[i].price;var new_p=$('<p/>',{html:sub_cat+", "+sub_cat_type+", <strong class='text-primary'>"+name+"</strong>, "+price+" zł",class:'text-center text-dark m-0 p-0',});var image=result[i].image;var new_img=$('<img/>',{src:image,class:'image-fluid mini mr-2',});new_a.click(function(){var url=$(this).attr('href');$(location).attr('href',url);});new_img.prependTo(new_a);new_p.appendTo(new_a);new_a.css('min_height','30px');new_a.appendTo(link);}}else{link.text('');link.css('display','none');div_link.css('display','none');}}});return result;}
result=GetSearchResult();}else{link.css('display','none');div_link.css('display','none');}});var j=-1;$(document).keyup(function(e){if(e.which===40){search_input.blur();$('a.new_a').each(function(el){$(this).css("background","white")});if(j<$('a.new_a').length){j+=1;};var first_a=$('#'+j);first_a.css("background","wheat")};if(e.which===38){search_input.blur();$('a.new_a').each(function(el){$(this).css("background","white")});if(j>1){j-=1;};var first_a=$('#'+j);first_a.css("background","wheat");};if(e.which===13){search_input.blur();$('#'+j).click();};});var link_mobile=$('#link_mobile');var div_link_mobile=$('#div_link_mobile');div_link_mobile.css('display','none');var inputSearch=$('#inputSearch');inputSearch.keyup(function(event){if($(this).val().length>1){var search=$(this).val();function GetSearchResult(){result="";$.ajax({url:form_url,async:true,type:"GET",data:{search:search,csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()},dataType:"json",success:function(data){result=JSON.parse(JSON.stringify(data));console.log(result);link_mobile.text('');if(result.length>0){link_mobile.css('display','flex');div_link_mobile.css('display','flex');for(var i=0;i<result.length;i++){var lp=i+1;var product_url=domain+result[i].product_url;var new_a=$('<a/>',{class:'new_a mx-auto text-center text-dark border-bottom row d-flex align-items-center row',value:lp,tabindex:lp,id:lp,href:product_url,});var sub_cat=result[i].sub_category_type.sub_category['name'];var name=result[i].name;var price=result[i].price;var new_p=$('<p/>',{html:sub_cat+", "+"<strong class='text-primary'>"+name+"</strong>, "+price+" zł",class:'text-center text-dark m-0 p-0',});var image=result[i].image;var new_img=$('<img/>',{src:image,class:'image-fluid mini mr-2',});new_a.click(function(){var url=$(this).attr('href');$(location).attr('href',url);});new_img.prependTo(new_a);new_p.appendTo(new_a);new_a.css('min_height','30px');new_a.appendTo(link_mobile);}}else{link_mobile.text('');link_mobile.css('display','none');div_link_mobile.css('display','none');}}});return result;}
result=GetSearchResult();}else{link_mobile.text('');link_mobile.css('display','none');div_link_mobile.css('display','none');}});});;$(document).ready(function(){window.onbeforeunload=function(){window.scrollTo(0,0);}
var products_div=$('div.product');products_div.each(function(e){$(this).on("mouseover",function(){$(this).children().addClass('show');});$(this).on("mouseout",function(){$(this).children().removeClass('show');});});var url_address='/koszyk/dodaj_produkt/'
var add_product=$('#add_product');var prod_id=$('#prod_id').val();var qty=$('#qty');var total_price=$('#total_price');var total_price_modal=$('#total_price_modal');var len=$('#len');var len_mobile=$('#len_mobile');var add_product=$('#add_product');var len_modal=$('#len_modal');var ifMobile=false;$('#form').on('keyup keypress',function(e){var keyCode=e.keyCode||e.which;if(keyCode===13){e.preventDefault();return false;}});var qty_value=qty.val();qty.bind('keyup change click',function(e){qty_value=$(this).val();});add_product.on("click",function(){$.ajax({url:url_address,type:"POST",data:{prod_id:prod_id,qty:qty_value,csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()},}).done(function(result){console.log(result);var result_js=$.parseJSON(result);var result_total=result_js['total'];result_total=result_total.toFixed(2);total_price.text(result_total+' PLN');total_price_modal.text(result_total+' PLN');len.text(result_js['len']+'szt.');len_mobile.text(result_js['len']);len_modal.text(result_js['len']);in_stock=result_js['in_stock'];$('#qty').val(1);$('#qty').attr({"max":in_stock,"min":1});$('#in_stock_info').text(in_stock+'szt.');$('#add_qty').text(qty_value+'szt.');console.log(qty_value);}).fail(function(xhr,status,err){}).always(function(xhr,status){});});var customizeForDevice=function(){var ua=navigator.userAgent;var checker={iphone:ua.match(/(iPhone|iPod|iPad)/),blackberry:ua.match(/BlackBerry/),android:ua.match(/Android/)};if(checker.android){ifMobile=true;}
else if(checker.iphone){ifMobile=true;}
else if(checker.blackberry){ifMobile=true;}
if(parseInt(screen.width)>=992){ifMobile=true
console.log("ssdfdfd")}else{ifMobile=false};console.log(ifMobile,screen.width);return ifMobile;}
customizeForDevice()
var sub_cat_type=$('#sub_cat_type');var sub_cat=$('#sub_cat');var cat=$('#cat');var ul_submenu=$('ul.SubCat');ul_submenu.each(function(e){if($(this).attr('id').replace('SubMenu','')==cat.val()){if(ifMobile){$(this).addClass('show');}
var active_sub_cat=$('#SubCat'+sub_cat.val());active_sub_cat.css('color','red');$(this).siblings().css('background-color','red');$(this).siblings().css('color','white');}});var customizeForDevice=function(){var ua=navigator.userAgent;var checker={iphone:ua.match(/(iPhone|iPod|iPad)/),blackberry:ua.match(/BlackBerry/),android:ua.match(/Android/)};if(checker.android){ifMobile=true;}
else if(checker.iphone){ifMobile=true;}
else if(checker.blackberry){ifMobile=true;}
else{if(screen.width<=992){ifMobile=true}else{ifMobile=false};}
console.log(ifMobile);return ifMobile;}
customizeForDevice()
var ul_type_menu=$('ul.TypeSubCat');console.log(ifMobile);ul_type_menu.each(function(e){if($(this).attr('id').replace('TypeSubMenu','')==sub_cat.val()){$(this).addClass('show');var active_type_sub_cat=$('#TypeSubCat'+sub_cat_type.val());active_type_sub_cat.css('color','red');console.log($(this).attr('id'),sub_cat.val());};});});;$(document).ready(function(){$('.close-cookies').click(function(){$(this).parent().hide();});});;$(document).ready(function(){$('.close-cookies').click(function(){$(this).parent().hide();});});;document.addEventListener('DOMContentLoaded',function(){cookieconsent.run({"notice_banner_type":"interstitial","consent_type":"implied","palette":"dark","language":"pl","page_load_consent_levels":["strictly-necessary","functionality","tracking","targeting"],"notice_banner_reject_button_hide":false,"preferences_center_close_button_hide":false,"website_privacy_policy_url":"https://serwiswrybnej.pl/polityka-prywatnosci"});});;