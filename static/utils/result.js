const result = document.getElementById('result');
const downloadBtn = document.getElementById('download-btn');
const fileInput = document.getElementById('file-input');
const uploadArea = document.getElementById('upload-area');
const colorInput = document.getElementById('colorInput');

let selectedColumn = null;
let uploadedImage = null;  
let selectedBackground = null;  

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
        imageUrl = uploadedImage ? uploadedImage : 'https://i.pinimg.com/originals/df/db/c7/dfdbc73a7622c6eb606035f2f04f9e45.gif'; 
    } else if (type === 'removed') {
        imageUrl = selectedBackground ? selectedBackground : 'https://www.avaide.com/images/online-bg-remover/remove-bg.png'; 
    }
    displayImage(imageUrl);

    const originalIndicator = document.getElementById('originalIndicator');
    const removedIndicator = document.getElementById('removedIndicator');

    if (type === 'original') {
        removedIndicator.style.transition = ''; 
        removedIndicator.style.transform = `translateX(${element.offsetLeft}px)`;
        setTimeout(() => {
            originalIndicator.classList.remove('hidden');
            removedIndicator.classList.add('hidden');
            originalIndicator.style.transition = 'transform 0.5s'; 
            originalIndicator.style.transform = `translateX(0)`;
        }, 10);
    } else {
        originalIndicator.style.transition = ''; 
        originalIndicator.style.transform = `translateX(${element.offsetLeft}px)`;
        setTimeout(() => {
            removedIndicator.classList.remove('hidden');
            originalIndicator.classList.add('hidden');
            removedIndicator.style.transition = 'transform 0.5s'; 
            removedIndicator.style.transform = `translateX(0)`;
        }, 10);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const originalImage = localStorage.getItem('uploadedImage');
    if (originalImage) {
        uploadedImage = originalImage; 
        result.src = originalImage;  
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
            uploadedImage = e.target.result; 
            displayImage(uploadedImage);  
            localStorage.setItem('uploadedImage', uploadedImage); 
        };
        reader.readAsDataURL(file);
    }
});

// Event listener for default background images
const defaultImages = document.querySelectorAll('.grid img');
defaultImages.forEach(img => {
    img.addEventListener('click', () => {
        selectedBackground = img.src; 
        displayImage(selectedBackground);  
    });
});

// Event listener for color input
colorInput.addEventListener('input', (event) => {
    const color = event.target.value;
    selectedBackground = color; 
    result.style.backgroundColor = selectedBackground; 
});

// Event listener for color divs
const colorDivs = document.querySelectorAll('.flex-wrap > div');  
colorDivs.forEach(div => {
    div.addEventListener('click', () => {
        const color = getComputedStyle(div).backgroundColor;  
        selectedBackground = color; 
        result.style.backgroundColor = selectedBackground;
    });
});

// Download confirmation popup
const downloadPopup = document.getElementById('downloadPopup');
const confirmDownloadBtn = document.getElementById('confirmDownloadBtn');
const cancelDownloadBtn = document.getElementById('cancelDownloadBtn');
const toast = document.getElementById('toast');

downloadBtn.addEventListener('click', () => {
    downloadPopup.classList.remove('hidden');
});

confirmDownloadBtn.addEventListener('click', () => {
    const link = document.createElement('a');
    link.href = result.src; 
    link.download = 'downloaded_image.png'; 
    document.body.appendChild(link);
    link.click(); 
    document.body.removeChild(link); 

    showToast("Image downloaded successfully!");
    downloadPopup.classList.add('hidden'); 
});

cancelDownloadBtn.addEventListener('click', () => {
    downloadPopup.classList.add('hidden'); 
});

//toast
function showToast(message) {
    toast.classList.remove('hidden');
    toast.textContent = message;
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 5000);
}

// Generate button logic
const generateButton = document.querySelector('button.mt-4.bg-blue-500'); 
const modal = document.getElementById('modal');
const loading = document.getElementById('loading');
const generatedImage = document.getElementById('generatedImage');
const applyBtn = document.getElementById('applyBtn');
const closeModalBtn = document.getElementById('closeModalBtn');

generateButton.addEventListener('click', () => {
    modal.classList.remove('hidden');
    loading.classList.remove('hidden');
    generatedImage.classList.add('hidden');
    applyBtn.classList.add('hidden');

    setTimeout(() => {
        const imageUrl = 'https://i.pinimg.com/originals/df/db/c7/dfdbc73a7622c6eb606035f2f04f9e45.gif'; 
        loading.classList.add('hidden');
        generatedImage.src = imageUrl;
        generatedImage.classList.remove('hidden');
        applyBtn.classList.remove('hidden');
    }, 3000);
});

applyBtn.addEventListener('click', () => {
    const imageUrl = generatedImage.src; 
    displayImage(imageUrl);  
    modal.classList.add('hidden');  
});
 
closeModalBtn.addEventListener('click', () => {
    modal.classList.add('hidden');  
});