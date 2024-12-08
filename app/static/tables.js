// Fetch performance data
fetch('/get_performance_data')
    .then(response => response.json())
    .then(data => {
        console.log('hi1');
        const performanceTables = data.performance_tables;
        console.log(performanceTables);

        // Check if the DOM is already loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function () {
                renderPerformanceTables(performanceTables);
            });
        } else {
            renderPerformanceTables(performanceTables);
        }
    })
    .catch(error => console.error('Error fetching data:', error));

// Function to render performance tables
function renderPerformanceTables(performanceTables) {
    const container = document.getElementById('performance-tables');
    console.log('hi2');
    if (container) {
        console.log('hi');
        // Loop through the performance tables and append them to the container
        for (const [key, rows] of Object.entries(performanceTables)) {
            let tableHtml = `<h2>${key.replace('_', ' ').toUpperCase()}</h2>`;
            tableHtml += '<table id="' + key + '" class="display"><thead><tr><th>Title</th><th>Num Favorers</th></tr></thead><tbody>';
            rows.forEach(row => {
                tableHtml += `<tr><td>${row.title}</td><td>${row.num_favorers}</td></tr>`;
            });
            tableHtml += '</tbody></table>';
            container.innerHTML += tableHtml;
        }

        // Initialize DataTables for all new tables
        $('table.display').each(function () {
            $(this).DataTable();
        });
    } else {
        console.error('Element with id "performance-tables" not found.');
    }
}
