// Login functionality
document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    document.getElementById('loginPage').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
});

// Section navigation
function scrollToSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
    updateNavigation(sectionId);
}

function updateNavigation(sectionId) {
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    document.querySelector(`a[href="#${sectionId}"]`)?.classList.add('active');
}

// Navigation links
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const sectionId = link.getAttribute('href').substring(1);
        scrollToSection(sectionId);
    });
});

// Mobile menu toggle
document.querySelector('.nav-toggle').addEventListener('click', () => {
    document.querySelector('.nav-menu').classList.toggle('active');
});

// Logout
document.getElementById('logout').addEventListener('click', () => {
    document.getElementById('dashboard').classList.add('hidden');
    document.getElementById('loginPage').classList.remove('hidden');
    document.getElementById('loginForm').reset();
});

// Prediction form
document.getElementById('predictionForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const resultBox = document.getElementById('result');
    resultBox.innerHTML = '<h3>Risk Assessment: 45% Low Risk</h3><p>Based on your health metrics, you have a low risk of diabetes. Continue maintaining healthy habits!</p>';
    resultBox.classList.remove('hidden');
});

// Initialize first section
scrollToSection('home');