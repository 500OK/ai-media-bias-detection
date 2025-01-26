document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        // Toggle menu visibility
        mobileMenuButton.addEventListener('click', function (event) {
            event.stopPropagation();
            mobileMenu.classList.toggle('hidden');
            mobileMenu.classList.toggle('block');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function (event) {
            if (!mobileMenu.contains(event.target) &&
                !mobileMenuButton.contains(event.target)) {
                mobileMenu.classList.add('hidden');
                mobileMenu.classList.remove('block');
            }
        });

        // Prevent clicks inside menu from closing it
        mobileMenu.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    } else {
        console.error('Mobile menu elements not found');
    }
}); 