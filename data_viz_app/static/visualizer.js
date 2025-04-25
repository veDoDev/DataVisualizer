// Assuming these variables are initialized elsewhere, likely in the HTML or another script
// For example, in the HTML: <script> var hot = ...; var processDataUrl = "..."; var generateGraph = ...; var bootstrap = ...; </script>
// Or, if they are defined in another included JavaScript file, ensure that file is loaded before this one.

// Add a new trace
function addTrace() {
    const graphType = document.getElementById('graphType').value;
    const xColumn = document.getElementById('xColumn').value;
    const yColumn = document.getElementById('yColumn').value;
    
    if (!graphType || !xColumn || !yColumn) {
        alert('Please select all required fields.');
        return;
    }
    
    // Get data from the table
    const data = hot.getData();
    const headers = hot.getColHeader();
    
    // Check if the selected columns exist in the headers
    if (!headers.includes(xColumn) || !headers.includes(yColumn)) {
        alert(`Error: One or both of the selected columns (${xColumn}, ${yColumn}) do not exist in the data.`);
        return;
    }
    
    // Convert to array of objects
    const jsonData = [];
    for (let i = 0; i < data.length; i++) {
        const row = {};
        for (let j = 0; j < headers.length; j++) {
            if (headers[j] && headers[j].trim() !== '') {
                row[headers[j]] = data[i][j];
            }
        }
        // Only add rows with data
        if (Object.values(row).some(val => val !== null && val !== '')) {
            jsonData.push(row);
        }
    }
    
    // Show loading spinner
    document.getElementById('loadingSpinner').style.display = 'flex';
    
    // Process data and generate graph
    fetch(processDataUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ data: jsonData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Generate graph
            generateGraph(graphType, xColumn, yColumn);
            
            // Close modal
            const traceModal = document.getElementById('traceModal');
            const modalInstance = bootstrap.Modal.getInstance(traceModal);
            if (modalInstance) {
                modalInstance.hide();
            }
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing data.');
    })
    .finally(() => {
        // Hide loading spinner
        document.getElementById('loadingSpinner').style.display = 'none';
    });
}