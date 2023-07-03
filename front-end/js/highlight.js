let navLinks = document.querySelectorAll("#nav-index a");

for (let link of navLinks) {
    if (link.href === document.URL) {
        link.classList.add("actual");
    }
}

