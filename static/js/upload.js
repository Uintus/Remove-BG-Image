const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const processBtn = document.getElementById('processBtn');
const loading = document.getElementById('loading');
let fileName = '';

function toggleLoading(show) {
    loading.classList.toggle('hidden', !show);
    processBtn.disabled = show;
}

function showToast(message, isError = true) {
    Toastify({
        text: message,
        duration: 3000, // Hiển thị trong 3 giây
        close: true,    // Có nút đóng
        gravity: "top",
        position: "right",
        style: {
            background: isError ? "#ff4444" : "#00C851", // Đỏ cho lỗi, xanh cho thành công
            fontSize: "16px",
            borderRadius: "8px",
        }
    }).showToast();
}

function previewImage(event) {
    const file = event.target.files[0];
    if (file) {
        fileName = file.name;
        preview.src = URL.createObjectURL(file);
        preview.classList.remove('hidden');
        processBtn.disabled = false;
    }
}

async function processImage() {
    const file = imageInput.files[0];
    if (!file) {
        showToast("Please select an image", true);
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
        toggleLoading(true);

        const removeBgResponse = await axios.post('/api/remove-background', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });

        if (removeBgResponse.data.status === 'error') {
            throw new Error(removeBgResponse.data.data);
        }

        const addBgResponse = await axios.get(`/api/add-background/${fileName}`);
        if (addBgResponse.data.status === 'error') {
            throw new Error(addBgResponse.data.data);
        }

        // Thông báo thành công trước khi chuyển hướng
        showToast("Image processed successfully!", false);
        setTimeout(() => {
            window.location.href = `result.html?image=${encodeURIComponent(addBgResponse.data.data)}`;
        }, 1000); // Chờ 1 giây để người dùng thấy thông báo

    } catch (error) {
        // Hiển thị lỗi chi tiết hơn nếu có response từ server
        const message = error.response ? error.response.data.data : error.message;
        showToast(message, true);
    } finally {
        toggleLoading(false);
    }
}

// Event Listeners
imageInput.addEventListener('change', previewImage);
processBtn.addEventListener('click', processImage);