from rembg import remove
from PIL import Image, ImageChops
import os

def remove_background_optimized(input_path, output_path="output_removed_bg.png", threshold=30):
    """Xóa nền ảnh, giữ nét vùng chính và loại bỏ viền thừa."""
    if not os.path.exists(input_path):
        raise Exception("❌ Lỗi: Ảnh đầu vào không tồn tại!")

    print(f"📂 Đang mở ảnh: {input_path}")
    inp = Image.open(input_path).convert("RGBA")

    print("🎨 Đang xóa nền ảnh...")
    foreground = remove(inp)

    # 📌 Bước 1: Tạo mặt nạ Alpha để loại bỏ viền mờ
    print("✨ Đang xử lý viền ảnh...")
    alpha = foreground.split()[3]  # Lấy kênh Alpha (độ trong suốt)
    mask = alpha.point(lambda p: 255 if p > threshold else 0)  # Giữ lại pixel có alpha cao

    # 📌 Bước 2: Áp dụng mặt nạ để xóa viền mờ
    foreground.putalpha(mask)

    # 📌 Bước 3: Cắt mép ảnh tự động
    bbox = foreground.getbbox()
    if bbox:
        foreground = foreground.crop(bbox)

    # 📌 Lưu ảnh kết quả
    foreground.save(output_path, format="PNG")
    print(f"✅ Ảnh đã xóa nền tối ưu và lưu tại: {output_path}")

    # Hiển thị ảnh kết quả
    foreground.show()

if __name__ == "__main__":
    input_image = input("Nhập đường dẫn ảnh cần xóa nền (ví dụ: input.jpg): ").strip()
    output_image = input("Nhập tên file kết quả (mặc định: output_removed_bg.png): ").strip()

    if not output_image:
        output_image = "output_removed_bg.png"

    try:
        remove_background_optimized(input_image, output_image)
    except Exception as e:
        print(f"❌ LỖI: {e}")
