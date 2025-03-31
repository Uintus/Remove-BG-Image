from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image, ImageFilter
import io
import requests
from pyngrok import ngrok

app = Flask(__name__)

# 🖼 Hàm xóa nền
def remove_background_and_keep_size(image_bytes, threshold=50, blur_radius=2):
    inp = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    width, height = inp.size

    print("🎨 Đang xóa nền ảnh...")
    foreground = remove(inp)

    print("✨ Đang xử lý viền ảnh...")
    alpha = foreground.split()[3]
    mask = alpha.point(lambda p: 255 if p > threshold else 0)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    foreground.putalpha(mask)

    background = Image.new("RGB", (width, height), (255, 255, 255))
    background.paste(foreground, mask=foreground.split()[3])

    output_buffer = io.BytesIO()
    background.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    print("✅ Xóa nền xong!")

    return output_buffer

# 📌 API Xóa nền
@app.route("/remove-bg", methods=["POST"])
def remove_bg_api():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image_bytes = file.read()
    output_buffer = remove_background_and_keep_size(image_bytes)

    return send_file(output_buffer, mimetype="image/png")

# 🔥 Mở cổng public với ngrok
public_url = ngrok.connect(5000).public_url
print(f"🌍 Public Flask URL: {public_url}")

# 🚀 Chạy Flask API
if __name__ == "__main__":
    import threading

    def run_flask():
        app.run(port=5000)

    # Chạy Flask trong luồng riêng
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # 💻 Client gọi API ngay trong cùng file
    import time

    time.sleep(3)  # Đợi Flask khởi động

    def call_remove_bg_api(image_path):
        url = f"{public_url}/remove-bg"  # Gọi API qua ngrok
        files = {'file': open(image_path, 'rb')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            with open("output_image.png", "wb") as f:
                f.write(response.content)
            print("✅ Đã nhận ảnh đã xóa nền và lưu thành 'output_image.png'")
        else:
            print(f"❌ Có lỗi xảy ra: {response.json()}")

    # 📸 Test API với ảnh mẫu
    image_path = "your_image.png"  # Thay bằng đường dẫn ảnh thực tế
    call_remove_bg_api(image_path)