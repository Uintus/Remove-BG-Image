from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image, ImageFilter
import io

app = Flask(__name__)

def remove_background_and_keep_size(image_bytes, threshold=50, blur_radius=2):
    inp = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    width, height = inp.size

    print("🎨 Đang xóa nền ảnh...")
    foreground = remove(inp)

    # Xử lý mặt nạ Alpha để loại bỏ viền đen
    print("✨ Đang xử lý viền ảnh...")
    alpha = foreground.split()[3]
    mask = alpha.point(lambda p: 255 if p > threshold else 0)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    foreground.putalpha(mask)

    # Tạo nền trắng có cùng kích thước
    background = Image.new("RGB", (width, height), (255, 255, 255))
    background.paste(foreground, mask=foreground.split()[3])

    # Chuyển ảnh thành bytes
    output_buffer = io.BytesIO()
    background.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    print("✅ Xóa nền xong!")

    return output_buffer

@app.route("/remove-bg", methods=["POST"])
def remove_bg_api():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image_bytes = file.read()
    output_buffer = remove_background_and_keep_size(image_bytes)

    return send_file(output_buffer, mimetype="image/png")

# if __name__ == "__main__":
#     app.run(port=5001, debug=True)
if __name__ == "__main__":
    # Test với ảnh cố định
    test_image_path = "bi.jpg"  # Thay bằng đường dẫn ảnh test của bạn
    with open(test_image_path, "rb") as f:
        image_bytes = f.read()
    
    output_image = remove_background_and_keep_size(image_bytes)
    
    with open("output_image.png", "wb") as f:
        f.write(output_image.getvalue())
    
    print("✅ Ảnh đã được xử lý và lưu thành 'output_image.png'")

