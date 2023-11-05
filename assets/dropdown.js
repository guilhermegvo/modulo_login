// Adicione este código em dropdown.js
document.addEventListener('DOMContentLoaded', function () {
    const dropdown = document.querySelector('.dropdown');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    if (dropdown && dropdownMenu) {
        dropdown.addEventListener('mouseover', () => {
            dropdown.classList.add('show');
        });

        dropdown.addEventListener('mouseout', () => {
            dropdown.classList.remove('show');
        });
    }
});
