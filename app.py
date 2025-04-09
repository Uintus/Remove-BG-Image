from io import BytesIO
from flask import Flask, render_template, send_file, url_for
import datetime
from diffusers import DiffusionPipeline
from flask import Flask, request, jsonify
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# ________________________ROUTES___________________________
@app.route("/")
def index():
    return render_template('home.html')

@app.route("/remove-bg")
def remove_background():
    return render_template('remove-bg.html')


# ________________________API___________________________

# URL Google Colab
NGROK_URL = "https://pony-beloved-positively.ngrok-free.app"
  
# REMOVE BACKGROUND IMAGE  
@app.route("/remove-background", methods=["POST"])
def remove_background_image():
    if "image" not in request.files:
        return jsonify({
            "status": "error",
            "code": response.status_code,
            "data": "Please upload an image"}), 400

    # Nhận file ảnh từ request
    image_file = request.files["image"]

    # 🔹 Chuyển file thành định dạng gửi đi (multipart/form-data)
    files = {
    "image": (image_file.filename, image_file.stream, image_file.content_type),
    }

    # Gửi request đến Google Colab
    response = requests.post(f"{NGROK_URL}/remove-background", files=files)

    if response.status_code == 200:
        image_data = BytesIO(response.content)

        print("✅ Background Image successfully removed!")

        return send_file(image_data, mimetype="image/png")

    else:
        print("❌ Error generating image:", response.text)
        return jsonify({
            "status": "error",
            "code": response.status_code,
            "data": response.text
        })


# GENERATE IMAGE FROM TEXT 
@app.route("/generate", methods=["POST"])
def generate_image():
    if request.content_type != "application/json":
        return jsonify({"error": "Unsupported Media Type", "message": "Use 'application/json'"}), 415
    
    data = request.json
    background_text = data.get("background_text")
    
    prompt = f"Create a high-quality background image featuring the following requirement: {background_text}. Ensure a visually appealing composition that is not too cluttered, making it suitable as a background."
    
    # Gửi request đến Google Colab
    response = requests.post(f"{NGROK_URL}/generate", json={"prompt": prompt})

    if response.status_code == 200:
        image_data = BytesIO(response.content)

        file_path = "generated_bg.png"
        with open(file_path, "wb") as f:
            f.write(image_data.getvalue())

        print(f"✅ Image successfully downloaded and saved as {file_path}!")

        return send_file(image_data, mimetype="image/png")

    else:
        print("❌ Error generating image:", response.text)
        return jsonify({
            "status": "error",
            "code": response.status_code,
            "data": response.text
        }), response.status_code
        

# ADD IMAGE BACKGROUND
@app.route("/add-background", methods=["POST"])
def add_background_to_image():
    if "image" not in request.files or "background" not in request.files:
        return jsonify({"error": "Missing files", "message": "Upload both 'image' and 'background'"}), 400

    # Nhận file ảnh từ request
    image_file = request.files["image"]
    background_file = request.files["background"]

    # 🔹 Chuyển file thành định dạng gửi đi (multipart/form-data)
    files = {
    "image": (image_file.filename, image_file.stream, image_file.content_type),
    "background": (background_file.filename, background_file.stream, background_file.content_type),
    }

    # Gửi request đến Google Colab
    response = requests.post(f"{NGROK_URL}/add-background", files=files)

    if response.status_code == 200:
        image_data = BytesIO(response.content)

        print("✅ Image successfully downloaded!")

        return send_file(image_data, mimetype="image/png")

    else:
        print("❌ Error generating image:", response.text)
        return jsonify({
            "status": "error",
            "code": response.status_code,
            "data": response.text
        })



if __name__ == '__main__':
    app.run(debug=True)
