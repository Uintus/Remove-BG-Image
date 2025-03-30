const result = document.getElementById('result');
const downloadBtn = document.getElementById('download-btn');
const fileInput = document.getElementById('file-input');
const uploadArea = document.getElementById('upload-area');
const colorInput = document.getElementById('colorInput');

let selectedColumn = null;

function showImage(type, element) {
    if (selectedColumn) {
        selectedColumn.classList.remove('text-blue-500');
        selectedColumn.classList.add('text-gray-500');
    }
    selectedColumn = element;
    selectedColumn.classList.add('text-blue-500');
    selectedColumn.classList.remove('text-gray-500');

    let imageUrl;
    if (type === 'original') {
        const originalImage = localStorage.getItem('uploadedImage');
        imageUrl = originalImage ? originalImage : 'https://i.pinimg.com/originals/df/db/c7/dfdbc73a7622c6eb606035f2f04f9e45.gif'; 
    } else if (type === 'removed') {
        const urlParams = new URLSearchParams(window.location.search);
        imageUrl = urlParams.get('processedImage') ? urlParams.get('processedImage') : 'https://www.avaide.com/images/online-bg-remover/remove-bg.png'; 
    }
    displayImage(imageUrl);
}
document.addEventListener('DOMContentLoaded', () => {
    const originalImage = localStorage.getItem('uploadedImage');
    if (originalImage) {
        const resultImg = document.getElementById('result');
        resultImg.src = originalImage; // Cập nhật src của hình ảnh
    } else {
        console.error("No image found in localStorage.");
    }
});

// Function to display the image
function displayImage(src) {
    result.src = src;
    result.classList.remove('hidden');
    downloadBtn.classList.remove('hidden');
}

// Event listener for file input (drag & drop)
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            displayImage(e.target.result);
            localStorage.setItem('uploadedImage', e.target.result); // Lưu vào localStorage
        };
        reader.readAsDataURL(file);
    }
});

// Event listener for default background images
const defaultImages = document.querySelectorAll('.grid img');
defaultImages.forEach(img => {
    img.addEventListener('click', () => {
        displayImage(img.src);
    });
});

// Event listener for color input
colorInput.addEventListener('input', (event) => {
    const color = event.target.value;
    result.style.backgroundColor = color; // Change background color of the image container
});

// Event listener for color divs
const colorDivs = document.querySelectorAll('.flex-wrap > div'); // Select all color divs
colorDivs.forEach(div => {
    div.addEventListener('click', () => {
        const color = getComputedStyle(div).backgroundColor; // Get the computed background color
        result.style.backgroundColor = color; 
    });
});

// Tải xuống hình ảnh
downloadBtn.addEventListener('click', () => {
    const confirmDownload = confirm("Do you want to download this image?");
    if (confirmDownload) {
        const link = document.createElement('a');
        link.href = result.src; 
        link.download = 'downloaded_image.png'; 
        document.body.appendChild(link);
        link.click(); 
        document.body.removeChild(link); 
    }
});

document.addEventListener('DOMContentLoaded', () => {
});