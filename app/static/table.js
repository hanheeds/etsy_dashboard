async function fetchCSV() {
    const response = await fetch('../data/listings.csv');
    const data = await response.text();
    return data;
  }
  
  function csvToTable(csv) {
    const rows = csv.split('\n');
    let table = '<table border="1">';
    
    rows.forEach((row, rowIndex) => {
      const cells = row.split(',');
      table += '<tr>';
      
      cells.forEach(cell => {
        if (rowIndex === 0) {
          table += `<th>${cell}</th>`; // Header cells
        } else {
          table += `<td>${cell}</td>`; // Data cells
        }
      });
      
      table += '</tr>';
    });
    
    table += '</table>';
    return table;
  }
  
  async function displayCSV() {
    const csvData = await fetchCSV();
    const tableHTML = csvToTable(csvData);
    document.getElementById('tableContainer').innerHTML = tableHTML;
  }
  
  // Call displayCSV to load and display the table when the page loads
  displayCSV();
  