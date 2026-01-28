// ===================================
// MANEJO DE TEMA CLARO/OSCURO
// ===================================

// Detectar preferencia del sistema
function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// Obtener tema guardado o usar preferencia del sistema
function getSavedTheme() {
    const saved = localStorage.getItem('portfolioTheme');
    if (saved) {
        return saved;
    }
    return getSystemTheme();
}

// Aplicar tema
function applyTheme(theme) {
    const html = document.documentElement;
    const toggle = document.getElementById('themeToggle');
    const icon = toggle?.querySelector('.theme-icon');

    if (theme === 'light') {
        html.classList.add('light-mode');
        if (icon) icon.textContent = '🌙';
        localStorage.setItem('portfolioTheme', 'light');
    } else {
        html.classList.remove('light-mode');
        if (icon) icon.textContent = '☀️';
        localStorage.setItem('portfolioTheme', 'dark');
    }
}

// Cambiar tema (función llamada por el botón)
function toggleTheme() {
    const current = localStorage.getItem('portfolioTheme') || getSystemTheme();
    const newTheme = current === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
}

// Escuchar cambios del sistema
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    // Solo aplicar si no hay preferencia guardada
    if (!localStorage.getItem('portfolioTheme')) {
        applyTheme(e.matches ? 'dark' : 'light');
    }
});

// Inicializar tema al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const theme = getSavedTheme();
    applyTheme(theme);
});

// También aplicar inmediatamente si el script se carga después del DOMContentLoaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        const theme = getSavedTheme();
        applyTheme(theme);
    });
} else {
    const theme = getSavedTheme();
    applyTheme(theme);
}
