let navLinks = document.querySelectorAll("#menu-principal a");

for (let link of navLinks) {
    if (link.href === window.location.href.split('?')[0]) {
        link.classList.add("actual");
    }
}

var tabla = document.getElementById("app");

tabla.addEventListener("mouseover", resaltarFila, false);
tabla.addEventListener("mouseout", desResaltarFila, false);

function resaltarFila (event)
{
    if( event.target.classList.contains('killer') ) {
        event.target.closest('tr').classList.add("borrar");
    }
}

function desResaltarFila (event)
{
    if( event.target.classList.contains('killer') ) {
        event.target.closest('tr').classList.remove("borrar");
    }
}