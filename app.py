from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, static_folder='static', static_url_path='')
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

# Tạo thư mục nếu chưa tồn tại (dù không thực sự dùng trong mock)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


# Route để render upload.html
@app.route('/')
@app.route('/upload.html')
def serve_upload():
    return render_template('upload.html')


# Route để render result.html
@app.route('/result.html')
def serve_result():
    return render_template('result.html')


# Mock API để xóa nền
@app.route('/api/remove-background', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return jsonify({"status": "error", "code": "400", "data": "No image file provided"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"status": "error", "code": "400", "data": "No selected file"}), 400

        # Mock response: giả lập đường dẫn file đã xóa nền
        mock_output = f"/results/no_bg_{file.filename}"
        return jsonify({"status": "success", "code": "200", "data": mock_output})

    except Exception as e:
        return jsonify({"status": "error", "code": "500", "data": "Something went wrong"}), 500


# Mock API để thêm nền
@app.route('/api/add-background/<filename>', methods=['GET'])
def add_background(filename):
    try:
        # Mock response: giả lập đường dẫn file đã thêm nền
        mock_output = f"/results/final_{filename}"
        return jsonify({"status": "success", "code": "200", "data": mock_output})

    except Exception as e:
        return jsonify({"status": "error", "code": "500", "data": "Something went wrong"}), 500


if __name__ == '__main__':
    app.run(debug=True)