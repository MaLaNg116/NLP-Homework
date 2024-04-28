import argparse
import json

from applications.KE1_prompt import KNOWLEDGE_EXTRACT_GENERAL_PROMPT_PATTERN, KNOWLEDGE_EXTRACT_METRICS
from applications.tmp_utils import set_logger
from remote import RemoteLLMs
from remote.ChatGPT import ChatGPTLLM
from remote.ChatGLM3 import ChatGLMLLM


class KE1Agent:
    def __init__(self, logger, llm_model: RemoteLLMs, task_name: str, metrics: dict,
                 language, text_term, in_context_examples=[],
                 more_guidance=[], more_task_definition=[]):
        """

        :param logger:
        :param llm_model: 给定一个RemoteLLMs的实例化对象
        :param task_name:  需要指定该评分任务的语言
        :param metrics: 三元组各部分的解释
        :param language:  数据的语言
        :param text_term: 源上下文
        :param in_context_examples: 如果需要给定In Context的例子，给对应的数组，每个例子一个Dict
        :param more_guidance: 通过的数组的形式提供补助
        :param more_task_definition:  通过数组的形式提供更多的任务定义补充
        """
        self.logger = logger
        self.llm_model = llm_model
        self.prompt_pattern = KNOWLEDGE_EXTRACT_GENERAL_PROMPT_PATTERN
        self.result_pattern = metrics

        # 处理额外的输入
        more_task_definition = '\n'.join(more_task_definition)

        output_pattern = json.dumps(metrics, ensure_ascii=False, indent=4)

        # In-Context Examples 的设置
        if len(in_context_examples) > 0:
            more_guidance.append('To help your extraction, some examples are provided in [Examples].')
            in_context_prompt = ["[Examples]", "'''"]
            in_context_prompt.append(json.dumps(in_context_examples, ensure_ascii=False, indent=4))
            in_context_prompt.append("'''")
            in_context_prompt = '\n'.join(in_context_prompt)
        else:
            in_context_prompt = ""

        # 是否有更多需要补充的指南
        tmp = []
        for idx, guidance in enumerate(more_guidance):
            tmp.append('%s. %s' % (idx + 4, guidance))
        more_guidance = '\n'.join(tmp)

        # 根据评价指标设置评价的标准
        input_format = {}
        criteria = []
        tmp = [value for key, value in metrics.items()]
        tmp2 = [item for sublist in tmp for item in sublist]
        for idx, metric in enumerate(tmp2):
            criteria.append('%d. %s' % (idx + 1, KNOWLEDGE_EXTRACT_METRICS[metric]))

        criteria = '\n'.join(criteria)

        # 给定输入的模板格式
        input_format = json.dumps(input_format, ensure_ascii=False, indent=4)

        self.meta_dict = {
            "{{TEXT}}": text_term,
            "{{Language}}": language,
            "{{Output}}": output_pattern,
            "{{Input}}": input_format,
            "{{Criteria}}": criteria,
            "{{TASK_NAME}}": task_name,
            "{{MORE_GUIDANCE}}": more_guidance,
            "{{MORE_TASK_DEFINITION}}": more_task_definition,
            "{{In-Context Examples}}": in_context_prompt
        }

    def extract_triads(self, case_data):
        llm_model = self.llm_model
        repeat_times = -1

        while True:
            repeat_times += 1
            if repeat_times >= llm_model.max_retries:
                break
            # 首先构造prompt
            prompt = llm_model.fit_case(pattern=self.prompt_pattern, data=case_data, meta_dict=self.meta_dict)
            contexts = llm_model.create_prompt(prompt)
            results = llm_model.request_llm(contexts, repeat_times=repeat_times)

            if results is not None and results[-1]['role'] == 'assistant':
                return prompt, results[-1]['content']

        return None


def KE1_prompt(src_text: str, model: str = "GPT-3.5", language: str = "Chinese"):
    parser = argparse.ArgumentParser()

    if model == "GPT-3.5":
        # 使用GPT-3.5，加载参数
        parser.add_argument("--config_path", type=str, default="../remote/configs/wsx_gpt35.json")
        args = parser.parse_args()
        # 定义Agent
        chat_agent = ChatGPTLLM(args.config_path)
    elif model == "GLM-3":
        # 使用GLM-3，加载参数
        parser.add_argument("--config_path", type=str, default="../remote/configs/cjh_glm3.json")
        args = parser.parse_args()
        # 定义Agent
        chat_agent = ChatGLMLLM(args.config_path)
    else:
        # 抛出模型不存在的异常
        raise ValueError("Model not found")

    # 定义一个Logger
    logger = set_logger("tmp.log")

    # 定义参数
    task_name = "Triad Extraction for General Knowledge"
    text_term = "Source Text"

    result_pattern = {
        "Triad": [
            "Head Entity", "Relationship", "Tail Entity"
        ]
    }

    more_guidance = []

    in_context_examples = [
        {
            "Input": {
                "Source Text": "百度公司的创始人是李彦宏。"
            },
            "Output": {
                "Triad": [
                    ("百度公司", "创始人", "李彦宏")
                ]
            }
        }
    ] if language == "Chinese" else [
        {
            "Input": {
                "Source Text": "The founder of Baidu is Robin Li."
            },
            "Output": {
                "Triad": [
                    ("Baidu", "founder", "Robin Li")
                ]
            }
        }
    ]

    score_agent = KE1Agent(logger, chat_agent, task_name, result_pattern,
                               language=language, text_term=text_term,
                               more_guidance=more_guidance, in_context_examples=in_context_examples)
    data = {
        "{{TEXT_VALUE}}": src_text
    }
    prompt, res = score_agent.extract_triads(data)
    res = json.loads(res)["Triad"]

    return prompt, res


if __name__ == '__main__':
    # https://platform.openai.com/docs/api-reference

    src_text = "习近平说，今年是中美建交45周年。45" \
               "年的中美关系历经风风雨雨，给了我们不少重要启示：两国应该做伙伴，而不是当对手；应该彼此成就，而不是互相伤害；应该求同存异，而不是恶性竞争；应该言必信、行必果，而不是说一套、做一套。我提出相互尊重、和平共处、合作共赢三条大原则，既是过去经验的总结，也是走向未来的指引。"

    KE1_prompt(src_text, "GPT-3.5", "Chinese")
