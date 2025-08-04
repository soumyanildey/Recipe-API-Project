// Apply saved theme immediately on page load
const savedTheme = localStorage.getItem('theme') || 'auto';
if (savedTheme !== 'auto') {
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
}

fetch('/frontend/html/navbar.html')
    .then(response => response.text())
    .then(html => {
        document.getElementById('navbar-container').innerHTML = html;

        // Update button icon based on current theme
        const updateButtonIcon = (theme) => {
            const button = document.querySelector('.dropdown-toggle i');
            if (theme === 'light') {
                button.className = 'fas fa-sun';
            } else if (theme === 'dark') {
                button.className = 'fas fa-moon';
            } else {
                button.className = 'fas fa-adjust';
            }
        };

        // Set initial icon
        updateButtonIcon(savedTheme);

        document.querySelectorAll('[data-bs-theme-value]').forEach(toggle => {
            toggle.addEventListener('click', () => {
                const theme = toggle.getAttribute('data-bs-theme-value');
                localStorage.setItem('theme', theme);
                updateButtonIcon(theme);
                if (theme === 'auto') {
                    document.documentElement.removeAttribute('data-bs-theme');
                } else {
                    document.documentElement.setAttribute('data-bs-theme', theme);
                }
            });
        });
    });
