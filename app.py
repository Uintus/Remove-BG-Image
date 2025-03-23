from flask import Flask, render_template, request, jsonify, send_file
from model.demo import format_date, generate_greeting
import datetime
import os
import uuid

app = Flask(__name__)

# Thư mục lưu trữ ảnh tạm thời
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Endpoint để tải ảnh lên
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Lưu ảnh tải lên
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200

# Endpoint để lấy ảnh đã xóa nền
@app.route('/result', methods=['GET'])
def get_result():
    file_path = request.args.get('file_path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    # Xóa nền ảnh (Mock test trả về chính ảnh gốc)
    result_path = file_path # Không thay đổi hình ảnh
    
    return send_file(result_path, mimetype='image/png')


# Endpoint để lấy ảnh đã kết hợp với nền mới
@app.route('/combine', methods=['GET'])
def combine_background():
    file_path = request.args.get('file_path')
    background_path = request.args.get('background_path')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    if not background_path or not os.path.exists(background_path):
        return jsonify({"error": "Background file not found"}), 404
    
    # Giả lập kết hợp nền: Trả về ảnh nền mới
    combined_path = background_path  # Trả về ảnh nền mới
    
    return send_file(combined_path, mimetype='image/png')

@app.route("/")
def hello_world():
    today = datetime.datetime.now()
    return f"Hôm nay là {format_date(today)}. {generate_greeting('Tuyet')}"

@app.route("/person/<name>")
def hello(name=None):
    return render_template('hello.html', person=name)

if __name__ == '__main__':
    app.run(debug=True)
