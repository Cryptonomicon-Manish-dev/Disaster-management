document.addEventListener('DOMContentLoaded', function() {
    const weatherForm = document.getElementById('weatherForm');
    const searchInput = weatherForm.querySelector('input[name="city"]');
    const submitButton = weatherForm.querySelector('button');

    // Add error message for invalid input
    const errorMessage = document.createElement('p');
    errorMessage.className = 'error-message';
    weatherForm.appendChild(errorMessage);

    // Add loading state to form submission
    weatherForm.addEventListener('submit', function(e) {
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        submitButton.disabled = true;

        // Add full-page loading spinner
        const loadingSpinner = document.createElement('div');
        loadingSpinner.className = 'loading-spinner';
        loadingSpinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        document.body.appendChild(loadingSpinner);
        loadingSpinner.style.display = 'flex';
    });

    // Add input validation and auto-capitalize
    searchInput.addEventListener('input', function(e) {
        this.value = this.value.replace(/[0-9]/g, '');
        this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1);

        if (/[0-9]/.test(this.value)) {
            errorMessage.textContent = 'Numbers are not allowed in city names.';
        } else {
            errorMessage.textContent = '';
        }
    });

    // Add weather icons based on condition
    function updateWeatherIcon() {
        const weatherCondition = document.querySelector('.weather-info h3 + p');
        if (weatherCondition) {
            const condition = weatherCondition.textContent.toLowerCase();
            const iconElement = weatherCondition.parentElement.querySelector('.weather-icon');
            
            if (condition.includes('clear')) {
                iconElement.className = 'fas fa-sun weather-icon';
            } else if (condition.includes('rain')) {
                iconElement.className = 'fas fa-cloud-rain weather-icon';
            } else if (condition.includes('cloud')) {
                iconElement.className = 'fas fa-cloud weather-icon';
            } else if (condition.includes('snow')) {
                iconElement.className = 'fas fa-snowflake weather-icon';
            }

            // Highlight active weather condition
            const weatherItems = document.querySelectorAll('.weather-item');
            weatherItems.forEach(item => item.classList.remove('active'));
            const activeItem = weatherCondition.parentElement;
            activeItem.classList.add('active');
        }
    }

    // Run once on page load
    updateWeatherIcon();

    // Add dark mode toggle functionality
    const darkModeToggle = document.createElement('button');
    darkModeToggle.className = 'dark-mode-toggle';
    darkModeToggle.textContent = 'Toggle Dark Mode';
    document.body.appendChild(darkModeToggle);

    // Check and apply saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }

    darkModeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        const isDarkMode = document.body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    });
});
