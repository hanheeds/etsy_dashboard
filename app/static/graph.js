// Include this script in your HTML after linking to Chart.js
document.addEventListener('DOMContentLoaded', function () {
  // Call the function on page load
  loadCSVFromServer();
});

// Function to load CSV data from Flask
async function loadCSVFromServer() {
  try {
    // Fetch data from the Flask endpoint
    const response = await fetch('/get_all_csv_data');
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const allData = await response.json();

    // Check for errors in the response
    if (allData.error) {
      console.error('Server Error:', allData.error);
      return;
    }

    // Extract listings.csv data
    const listingsData = allData.all_csv_files['listings.csv'];
    if (!listingsData) {
      console.error('No listings.csv data found in response');
      return;
    }

    // Visualize the data using the extracted listings data
    visualizeData(listingsData);
  } catch (error) {
    console.error('Error fetching data from the server:', error);
  }
}

// Function to extract and prepare data for visualization
function visualizeData(data) {
  const amounts = data.map(row => {
    if (row.price) {
      try {
        const priceString = row.price.replace(/'/g, '"'); // Replace single quotes with double quotes
        const priceObj = JSON.parse(priceString); // Parse the price JSON string
        return priceObj.amount / priceObj.divisor; // Calculate the actual price
      } catch (error) {
        console.error('Invalid JSON format in price column:', row.price);
        return 0; // Fallback value if parsing fails
      }
    }
    return 0; // Default to 0 if no price is available
  });

  const labels = data.map(row => {
    if (row.created_timestamp && !isNaN(row.created_timestamp)) {
      try {
        const timestamp = parseInt(row.created_timestamp, 10); // Ensure the timestamp is an integer
        const date = new Date(timestamp * 1000); // Convert seconds to milliseconds
        if (!isNaN(date.getTime())) {
          return date.toLocaleDateString(); // Format as a readable date
        }
      } catch (error) {
        console.error(`Error parsing timestamp: ${row.created_timestamp}`, error);
      }
    }
    return 'Invalid Date'; // Default to 'Invalid Date' for unparseable timestamps
  });

  createChart(labels, amounts);
}

// Global variable to store the chart instance
let chartInstance;

// Function to create or update the chart
function createChart(labels, data) {
  const ctx = document.getElementById('transactionChart').getContext('2d');

  // Check if a chart instance already exists and destroy it
  if (chartInstance) {
    chartInstance.destroy();
  }

  // Create a new chart instance
  chartInstance = new Chart(ctx, {
    type: 'line', // Chart type (e.g., 'line', 'bar', etc.)
    data: {
      labels: labels,
      datasets: [{
        label: 'Item Cost',
        data: data,
        borderColor: 'rgba(75, 192, 192, 1)', // Line color
        borderWidth: 2, // Line width
        fill: false // No area fill under the line
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false, // Allows resizing
      scales: {
        y: {
          beginAtZero: true, // Start y-axis at 0
          title: {
            display: true,
            text: 'Amount (USD)' // Label for the y-axis
          }
        },
        x: {
          title: {
            display: true,
            text: 'Created Date' // Label for the x-axis
          }
        }
      }
    }
  });
}
