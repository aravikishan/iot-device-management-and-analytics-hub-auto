document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });

    const toggleNav = document.querySelector('.toggle-nav');
    if (toggleNav) {
        toggleNav.addEventListener('click', function() {
            const nav = document.querySelector('nav');
            nav.classList.toggle('open');
        });
    }

    // Smooth scrolling
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Example of dynamic content loading
    async function loadDevices() {
        const response = await fetch('/api/devices');
        const devices = await response.json();
        console.log(devices); // Handle the devices data
    }

    loadDevices();
});