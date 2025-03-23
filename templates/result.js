const imageUrl = localStorage.getItem('processedImage');
if (imageUrl) {
    document.getElementById('resultImage').src = imageUrl; 
} else {
    console.error('Không tìm thấy ảnh đã xử lý.');
}

document.getElementById('generate-btn').addEventListener('click', function() {
    const aiBackgroundGenerator = document.getElementById('ai-background-generator');
    aiBackgroundGenerator.classList.remove('hidden');
    aiBackgroundGenerator.scrollIntoView({ behavior: 'smooth' });
});

document.getElementById('ai-generate').addEventListener('click', function() {
    const aiBackgroundGenerator = document.getElementById('ai-background-generator');
    aiBackgroundGenerator.classList.remove('hidden');
    aiBackgroundGenerator.scrollIntoView({ behavior: 'smooth' });
});