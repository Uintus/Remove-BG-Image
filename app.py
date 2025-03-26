from flask import Flask, render_template, request, jsonify, send_file
from model.demo import format_date, generate_greeting
import datetime
import os
import uuid
from io import BytesIO

app = Flask(__name__)

# Thư mục lưu trữ ảnh tạm thời
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Endpoint để tải ảnh lên
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({
            "status": "error",
            "code": "400",
            "message": "No file part"
        }), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "status": "error",
            "code": "400",
            "message": "No selected file"
        }), 400
    
    try:
        # Lưu ảnh tải lên
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # Trả về ảnh trực tiếp
        return send_file(file_path, mimetype='image/jpeg')
    except Exception as e:
        # Trả về kết quả lỗi nếu có lỗi xảy ra
        return jsonify({
            "status": "error",
            "code": "500",
            "message": str(e)
        }), 500

# Endpoint để lấy ảnh đã xóa nền (giả lập)
@app.route('/result', methods=['GET'])
def get_result():
    file_path = request.args.get('file_path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({
            "status": "error",
            "code": "404",
            "message": "File not found"
        }), 404
    
    try:
        # Giả lập xóa nền: Trả về chính ảnh gốc
        return send_file(file_path, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({
            "status": "error",
            "code": "500",
            "message": str(e)
        }), 500

# Endpoint để lấy ảnh đã kết hợp với nền mới (giả lập)
@app.route('/combine', methods=['GET'])
def combine_background():
    file_path = request.args.get('file_path')
    background_path = request.args.get('background_path')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({
            "status": "error",
            "code": "404",
            "message": "File not found"
        }), 404
    
    if not background_path or not os.path.exists(background_path):
        return jsonify({
            "status": "error",
            "code": "404",
            "message": "Background file not found"
        }), 404
    
    try:
        # Giả lập kết hợp nền: Trả về ảnh nền mới
        return send_file(background_path, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({
            "status": "error",
            "code": "500",
            "message": str(e)
        }), 500

@app.route("/")
def hello_world():
    today = datetime.datetime.now()
    return f"Hôm nay là {format_date(today)}. {generate_greeting('Tuyet')}"

@app.route("/person/<name>")
def hello(name=None):
    return render_template('hello.html', person=name)

if __name__ == '__main__':
    app.run(debug=True)