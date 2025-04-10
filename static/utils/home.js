const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const uploadText = document.getElementById('upload-text');


uploadArea.addEventListener('click', () => {
    fileInput.click();
});

uploadArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    uploadArea.classList.add('bg-gray-300');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('bg-gray-300');
});

uploadArea.addEventListener('drop', (event) => {
    event.preventDefault();
    uploadArea.classList.remove('bg-gray-300');
    const files = event.dataTransfer.files;
    handleFileSelect(files);
});

fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    handleFileSelect(files);
});

function handleFileSelect(files) {
    if (files.length > 0) {
        const file = files[0]; 
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onloadend = function() {
                localStorage.setItem('uploadedImage', reader.result);
                previewImg.src = reader.result; 
                imagePreview.classList.remove('hidden');
                uploadText.classList.add('hidden');
                submitBtn.classList.remove('hidden');
            };
            reader.readAsDataURL(file);
        } else {
            alert('Please select an image file!');
        }
    }
}


document.addEventListener('paste', (event) => {
    const items = event.clipboardData.items;
    for (let i = 0; i < items.length; i++) {
        if (items[i].kind === 'file') {
            const file = items[i].getAsFile();
            handleFileSelect([file]);
        }
    }
});

const images = document.querySelectorAll('.flex img'); 
images.forEach((img) => {
    img.addEventListener('click', () => {
        const imgURL = img.src; 
        previewImg.src = imgURL;  
        imagePreview.classList.remove('hidden');  
        uploadText.classList.add('hidden'); 
        submitBtn.classList.remove('hidden');  
        fileInput.value = '';  
    });
});

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' 
    });
}

function scrollToFeatures() {
    const featuresSection = document.getElementById('features-section');
    featuresSection.scrollIntoView({
        behavior: 'smooth' 
    });
}

