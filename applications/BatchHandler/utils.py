import logging

from markdown2 import markdown
from bs4 import BeautifulSoup
import uuid
import json
import re
import requests
import multiprocessing

# 配置logging
logging.basicConfig(filename='service.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s'
                    , encoding="utf-8")

# 创建一个日志器对象
logger = logging.getLogger(__name__)

# 创建锁
LOCK = multiprocessing.Lock()


def generate_task_token():
    return uuid.uuid4().hex


def detect_language(text):
    chinese_characters = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_characters = len(re.findall(r'[a-zA-Z]', text)) / 1.5
    # 判断文本的主要语言
    if chinese_characters >= english_characters:
        return 'Chinese'
    elif english_characters > chinese_characters:
        return 'English'


def push_request(token):
    global LOCK, logger
    file_search, task_search = token.split('-')
    with open(f"./cache/{file_search}.json", 'r', encoding='utf-8') as f:
        tmp = json.load(f)
        content = tmp["missions"][task_search]
    lang = detect_language(content)
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "src_text": content,
        "model": "GPT-3.5",
        "language": lang,
        "stream": False,
        "max_length": 8192,
        "temperature": 0.2,
        "top_p": 0.9
    }
    try:
        response = requests.post('http://127.0.0.1:5000/ke1', data=json.dumps(data), headers=headers)
    except Exception as e:
        logger.error('Handle %s-%s failed' % (file_search, task_search))
        with LOCK:
            with open("status.json", "r", encoding='utf-8') as f:
                tmp = json.load(f)
                tmp["waiting"][file_search].remove(task_search) if task_search in tmp["waiting"][file_search] else \
                    tmp["failed"][file_search].remove(task_search)
                tmp["failed"][file_search].append(task_search)
            with open("status.json", "w", encoding='utf-8') as f:
                json.dump(tmp, f, ensure_ascii=False, indent=4)
        return
    # 如果请求成功
    if response.status_code == 200:
        try:
            # 解析返回的结果
            soup = BeautifulSoup(markdown(response.json()['data']['result']), 'lxml')
            # 尝试解析json数据
            with LOCK:
                with open(f"./cache/{file_search}.json", "r", encoding='utf-8') as f:
                    tmp = json.load(f)
                    for i in json.loads(soup.find('code').string.lstrip('json'))['Triad']:
                        tmp["results"].append(i)
                with open(f"./cache/{file_search}.json", "w", encoding='utf-8') as f:
                    json.dump(tmp, f, ensure_ascii=False, indent=4)
            # 若解析成功，将任务从waiting中移除，添加到done中
            with LOCK:
                with open("status.json", "r", encoding='utf-8') as f:
                    tmp = json.load(f)
                    tmp["waiting"][file_search].remove(task_search) if task_search in tmp["waiting"][file_search] else \
                        tmp["failed"][file_search].remove(task_search)
                    tmp["done"][file_search].append(task_search)
                with open("status.json", "w", encoding='utf-8') as f:
                    json.dump(tmp, f, ensure_ascii=False, indent=4)
            logger.info('Handle %s-%s succeed' % (file_search, task_search))
        # 若解析失败，将任务从waiting中移除，添加到failed中
        except Exception as e:
            with LOCK:
                with open("status.json", "r", encoding='utf-8') as f:
                    tmp = json.load(f)
                    tmp["waiting"][file_search].remove(task_search) if task_search in tmp["waiting"][file_search] else \
                        tmp["failed"][file_search].remove(task_search)
                    tmp["failed"][file_search].append(task_search)
                with open("status.json", "w", encoding='utf-8') as f:
                    json.dump(tmp, f, ensure_ascii=False, indent=4)
                logger.warning('Handle %s-%s failed' % (file_search, task_search))
    else:
        # 若请求失败，将任务从waiting中移除，添加到failed中
        with LOCK:
            with open("status.json", "r", encoding='utf-8') as f:
                tmp = json.load(f)
                tmp["waiting"][file_search].remove(task_search) if task_search in tmp["waiting"][file_search] else \
                    tmp["failed"][file_search].remove(task_search)
                tmp["failed"][file_search].append(task_search)
            with open("status.json", "w", encoding='utf-8') as f:
                json.dump(tmp, f, ensure_ascii=False, indent=4)
        logger.warning('Handle %s-%s failed' % (file_search, task_search))


def main():
    # 创建任务队列和结果队列
    task_queue = []

    # 创建进程池
    pool = multiprocessing.Pool(processes=4)

    with LOCK:
        # 向任务队列中添加初始任务
        with open("status.json", "r", encoding='utf-8') as f:
            tmp = json.load(f)
            for file_id, task_ids in tmp["failed"].items():
                for task_id in task_ids:
                    task_queue.append(f"{file_id}-{task_id}")
            for file_id, task_ids in tmp["waiting"].items():
                for task_id in task_ids:
                    task_queue.append(f"{file_id}-{task_id}")

    # 启动工作进程
    pool.map(push_request, task_queue)
    # 关闭进程池，不再接收新的任务
    pool.close()

    # 等待所有任务完成
    pool.join()


def start_uuid(file_uid):
    global LOCK
    # 创建任务队列和结果队列
    task_queue = []

    # 创建进程池
    pool = multiprocessing.Pool(processes=4)

    with LOCK:
        # 向任务队列中添加初始任务
        with open("status.json", "r", encoding='utf-8') as f:
            tmp = json.load(f)
            for task_id in tmp["failed"][file_uid]:
                task_queue.append(f"{file_uid}-{task_id}")
            for task_id in tmp["waiting"][file_uid]:
                task_queue.append(f"{file_uid}-{task_id}")

    # 启动工作进程
    pool.map(push_request, task_queue)
    # 关闭进程池，不再接收新的任务
    pool.close()

    # 等待所有任务完成
    pool.join()

    if get_degree(file_uid) != 1:
        return {"results": get_degree(file_uid)}
    else:
        with open(f"./cache/{file_uid}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data


def get_degree(file_uid):
    global LOCK
    with LOCK:
        with open("./status.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        total = data["waiting"][file_uid] + data["done"][file_uid] + data["failed"][file_uid]
        success = data["done"][file_uid]

    return len(success) / len(total)


if __name__ == "__main__":
    # main()
    # start("4d18ffca48af4305b5c168f046c0b7e4")
    get_degree("4d18ffca48af4305b5c168f046c0b7e4")
