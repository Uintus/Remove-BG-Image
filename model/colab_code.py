# THIS PART DIDN'T BE USED HERE!!, COPY THIS TO COLAB AND RUN BEFORE FLASK SERVER
# THIS PART DIDN'T BE USED HERE!!, COPY THIS TO COLAB AND RUN BEFORE FLASK SERVER
# THIS PART DIDN'T BE USED HERE!!, COPY THIS TO COLAB AND RUN BEFORE FLASK SERVER


def text_to_image():
    # !pip install diffusers --upgrade
    # !pip install invisible_watermark transformers accelerate safetensors
    # !pip install torch flask flask-ngrok
    # !pip install pyngrok
    # !ngrok config add-authtoken 2ultHshNkR4erH0OuzEljBKJgdV_27xQzCQ5LtvMftrs1BWJV
   
    from diffusers import DiffusionPipeline
    import torch
    from pyngrok import ngrok
    import io
    from flask import Flask, request, send_file, jsonify
    from PIL import Image
    import numpy as np
    

    # Download model
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
    pipe.to("cuda")
    
    # Mở cổng Flask (5000)
    ngrok_tunnel = ngrok.connect(5000, domain="pony-beloved-positively.ngrok-free.app")
    print(f"Public URL: {ngrok_tunnel.public_url}")
    
    # Khởi tạo Flask
    app = Flask(__name__)


    @app.route("/generate", methods=["POST"])
    def generate_image():
        if request.content_type != "application/json":
            return jsonify({"error": "Unsupported Media Type", "message": "Use 'application/json'"}), 415

        data = request.json
        prompt = data.get("prompt") 

        print(f"🎨 Đang tạo ảnh với prompt: {prompt}")

        image = pipe(prompt).images[0]

        # Define a fixed filename
        file_path = "generated_image.png"
        image.save(file_path)

        img_io = io.BytesIO()
        image.save(img_io, format="PNG")
        img_io.seek(0)

        print("✅ Ảnh đã tạo xong, gửi về client!")

        return send_file(img_io, mimetype="image/png")
    
    @app.route("/add-background", methods=["POST"])
    def add_background_to_image():
        if "image" not in request.files or "background" not in request.files:
            return {"error": "Please upload both the main image and the background!"}, 400

        image = Image.open(request.files["image"])
        background = Image.open(request.files["background"])

        result = add_background(image, background)

        # Chuyển kết quả thành file ảnh để trả về
        img_io = io.BytesIO()
        result.save(img_io, format="PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")
    

    # ______________________FUNCTION___________________________
    def add_background(foreground, background):
        # Chuyển ảnh về RGBA nếu chưa có alpha channel
        foreground = foreground.convert("RGBA")
        background = background.convert("RGBA")

        # Resize background theo kích thước ảnh chính
        background = background.resize(foreground.size)

        # Chuyển ảnh thành array numpy
        fg_array = np.array(foreground)
        bg_array = np.array(background)

        # Tách các kênh màu và alpha
        fg_rgb, fg_alpha = fg_array[:, :, :3], fg_array[:, :, 3] / 255.0
        bg_rgb = bg_array[:, :, :3]

        # Tạo ảnh hợp nhất
        result_rgb = (fg_rgb * fg_alpha[:, :, None] + bg_rgb * (1 - fg_alpha[:, :, None])).astype(np.uint8)
        result = Image.fromarray(result_rgb)

        return result

    # Chạy Flask API
    app.run(port=5000)
   
    return