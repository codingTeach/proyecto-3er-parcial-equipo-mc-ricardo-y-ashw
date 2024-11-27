
// Función para alternar el estado del sidebar (expandido o colapsado)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const contentContainer = document.getElementById('content-container');

    if (!sidebar || !contentContainer) return; // Verifica que ambos elementos existen
    
    // Alternar las clases para expandir o colapsar
    sidebar.classList.toggle('collapsed');
    sidebar.classList.toggle('expanded');
    
    // Ajustar el margen del contenido cuando el sidebar cambia de tamaño
    if (sidebar.classList.contains('collapsed')) {
        contentContainer.style.marginLeft = '80px'; // Ajuste para sidebar colapsado
    } else {
        contentContainer.style.marginLeft = '250px'; // Ajuste para sidebar expandido
    }
    
    // Guardar el estado en localStorage
    const state = sidebar.classList.contains('collapsed') ? 'collapsed' : 'expanded';
    localStorage.setItem('sidebarState', state);
}

// Al cargar la página, verificar el estado guardado y ajustar el sidebar
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const contentContainer = document.getElementById('content-container');

    if (!sidebar || !contentContainer) return;  // Evita errores si los elementos no existen
    
    // Obtener el estado guardado en localStorage
    const sidebarState = localStorage.getItem('sidebarState');

    // Establecer el estado del sidebar basado en lo almacenado
    if (sidebarState === 'collapsed') {
        sidebar.classList.add('collapsed');
        sidebar.classList.remove('expanded');
        contentContainer.style.marginLeft = '80px'; // Ajustar el margen cuando está colapsado
    } else {
        sidebar.classList.add('expanded');
        sidebar.classList.remove('collapsed');
        contentContainer.style.marginLeft = '250px'; // Ajustar el margen cuando está expandido
    }
});
