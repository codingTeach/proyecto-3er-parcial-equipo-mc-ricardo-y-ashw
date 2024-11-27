document.addEventListener("DOMContentLoaded", function () {
    const profilePic = document.querySelector(".profile-pic");
    const dropdownMenu = document.querySelector(".dropdown-menu");
    const header = document.querySelector(".header-container");
    const sidebar = document.querySelector(".sidebar");

    // Mostrar/Ocultar dropdown al hacer clic en la imagen
    profilePic.addEventListener("click", function () {
        //event.stopPropagation(); 

        // Alternar la visibilidad del dropdown
        dropdownMenu.classList.toggle("show");
    });

    // Cerrar el dropdown si se hace clic fuera
    document.addEventListener("click", function (e) {
        if (!profilePic.contains(e.target) && !dropdownMenu.contains(e.target)) {
            dropdownMenu.classList.remove("show");
        }
    });

    const dropdownLinks = dropdownMenu.querySelectorAll('a');
    dropdownLinks.forEach(link => {
        link.addEventListener("click", function(event) {
            event.stopPropagation(); // Evitar que el clic cierre el dropdown
            // Aquí puedes agregar cualquier funcionalidad para los enlaces del menú si es necesario
        });
    });

    // Ajustar el header dinámicamente según el estado del sidebar
    function adjustHeader() {
        if (sidebar.classList.contains("expanded")) {
            header.classList.remove("sidebar-collapsed");
            header.classList.add("sidebar-expanded");
        } else {
            header.classList.remove("sidebar-expanded");
            header.classList.add("sidebar-collapsed");
        }
    }

    // Detectar cambios en el estado del sidebar
    const toggleSidebar = document.querySelector(".toggle-btn");
    if (toggleSidebar) {
        toggleSidebar.addEventListener("click", adjustHeader);
    }

    // Ajustar el header al cargar la página
    adjustHeader();
});
