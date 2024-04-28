from flask import Flask, request, jsonify
from flask_cors import CORS
from applications.KE1 import KE1_prompt

app = Flask(__name__)
CORS(app)  # 这里启用CORS，允许所有域的跨域请求


@app.route('/ke1', methods=['POST'])
def ke1():
    """
    KE1任务的接口
    :return: 返回KE1任务的结果
    """
    # 获取请求数据
    # 请求数据格式为：
    # {
    #     "src_text": "这里是源文本",
    #     "model": "GPT-3.5",
    #     "language": "Chinese"
    # }
    data = request.get_json()

    # 创建Prompt并执行KE1任务
    prompt, res = KE1_prompt(data['src_text'], data['model'], data['language'])
    print("本次请求的Prompt是", prompt)
    print("本次请求的结果是", res)

    # 返回响应
    return jsonify({
        "code": 200,
        "message": "Success",
        "data": {
            "prompt": prompt,
            "result": res
        }
    })


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
