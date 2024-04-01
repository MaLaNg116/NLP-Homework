import argparse
import json

from llms.applications.scoring_prompts import TEXT_EVAL_GENERAL_PROMPT_PATTERN, TEXT_EVAL_METRICS
from llms.applications.tmp_utils import set_logger
from llms.remote import RemoteLLMs
from llms.remote.ChatGPT import ChatGPTLLM


class ScoringAgent:
    def __init__(self, logger, llm_model: RemoteLLMs, task_name: str, metrics: dict,
                 language, src_term, tgt_term, in_context_examples=[],
                 more_guidance=[], more_task_definition=[]):
        """

        :param logger:
        :param llm_model: 给定一个RemoteLLMs的实例化对象
        :param task_name:  需要指定该评分任务的语言
        :param metrics: 需要评价的指标 key-value
        :param language:  数据的语言
        :param src_term: 在输入数据里，每一个上文的Key值，可选
        :param tgt_term: 在输入数据里，每一个待评价部分Key值，可选
        :param in_context_examples: 如果需要给定In Context的例子，给对应的数组，每个例子一个Dict
        :param more_guidance: 通过的数组的形式提供补助
        :param more_task_definition:  通过数组的形式提供更多的任务定义补充
        """
        self.logger = logger
        self.llm_model = llm_model
        self.prompt_pattern = TEXT_EVAL_GENERAL_PROMPT_PATTERN
        self.result_pattern = metrics

        # 处理额外的输入
        more_task_definition = '\n'.join(more_task_definition)

        # 评价的指标
        metric_dict = dict()
        data_type = None
        min_score = None
        max_score = None
        for metric, score_format in metrics.items():
            metric_dict[metric] = "[Your Score]"
            items = score_format.split('_')

            if data_type is None:
                data_type = items[0]
                min_score = items[1]
                max_score = items[2]
            else:
                assert data_type == items[0]
                assert min_score == items[1]
                assert max_score == items[2]

        output_pattern = json.dumps(metric_dict, ensure_ascii=False, indent=4)

        # In-Context Examples 的设置
        if len(in_context_examples) > 0:
            more_guidance.append('To help your judgment, some examples are provided in [Examples].')
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
        for idx, metric in enumerate(metrics):
            tmp = TEXT_EVAL_METRICS[metric]
            if src_term is None:
                assert "{{SRC}}" not in tgt_term, "当前Metric要求有{{SRC}}"
            else:
                input_format[src_term] = '{{SRC_VALUE}}'

            input_format[tgt_term] = '{{TGT_VALUE}}'

            tmp = tmp.replace("{{SRC}}", src_term)
            tmp = tmp.replace("{{TGT}}", tgt_term)
            criteria.append('%d. %s' % (idx + 1, tmp))

        criteria = '\n'.join(criteria)

        # 给定输入的模板格式
        input_format = json.dumps(input_format, ensure_ascii=False, indent=4)

        self.meta_dict = {
            "{{DATATYPE}}": "an integer" if data_type == "int" else "a float",
            "{{SRC}}": src_term,
            "{{TGT}}": tgt_term,
            "{{MIN_SCORE}}": min_score,
            "{{MAX_SCORE}}": max_score,
            "{{Language}}": language,
            "{{Output}}": output_pattern,
            "{{Input}}": input_format,
            "{{Criteria}}": criteria,
            "{{TASK_NAME}}": task_name,
            "{{MORE_GUIDANCE}}": more_guidance,
            "{{MORE_TASK_DEFINITION}}": more_task_definition,
            "{{In-Context Examples}}": in_context_prompt
        }

    def judge_a_case(self, case_data):
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
                extracted_results = self.extract_scores(results[-1]['content'])
                if extracted_results is not None:
                    return prompt, extracted_results

        return None

    def extract_scores(self, last_response: str):
        try:
            last_response = last_response.strip('\r\n')
            # 找到JSON字符串的开始和结束位置
            start = last_response.find('{')
            end = last_response.rfind('}') + 1

            # 提取JSON字符串
            json_str = last_response[start:end]
            json_str = json_str.replace("\n", "")

            # 将JSON字符串解析为Python字典
            print(json_str)
            data_dict = json.loads(json_str)

            res_dict = {}

            # 随后需要根据Output的Pattern做检查
            for k, v in self.result_pattern.items():
                # 首先检查是否存在，不存在return None
                if k not in data_dict:
                    return None
                # 检查值的有效性

                value = data_dict[k]
                if isinstance(value, str):
                    value = value.strip('\r\n')

                strict_flag = False
                data_type = float
                items = v.split("_")

                # 判定支持的数据类型
                if items[0].upper() == 'INT':
                    data_type = int
                elif items[0].upper() == 'FLOAT':
                    data_type = float

                # 判定是否严格模式
                if items[0].upper() == items[0]:
                    strict_flag = True

                # 转换数值
                if strict_flag:
                    value = data_type(value)
                else:
                    value = data_type(float(value))

                # 最大最小值
                if len(items) >= 2:
                    min_value = data_type(items[1])
                else:
                    min_value = -float('INFINITY')

                if len(items) >= 3:
                    max_value = data_type(items[2])
                else:
                    max_value = float('INFINITY')

                if value < min_value or value > max_value:
                    if strict_flag:
                        return None
                    value = max(min_value, value)
                    value = min(max_value, value)

                # 检查完成
                res_dict[k] = value

            return res_dict
        except Exception as e:
            raise e
            return None


if __name__ == '__main__':
    # https://platform.openai.com/docs/api-reference

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=str, default="../remote/configs/wsx_gpt35.json")
    args = parser.parse_args()

    # 定义一个Logger
    logger = set_logger("tmp.log")

    # 定义一个Agent
    chat_gpt = ChatGPTLLM(args.config_path)

    # 定义参数
    task_name = "Dialogue Response Evaluation"
    src_term = "Dialogue History"
    tgt_term = "Dialogue Response"
    language = "Chinese"

    result_pattern = {
        "Fluency": "float_1_5",
        "Relevance": "float_1_5",
        "Informativeness": "float_1_5",
    }

    more_guidance = ['Each score should have two digits.']

    in_context_examples = [
        {
            "Input": {
                "Dialogue History": "我觉得你是个坏人。",
                "Dialogue Response": "我也觉得你好坏",
            },
            "Output": {
                "Fluency": "4.4",
                "Relevance": "4.1",
                "Informativeness": "2.3",
            }
        }
    ]

    score_agent = ScoringAgent(logger, chat_gpt, task_name, result_pattern,
                               language=language, src_term=src_term, tgt_term=tgt_term,
                               more_guidance=more_guidance, in_context_examples=in_context_examples)
    data = {
        "{{SRC_VALUE}}": "我觉得你是个好人。 我好喜欢你",
        "{{TGT_VALUE}}": "好好学习 天台呢向上。",
    }
    prompt, res = score_agent.judge_a_case(data)
    print("本次请求的Prompt是", prompt)
    print("本次请求的结果是", res)
