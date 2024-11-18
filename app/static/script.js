document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:5000/get-listings')
      .then(response => response.json())
      .then(data => {
        createTable(data);
      })
      .catch(error => console.error('Error fetching data:', error));
  
    document.getElementById('submitBtn').addEventListener('click', function() {
      const editedData = [];
      d3.selectAll('tbody tr').each(function() {
        const row = d3.select(this);
        const listingId = row.select('.listing-id').text();
        const tags = row.select('.tags input').property('value');
        editedData.push({ listing_id: listingId, tags: tags });
      });
  
      fetch('http://127.0.0.1:5000/submit-tags', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(editedData)
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          alert('Tags submitted successfully!');
        }
      })
      .catch(error => console.error('Error submitting tags:', error));
    });
  });
  
  function createTable(data) {
    const tbody = d3.select('#listingsTable tbody');
    tbody.selectAll('tr')
      .data(data)
      .enter()
      .append('tr')
      .html(d => `
        <td>${d.title}</td>
        <td class="listing-id">${d.listing_id}</td>
        <td class="tags"><input type="text" value="${d.tags}"></td>
      `);
  }
  