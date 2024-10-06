const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imgView = document.getElementById("img-view");

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
    const x_var = document.getElementById("x_var").value;
    const y_var = document.getElementById("y_var").value;

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

                // Set the image view to show the generated plot
                const imgView = document.getElementById("img-view");
                imgView.innerHTML = `<img src="${data.img_url}" alt="Generated Plot">`;
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please upload a valid CSV file.');
    }
}