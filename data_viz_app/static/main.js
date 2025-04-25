// URL variables (to be set in the template)
let uploadFileUrl;
let processDataUrl;
let getColumnsUrl;
let generateGraphUrl;
let saveDataUrl;

// Global variables
let hot; // Handsontable instance
let bootstrap;

// Declare functions that are used but not defined in this file.
let initializeHandsontable;
let uploadFile;
let updateColumnSelects;
let addTrace;
let addColumn;
let addRow;
let saveData;

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    bootstrap = window.bootstrap;
    
    // Initialize Handsontable
    initializeHandsontable();
    
    // Set up event listeners
    setupEventListeners();
});

// Set up event listeners
function setupEventListeners() {
    // Import button
    document.getElementById('importBtn').addEventListener('click', function() {
        const importModal = new bootstrap.Modal(document.getElementById('importModal'));
        importModal.show();
    });
    
    // Upload form submission
    document.getElementById('uploadForm').addEventListener('submit', function(e) {
        e.preventDefault();
        uploadFile();
    });
    
    // Add trace button
    document.getElementById('addTraceBtn').addEventListener('click', function() {
        updateColumnSelects();
        const traceModal = new bootstrap.Modal(document.getElementById('traceModal'));
        traceModal.show();
    });
    
    // Trace form submission
    document.getElementById('traceForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addTrace();
    });
    
    // Add column button
    document.getElementById('addColumnBtn').addEventListener('click', addColumn);
    
    // Add row button
    document.getElementById('addRowBtn').addEventListener('click', addRow);
    
    // Save data button
    document.getElementById('saveDataBtn').addEventListener('click', saveData);
}