function abrirMenu() {
    var x = document.getElementById("nav-index");
    if (x.className === "nav") {
        x.classList.add("responsive");
    } else {
        x.className = "nav";
    }
}