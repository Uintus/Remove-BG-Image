from flask import Flask, request, send_file, jsonify
from rembg import remove, new_session
from PIL import Image
import io
from pyngrok import ngrok

app = Flask(__name__)


def remove_background(image_bytes):
    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    session = new_session("u2net")

    result = remove(
        input_image,
        session=session,
        alpha_matting=False,  
        post_process_mask=True
    )

    result = result.resize((input_image.width * 2, input_image.height * 2), Image.LANCZOS)
    result = result.resize((input_image.width, input_image.height), Image.LANCZOS)

    return result
# API: Xóa nền
@app.route("/remove-background", methods=["POST"])
def remove_bg_api():
    if "image" not in request.files:
        return jsonify({"error": "Please upload an image!"}), 400

    image_bytes = request.files["image"].read()
    result_image = remove_background(image_bytes)

    img_io = io.BytesIO()
    result_image.save(img_io, format="PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")
# 🔥 Mở cổng ngrok
public_url = ngrok.connect(5000).public_url
print(f"🌍 Public Flask URL: {public_url}/remove-background")

# 🚀 Run Flask server
if __name__ == "__main__":
    import threading

    def run_flask():
        app.run(port=5000)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
