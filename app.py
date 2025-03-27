from io import BytesIO
from flask import Flask, render_template, send_file
from model.demo import format_date, generate_greeting
import datetime
from diffusers import DiffusionPipeline
from flask import Flask, request, jsonify
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# URL Google Colab
NGROK_URL = "https://pony-beloved-positively.ngrok-free.app/generate"

@app.route("/")
def hello_world():
    today = datetime.datetime.now()
    return f"Hôm nay là {format_date(today)}. {generate_greeting('Tuyet')}"

# GENERATE IMAGE FROM TEXT 
@app.route("/generate", methods=["POST"])
def generate_image():
    if request.content_type != "application/json":
        return jsonify({"error": "Unsupported Media Type", "message": "Use 'application/json'"}), 415
    
    data = request.json
    elements = data.get("elements", "")
    style = data.get("style", "realistic")
    preferred_colors = data.get("preferred_colors", "")
    
    prompt = f"Create a high-quality background image featuring the following elements: {elements}. The image should have a {style} style, with a color palette of {preferred_colors}. Ensure a visually appealing composition that is not too cluttered, making it suitable as a background."
    
    # Gửi request đến Google Colab
    response = requests.post(NGROK_URL, json={"prompt": prompt})

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
        }), response.status_code


if __name__ == '__main__':
    app.run(port=8080, debug=True)
