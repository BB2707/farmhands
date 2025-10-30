// This event listener ensures that the script runs only after the entire
// HTML document has been loaded and parsed.
document.addEventListener('DOMContentLoaded', () => {

    // --- Weekly Growth Chart (Bar Chart) ---
    // Get the canvas element from the HTML
    const growthCtx = document.getElementById('growthChart').getContext('2d');
    
    // Create a new bar chart instance
    const growthChart = new Chart(growthCtx, {
        type: 'bar',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
            datasets: [{
                label: 'Height (cm)',
                data: [5, 12, 19, 25, 32, 40],
                backgroundColor: 'rgba(42, 157, 143, 0.6)',
                borderColor: 'rgba(42, 157, 143, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // --- Crop Distribution Chart (Pie Chart) ---
    // Get the canvas element for the pie chart
    const pieCtx = document.getElementById('cropPieChart').getContext('2d');

    // Create a new pie chart instance
    const cropPieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: ['Wheat', 'Corn', 'Soybeans', 'Potatoes'],
            datasets: [{
                label: 'Acres',
                data: [300, 150, 100, 50],
                backgroundColor: [
                    '#2a9d8f',
                    '#e9c46a',
                    '#f4a261',
                    '#e76f51'
                ],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
});
