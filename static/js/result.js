const resultImage = document.getElementById('resultImage');
const downloadBtn = document.getElementById('downloadBtn');

function getImageUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('image');
}

function displayImage() {
    const imageUrl = getImageUrl();
    if (!imageUrl) {
        window.location.href = 'upload.html';
        return;
    }
    resultImage.src = imageUrl;
}

function downloadImage() {
    const imageUrl = getImageUrl();
    if (imageUrl) {
        const link = document.createElement('a');
        link.href = imageUrl;
        link.download = 'processed_image.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Event Listeners
downloadBtn.addEventListener('click', downloadImage);
window.addEventListener('load', displayImage);