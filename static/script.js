const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");

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

    if (file && file.name.endsWith('.csv')) {
        let formData = new FormData();
        formData.append("file", file);
        formData.append("table_name", "my_table");  // You can dynamically set the table name

        fetch('http://127.0.0.1:5001/upload', {
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
