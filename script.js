const dropArea = document.getElementById("drop-area")
const inputFile = document.getElementById("input-file")
const imageView = document.getElementById('"img-view') 

inputFile.addEventListener("change",uploadFile)


function uploadFile() {
    inputFile.files[0];
    let imgLink = URL.createObjectURL(inputFile.files[0]);
    imageView.style.backgroundImage = `url(${imgLink})`;
    imageView.textContent = "";
    imageView.style.border = 0;
}

function getFile() {
    return inputFile.files[0];
}

module.exports = {getFile};

dropArea.addEventListener("dragover", function(e) {
    e.preventDefault();
});

dropArea.addEventListener("drop", function(e) {
    e.preventDefault(); 
    inputFile.files = e.dataTransfer.files;
    uploadFile()
});
