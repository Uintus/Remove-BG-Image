from io import BytesIO
from flask import Flask, render_template, send_file
from model.demo import format_date, generate_greeting
import datetime
from diffusers import DiffusionPipeline
from model.model_loader.generator_bg_loader import pipe
from model.bg_generator import generate_bg

app = Flask(__name__)


@app.route("/")
def hello_world():
    today = datetime.datetime.now()
    return f"Hôm nay là {format_date(today)}. {generate_greeting('Tuyet')}"



@app.route("/person/<name>")
def hello(name=None):
    return render_template('hello.html', person=name)

# ___________________________TEST DEMO MODEL_______________________
# Demo run bg_generator 
@app.route("/bg-generator")
def bg_generator():
    elements = "a sunset sky with soft purple clouds and distant mountains"
    style = "realistic"
    preferred_colors = "warm tones like orange, purple, and soft blue"

    bg_result = generate_bg(elements, style, preferred_colors)
    
    # Chuyển ảnh thành dữ liệu nhị phân để gửi trực tiếp
    img_io = BytesIO()
    bg_result.save(img_io, format="PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")  # Trả về ảnh trực tiếp




if __name__ == '__main__':
    app.run(debug=True)
