// static/js/dashboard.js
document.addEventListener('DOMContentLoaded', function() {
    // Example: Toggle visibility of elements
    const toggleButton = document.getElementById('toggle-button');
    const contentToToggle = document.getElementById('toggle-content');

    toggleButton.addEventListener('click', () => {
        contentToToggle.style.display = contentToToggle.style.display === 'none' ? 'block' : 'none';
    });

    // More interactive features can be added here
});
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar', // or 'line', 'pie', etc.
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                ...
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                ...
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
