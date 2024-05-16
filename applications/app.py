import argparse

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from applications.KE1 import KE1_prompt
from remote.ChatGPT_Stream import ChatGPTLLM
from remote.ChatGLM3 import ChatGLMLLM


def read_args(config_path):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=str, default=config_path)
    args = parser.parse_args()
    return args


app = Flask(__name__)
CORS(app)  # 这里启用CORS，允许所有域的跨域请求

gpt_args = read_args("../remote/configs/wsx_gpt35.json")
chat_gpt = ChatGPTLLM(gpt_args.config_path)
glm_args = read_args("../remote/configs/cjh_glm3.json")
chat_glm = ChatGLMLLM(glm_args.config_path)

@app.route('/interactive', methods=['POST'])
def interactive():
    """
    交互式任务的接口
    :return:
    """
    # {
    #     "src_text": "这里是源文本",
    #     "model": "GPT-3.5",
    #     "stream": "False"
    #     "max_length": 100,
    #     "temperature": 0.5,
    #     "top_p": 1.0
    # }
    data = request.get_json()

    if data['model'] == "GPT-3.5":
        chat = chat_gpt
    elif data['model'] == "GLM-3":
        chat = chat_glm
    else:
        raise ValueError("Model not found")

    def stream():
        response = chat.interactive_dialogue(data['src_text'], use_stream=True, max_length=data["max_length"],
                                             temperature=data["temperature"], top_p=data["top_p"])
        for chunk in response:
            if chunk.choices[0].finish_reason is None:
                content = chunk.choices[0].delta.content.replace("\n", "<br>")
                yield f"data: {content}\n\n"
            else:
                event = chunk.choices[0].finish_reason
                yield f"event: {event}\n\n"
                break

    if data['stream']:
        headers = {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        }
        return Response(stream(), mimetype='text/event-stream', headers=headers)
    else:
        res = chat.interactive_dialogue(data['src_text'], use_stream=False, max_length=data["max_length"],
                                        temperature=data["temperature"], top_p=data["top_p"])
        if res is not None and res[-1]['role'] == 'assistant':
            res = res[-1]['content']
        return jsonify({
            "code": 200,
            "message": "Success",
            "data": {
                "result": res
            }
        })


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
    #     "stream": "False"
    #     "max_length": 100,
    #     "temperature": 0.5,
    #     "top_p": 1.0
    # }
    data = request.get_json()

    # 创建流式请求
    def stream():
        # 流式请求
        response = KE1_prompt(data['src_text'], data['model'], data['language'], stream=True,
                              max_length=data["max_length"], temperature=data["temperature"], top_p=data["top_p"])
        for chunk in response:
            if chunk.choices[0].finish_reason is None:
                content = chunk.choices[0].delta.content.replace("\n", "<br>")
                yield f"data: {content}\n\n"
            else:
                event = chunk.choices[0].finish_reason
                yield f"event: {event}\n\n"
                break

    # 创建Prompt并执行KE1任务
    if data['stream']:
        headers = {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        }
        # 流式请求
        return Response(stream(), mimetype='text/event-stream', headers=headers)
    else:
        # 非流式请求
        prompt, res = KE1_prompt(data['src_text'], data['model'], data['language'],
                                 max_length=data["max_length"], temperature=data["temperature"], top_p=data["top_p"])
        # print("本次请求的Prompt是", prompt)
        # print("本次请求的结果是", res)

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
