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

    # Chạy Flask API
    app.run(port=5000)
   
    return