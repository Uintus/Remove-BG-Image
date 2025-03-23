const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const uploadText = document.getElementById('upload-text');
const imagePreview = document.getElementById('image-preview');
const previewImg = document.getElementById('preview-img');
const removeBtn = document.getElementById('remove-btn');
const submitBtn = document.getElementById('submit-btn');

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
            const imgURL = URL.createObjectURL(file);
            previewImg.src = imgURL;
            imagePreview.classList.remove('hidden');
            uploadText.classList.add('hidden');
            submitBtn.classList.remove('hidden');
        } else {
            alert('Please select an image file!');
        }
    }
}

removeBtn.addEventListener('click', (event) => {
    event.stopPropagation(); 
    previewImg.src = '';
    imagePreview.classList.add('hidden');
    uploadText.classList.remove('hidden');
    submitBtn.classList.add('hidden');
    fileInput.value = '';  
});

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


submitBtn.addEventListener('click', (event) => {
    event.preventDefault(); 
    const apiUrl = 'https://api.example.com/remove-background'; 

    const formData = new FormData();
    const file = fileInput.files[0];
    if (file) {
        formData.append('image', file); 

        fetch(apiUrl, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            localStorage.setItem('processedImage', data.image);
            window.location.href = 'result.html';
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('Please upload an image first.');
    }
});