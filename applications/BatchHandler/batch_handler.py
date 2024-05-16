import json
import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import generate_task_token, LOCK, main, start_uuid

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload_json():
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    # 获取上传的文件
    file = request.files['file']

    # 检查文件是否为JSON格式
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # 保存文件
        filename = file.filename
        file_id = generate_task_token()
        save_path = f'./storage/{file_id}/{filename}'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)

        # 读取文件内容并解析为JSON
        with open(save_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            data_queue = [generate_task_token() for _ in range(len(data))]
        with LOCK:
            with open("status.json", "r", encoding='utf-8') as f:
                tmp = json.load(f)
                tmp["waiting"][file_id] = data_queue
                tmp["failed"][file_id] = []
                tmp["done"][file_id] = []
            with open("status.json", "w", encoding='utf-8') as f:
                json.dump(tmp, f, ensure_ascii=False, indent=4)
            with open(f"./cache/{file_id}.json", "w", encoding='utf-8') as f:
                cache_dict = {
                    "missions": {},
                    "results": []
                }
                for task_id, content in zip(data_queue, data):
                    cache_dict["missions"][task_id] = content
                json.dump(cache_dict, f, ensure_ascii=False, indent=4)
            time.sleep(5)

        # 返回成功的响应
        return jsonify({"uuid": file_id}), 200


@app.route('/restart_all', methods=['GET'])
def restart():
    main()
    return jsonify({"message": "Restarted"}), 200


@app.route('/start', methods=['GET'])
def start():
    file_uid = request.args.get("file_uid")
    data = start_uuid(file_uid)
    result = data["results"]

    return jsonify(result), 200


# 检查文件扩展名是否允许
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'json'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
