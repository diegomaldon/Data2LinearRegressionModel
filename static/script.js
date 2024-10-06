const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const xVarInput = document.getElementById("x_var");  // Capture x_var input field
const yVarInput = document.getElementById("y_var");  // Capture y_var input field

dropArea.addEventListener("dragover", function(e) {
    e.preventDefault();
});

dropArea.addEventListener("drop", function(e) {
    e.preventDefault();
    inputFile.files = e.dataTransfer.files;
    uploadFile();
});

inputFile.addEventListener("change", uploadFile);

function uploadFile() {
    const file = inputFile.files[0];
    const x_var = xVarInput.value;  // Capture the value of x_var
    const y_var = yVarInput.value;  // Capture the value of y_var

    if (file && file.name.endsWith('.csv')) {
        let formData = new FormData();
        formData.append("file", file);
        formData.append("table_name", file.name.split('.')[0]);  // Set table name from file name
        formData.append("x_var", x_var);  // Add x_var to formData
        formData.append("y_var", y_var);  // Add y_var to formData

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.success);
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please upload a valid CSV file.');
    }
}