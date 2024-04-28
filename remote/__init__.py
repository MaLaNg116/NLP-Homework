import json
import os
from dotenv import load_dotenv, find_dotenv


class RemoteLLMs:

    def init_local_client(self):
        """
        初始化用户的客户端
        :param args:
        :return:
        """
        raise NotImplementedError()

    def __load_args(self, config_path):
        # 首先读取Config
        load_dotenv(find_dotenv("./configs/API.env"))
        self.args = json.load(open(config_path))
        # 读取环境变量
        if self.args["model"] == "gpt-3.5-turbo":
            self.args["api_key"] = os.getenv("OPENAI_API_KEY")
            self.args["base_url"] = os.getenv("OPENAI_BASE_URL")
        elif self.args["model"] == "chatglm3-6b":
            self.args["api_key"] = os.getenv("ZHIPU_API_KEY")
            self.args["base_url"] = os.getenv("ZHIPU_BASE_URL")

    def __init__(self, config_path):
        # 首先读取Config
        self.__load_args(config_path)
        self.max_retries = self.args.get("max_retries", 5)
        self.client = None
        for idx in range(self.max_retries):
            model = self.init_local_client()
            if model is not None:
                self.client = model
                break
        if self.client is None:
            raise ModuleNotFoundError()

    def create_prompt(self, history, current_query):
        pass

    def request_llm(self, context, seed=1234, sleep_time=1, repeat_times=0, use_stream=False, max_length=100,
                    temperature=0.5, top_p=1.0):
        pass

    def fit_case(self, pattern: str, data: dict, meta_dict: dict = None):

        if meta_dict is not None:
            for k,v in meta_dict.items():
                pattern = pattern.replace(k, str(v))

        for k, v in data.items():
            pattern = pattern.replace(k, str(v))

        assert '{{' not in pattern, pattern
        assert '}}' not in pattern, pattern
        return pattern


    def interactive_dialogue(self):
        """
        进行交互式的对话，进行模型检查
        :return:
        """
        contexts = []
        while True:
            current_query = input("请输入当前你的对话(输入'CLEAN'清除上下文，'END'离开对话)：")
            if current_query == "CLEAN":
                contexts = []
                print("已经清除上下文")
                continue
            elif current_query == "END":
                return
            contexts = self.create_prompt(current_query, contexts)
            results = self.request_llm(contexts)
            print("%s\t%s" % (results[-1]['role'], results[-1]['content']))
