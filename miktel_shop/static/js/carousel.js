window.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('carousel0').classList.add('active');
    document.getElementById('indicator0').classList.add('active');
    var wrapIconInfo = document.getElementById('wrapIconInfo');
    var heightwrapIconInfo = wrapIconInfo.offsetHeight;

    var inIconInfo = document.getElementById('inIconInfo');
    inIconInfo.style.height = heightwrapIconInfo + "px";
    
    var iconInfo = document.getElementById('iconInfo');
    iconInfo.style.height = heightwrapIconInfo + "px";
});