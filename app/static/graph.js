// Include this script in your HTML after linking to Chart.js and PapaParse libraries
// Add event listener to the button for updating data
document.addEventListener('DOMContentLoaded', function () {
  // Get the button element by its ID
  const button = document.getElementById('changeTextBtn');

  // Add a click event listener to the button
  button.addEventListener('click', function () {
    // Call the loadCSV function when the button is clicked
    loadCSV();
  });
});


// Function to load CSV data
function loadCSV() {
  Papa.parse('../data/transactions.csv', {
    download: true,
    header: true,
    complete: function(results) {
      visualizeData(results.data);
    }
  });
}

// Function to extract and prepare data
function visualizeData(data) {
  const amounts = data.map(row => {
    if (row.price) {
      try {
        // Replace single quotes with double quotes and parse the string
        const priceString = row.price.replace(/'/g, '"');
        const priceObj = JSON.parse(priceString);
        return priceObj.amount / priceObj.divisor;
      } catch (error) {
        console.error('Invalid JSON format in price column:', row.price);
        return 0; // Fallback value if parsing fails
      }
    }
    return 0;
  });

  // Convert the Unix timestamps to readable date strings for labels
  const labels = data.map(row => {
    if (row.paid_timestamp) {
      const date = new Date(parseInt(row.paid_timestamp) * 1000); // Convert to milliseconds
      return date.toLocaleString(); // Format as a readable date and time
    }
    return 'Invalid Date';
  });

  createChart(labels, amounts);
}



// Global variable to store the chart instance
let chartInstance;

function createChart(labels, data) {
  const ctx = document.getElementById('transactionChart').getContext('2d');

  // Check if a chart instance already exists and destroy it
  if (chartInstance) {
    chartInstance.destroy();
  }

  // Create a new chart and store it in the global variable
  chartInstance = new Chart(ctx, {
    type: 'line', // or 'bar', 'pie', etc.
    data: {
      labels: labels,
      datasets: [{
        label: 'Item Cost',
        data: data,
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        fill: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false, // Allows resizing
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Amount (USD)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Date'
          }
        }
      }
    }
  });
}
