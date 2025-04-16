// Không cần import Toastify nếu dùng CDN

document.addEventListener('DOMContentLoaded', () => {
  const uploadArea = document.getElementById('upload-area');
  const fileInput = document.getElementById('file-input');
  const uploadText = document.getElementById('upload-text');
  const previewImg = document.getElementById('previewImg');
  const imagePreview = document.getElementById('imagePreview');
  const submitBtn = document.getElementById('submitBtn');

  // Kiểm tra null
  if (!uploadArea || !fileInput || !uploadText || !previewImg || !imagePreview || !submitBtn) {
    console.error('One or more elements not found');
    return;
  }

  uploadArea.addEventListener('click', () => {
    console.log('Upload area clicked');
    fileInput.click();
  });

  uploadArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    console.log('Dragover');
    uploadArea.classList.add('bg-gray-300');
  });

  uploadArea.addEventListener('dragleave', () => {
    console.log('Dragleave');
    uploadArea.classList.remove('bg-gray-300');
  });

  uploadArea.addEventListener('drop', (event) => {
    event.preventDefault();
    console.log('Drop');
    uploadArea.classList.remove('bg-gray-300');
    const files = event.dataTransfer.files;
    handleFileSelect(files);
  });

  fileInput.addEventListener('change', (event) => {
    console.log('File input changed');
    const files = event.target.files;
    handleFileSelect(files);
  });

  document.addEventListener('paste', (event) => {
    console.log('Paste event');
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
      console.log('Sample image clicked');
      const imgURL = img.src;
      localStorage.setItem('uploadedImage', imgURL);
      previewImg.src = imgURL;
      imagePreview.classList.remove('hidden');
      uploadText.classList.add('hidden');
      submitBtn.classList.remove('hidden');
      fileInput.value = '';
    });
  });

  submitBtn.addEventListener('click', () => {
    console.log('Submit clicked');
    if (localStorage.getItem('uploadedImage')) {
      window.location.href = '/remove-bg';
    } else {
      showToast('Please select an image first!', 'error');
    }
  });

  function handleFileSelect(files) {
    if (files.length > 0) {
      const file = files[0];
      if (!['image/png', 'image/jpeg'].includes(file.type)) {
        showToast('Please select a PNG or JPEG image!', 'error');
        return;
      }

      const reader = new FileReader();
      reader.onloadend = function () {
        console.log('File loaded');
        localStorage.setItem('uploadedImage', reader.result);
        previewImg.src = reader.result;
        imagePreview.classList.remove('hidden');
        uploadText.classList.add('hidden');
        submitBtn.classList.remove('hidden');
        showToast('Image uploaded successfully!', 'success');
      };
      reader.readAsDataURL(file);
    }
  }

  function showToast(message, type = 'success') {
    window.Toastify({
      text: message,
      duration: 3000,
      style: {
        background: type === 'success' ? 'green' : 'red',
      },
    }).showToast();
  }
});

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function scrollToFeatures() {
  const featuresSection = document.getElementById('features-section');
  if (featuresSection) {
    featuresSection.scrollIntoView({ behavior: 'smooth' });
  }
}