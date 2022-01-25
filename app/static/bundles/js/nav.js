const nav_toggle = document.getElementById("nav-toggle");
const nav_menu = document.getElementById("nav-menu");
nav_toggle.onclick = function() {
    nav_menu.classList.toggle("active");
};
