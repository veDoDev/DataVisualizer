// Declare variables (assuming they are defined elsewhere or will be)
let uploadFileUrl;
let bootstrap;
let populateColumnSelects;
let getColumnsUrl; // Declare getColumnsUrl
let hot; // Declare hot

// Upload file function
function uploadFile() {
    const form = document.getElementById('uploadForm');
    const formData = new FormData(form);
    
    // Show loading spinner
    document.getElementById('loadingSpinner').style.display = 'flex';
    
    fetch(uploadFileUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Close modal
            const importModal = document.getElementById('importModal');
            const modalInstance = bootstrap.Modal.getInstance(importModal);
            if (modalInstance) {
                modalInstance.hide();
            }
            
            // Update column selects
            populateColumnSelects(data.columns);
            
            // Display the file name
            const fileNameDisplay = document.getElementById('importedFileName');
            if (fileNameDisplay) {
                fileNameDisplay.textContent = data.file_name;
                fileNameDisplay.parentElement.style.display = 'block';
            }
            
            // Show success message
            alert('File uploaded and processed successfully!');
            
            // Fetch the processed data
            fetchProcessedData();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during file upload.');
    })
    .finally(() => {
        // Hide loading spinner
        document.getElementById('loadingSpinner').style.display = 'none';
    });
}

// Fetch processed data
function fetchProcessedData() {
    fetch(getColumnsUrl)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update column selects
                populateColumnSelects(data.columns);
                
                // Load data into the spreadsheet
                if (data.data && data.data.length > 0) {
                    loadDataIntoSpreadsheet(data.data, data.columns);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Load data into the spreadsheet
function loadDataIntoSpreadsheet(data, columns) {
    // Convert data from array of objects to array of arrays
    const arrayData = [];
    
    // Add header row
    arrayData.push(columns);
    
    // Add data rows
    data.forEach(row => {
        const rowArray = [];
        columns.forEach(col => {
            rowArray.push(row[col] !== undefined ? row[col] : '');
        });
        arrayData.push(rowArray);
    });
    
    // Update Handsontable
    hot.updateSettings({
        data: arrayData.slice(1),  // Remove header row
        colHeaders: columns,       // Use columns as headers
        minSpareRows: 1,
        minSpareCols: 1
    });
}