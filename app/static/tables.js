// Fetch performance data
// Fetch performance data
fetch('/get_performance_data')
    .then(response => response.json())
    .then(data => {
        const performanceTables = data.performance_tables;
        console.log(performanceTables);

        // Wait for the DOM to be fully loaded
        document.addEventListener('DOMContentLoaded', function () {
            const container = document.getElementById('performance-tables');
            
            if (container) {
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

                // Initialize DataTables
                $(document).ready(function () {
                    $('table.display').DataTable();
                });
            } else {
                console.error('Element with id "performance-tables" not found.');
            }
        });
    })
    .catch(error => console.error('Error fetching data:', error));
