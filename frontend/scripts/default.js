document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle'); 
    const navLinksContainer = document.querySelector('.normal-menu'); 
    
    const hamburgerIcon = menuToggle ? menuToggle.querySelector('img') : null;

    if (menuToggle && navLinksContainer) {
        
        menuToggle.addEventListener('click', function() {
            navLinksContainer.classList.toggle('active');

            const isExpanded = navLinksContainer.classList.contains('active');
            menuToggle.setAttribute('aria-expanded', isExpanded);

            if (hamburgerIcon) {
                if (isExpanded) {
                    menuToggle.classList.add('is-open');
                } else {
                    menuToggle.classList.remove('is-open');
                }
            }
        });

document.addEventListener('click', function(event) {
            const isClickInsideMenu = navLinksContainer.contains(event.target);
            const isClickOnToggle = menuToggle.contains(event.target);
            const isMenuOpen = navLinksContainer.classList.contains('active');

            if (isMenuOpen && !isClickInsideMenu && !isClickOnToggle) {
                navLinksContainer.classList.remove('active');
                menuToggle.classList.remove('is-open');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });

    } else {
        console.error("Error");
    }
});

