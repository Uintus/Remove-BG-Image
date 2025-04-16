// static/utils/remove-bg.js
document.addEventListener('DOMContentLoaded', () => {
  const originalColumn = document.getElementById('originalColumn');
  const removedBackgroundColumn = document.getElementById('removedBackgroundColumn');
  const originalIndicator = document.getElementById('originalIndicator');
  const removedIndicator = document.getElementById('removedIndicator');
  const resultImg = document.getElementById('result');
  const loading = document.getElementById('loading');
  const uploadArea = document.getElementById('upload-area');
  const fileInput = document.getElementById('file-input');
  const uploadText = document.getElementById('upload-text');
  const downloadBtn = document.getElementById('download-btn');

  // Check null elements
  if (!originalColumn || !removedBackgroundColumn || !originalIndicator || !removedIndicator || !resultImg || !loading || !uploadArea || !fileInput || !uploadText || !downloadBtn) {
    console.error('One or more elements not found');
    window.utils.showToast('Page error. Redirecting to home...', 'error');
    setTimeout(() => { window.location.href = '/'; }, 3000);
    return;
  }

  // Check for uploaded image
  let uploadedImage = localStorage.getItem('uploadedImage');
  let processedImage = null;
  if (!uploadedImage) {
    window.utils.showToast('No image selected. Redirecting to home...', 'error');
    setTimeout(() => { window.location.href = '/'; }, 3000);
    return;
  }

  // Initialize image
  resultImg.src = uploadedImage;
  resultImg.classList.remove('hidden');

  // Tab switching
  window.showImage = function (type, element) {
    originalIndicator.classList.add('hidden');
    removedIndicator.classList.add('hidden');
    if (type === 'original') {
      originalIndicator.classList.remove('hidden');
      resultImg.src = uploadedImage;
    } else {
      removedIndicator.classList.remove('hidden');
      resultImg.src = processedImage || uploadedImage;
    }
    originalColumn.classList.remove('text-blue-700');
    removedBackgroundColumn.classList.remove('text-blue-700');
    element.classList.add('text-blue-700');
  };

  // Default to Result tab
  showImage('removed', removedBackgroundColumn);

  // Process image
  if (uploadedImage) {
    window.utils.showLoading(true);
    resultImg.classList.add('hidden');
    removeBackground(uploadedImage);
  }

  // Upload new image
  uploadArea.addEventListener('click', () => {
    fileInput.click();
  });

  fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    handleFileSelect(files);
  });

  uploadArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    uploadArea.classList.add('bg-gray-200');
  });

  uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('bg-gray-200');
  });

  uploadArea.addEventListener('drop', (event) => {
    event.preventDefault();
    uploadArea.classList.remove('bg-gray-200');
    const files = event.dataTransfer.files;
    handleFileSelect(files);
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

  // Download button
  downloadBtn.addEventListener('click', () => {
    if (processedImage) {
      const link = document.createElement('a');
      link.href = processedImage;
      link.download = 'background-removed.png';
      link.click();
    } else {
      window.utils.showToast('No processed image available!', 'error');
    }
  });

  function handleFileSelect(files) {
    if (files.length > 0) {
      const file = files[0];
      if (!['image/png', 'image/jpeg'].includes(file.type)) {
        window.utils.showToast('Please select a PNG or JPEG image!', 'error');
        return;
      }

      const reader = new FileReader();
      reader.onloadend = function () {
        uploadedImage = reader.result;
        localStorage.setItem('uploadedImage', uploadedImage);
        resultImg.src = uploadedImage;
        resultImg.classList.remove('hidden');
        window.utils.showLoading(true);
        showImage('removed', removedBackgroundColumn);
        removeBackground(uploadedImage);
      };
      reader.onerror = function () {
        window.utils.showToast('Failed to read image!', 'error');
      };
      reader.readAsDataURL(file);
    }
  }

  function removeBackground(imageData) {
    const byteString = atob(imageData.split(',')[1]);
    const mimeString = imageData.split(',')[0].split(':')[1].split(';')[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }
    const blob = new Blob([ab], { type: mimeString });

    const formData = new FormData();
    formData.append('image', blob, 'uploaded_image.png');

    fetch('/remove-background', {
      method: 'POST',
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('API error');
        }
        return response.json();
      })
      .then((data) => {
        window.utils.showLoading(false);
        resultImg.classList.remove('hidden');
        if (data.status === 'success') {
          processedImage = data.data;
          if (removedIndicator.classList.contains('hidden')) {
            showImage('original', originalColumn);
          } else {
            resultImg.src = processedImage;
          }
          resultImg.onload = () => {
            window.utils.showToast('Background removed successfully!', 'success');
          };
          resultImg.onerror = () => {
            window.utils.showToast('Failed to load processed image!', 'error');
          };
        } else {
          window.utils.showToast(data.data || 'Failed to remove background', 'error');
        }
      })
      .catch((error) => {
        console.error('Error removing background:', error);
        window.utils.showLoading(false);
        resultImg.classList.remove('hidden');
        window.utils.showToast('Error processing image. Please try again.', 'error');
      });
  }
});