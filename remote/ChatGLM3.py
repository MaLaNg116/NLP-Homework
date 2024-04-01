import json
import logging
import argparse
import openai
from openai import OpenAI
import time
import socket

from remote import RemoteLLMs


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=str, default="configs/cjh_glm3.json")
    args = parser.parse_args()
    return args


class ChatGPTLLM(RemoteLLMs):
    def init_local_client(self):
        try:
            self.model = self.args['model']
            client = OpenAI(api_key=self.args['api_key'], base_url=self.args['base_url'])
            return client
        except:
            return None

    def create_prompt(self, current_query, context=None):
        if context is None:
            context = []
        context.append(
            {
                "role": "user",
                "content": current_query,
            }
        )
        return context

    def request_llm(self, context, seed=1234, sleep_time=1, repeat_times=0):
        while True:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=context,
                    stream=False,
                    seed=seed+repeat_times
                )
                context.append(
                    {
                        'role': response.choices[0].message.role,
                        'content': response.choices[0].message.content
                    }
                )
                return context
            except openai.RateLimitError as e:
                logging.error(str(e))
                raise e
            except (openai.APIError, openai.InternalServerError, socket.timeout) as e:
                logging.error(str(e))
                raise e
            except Exception as e:
                # 捕捉未预料的异常，考虑是否终止循环或做其他处理
                logging.error(f"An unexpected error occurred: {str(e)}")
                raise e
            time.sleep(sleep_time)

if __name__ == '__main__':
    # https://platform.openai.com/docs/api-reference
    args = read_args()
    chat_gpt = ChatGPTLLM(args.config_path)
    chat_gpt.interactive_dialogue()