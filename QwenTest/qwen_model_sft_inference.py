import sys
import torch
import json
import re
import os
import pandas as pd
from tqdm import tqdm
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer,AutoModelForCausalLM
from transformers.generation import GenerationConfig
import openai

dir_name = '/home/caijj/huixin/model_val/evaluate_datasets'
output_dir_name = '/home/caijj/huixin/model_val/evaluate_datasets_output'
'''把指定目录下的json文件读取，调用模型和分词器进行聊天生成，将生成结果保存到字典中，最后将字典保存到文件中。'''
def predicition(model,tokenizer,config):
    for name in os.listdir(dir_name):
        output = {}
        i = 0
        if not str(name).endswith('.json'):
            continue
        path = os.path.join(dir_name,name)
        with open(path,encoding='utf-8') as fr:
            data_json = json.load(fr)
        for data in tqdm(data_json):
            new_data = {}
            prompt = data['instruction'] + data['question']
            print(prompt)
            new_data['origin_prompt'] = prompt
            new_data['refr'] = data['answer']
            response, _ = model.chat(tokenizer, prompt, history=None,generation_config=config)
            print(response)
            new_data['prediction'] = response
            output[str(i)] = new_data
            i += 1
        print(len(output))
        with open(f'{output_dir_name}/{name}','w',encoding='utf-8') as fw:
            json.dump(output,fw,ensure_ascii=False, indent=4)



# def predictOpenAi(model, tokenizer, config):
#     for name in os.listdir(dir_name):
#         output = {}
#         i = 0
#         if not str(name).endswith('.json'):
#             continue
#         path = os.path.join(dir_name,name)
#         with open(path,encoding='utf-8') as fr:
#             data_json = json.load(fr)
#         for data in tqdm(data_json):
#             new_data = {}
#             prompt = data['instruction'] + data['question']
#             print(prompt)
#             new_data['origin_prompt'] = prompt
#             new_data['refr'] = data['answer']
#             response, _ = openai.Completion.create(
#                 engine=model,
#                 prompt=prompt,
#                 max_tokens=50,
#                 temperature=0.5,
#                 top_p=1.0,
#                 n=1,
#                 stop=None,
#                 temperature=config['temperature'],
#                 max_tokens=config['max_tokens']
#             )
#             print(response.choices[0].text)
#             new_data['prediction'] = response.choices[0].text
#             output[str(i)] = new_data
#             i += 1
#         print(len(output))
#         with open(f'{output_dir_name}/{name}','w',encoding='utf-8') as fw:
#             json.dump(output,fw,ensure_ascii=False, indent=4)


if __name__ == '__main__':
    qwen_model_path = '/home/caijj/huixin/model_val/qwen_pretrain_merge_chat_model'
    path_to_adapter = '/home/caijj/huixin/model_val/qwen_checkpoints'
    tokenizer = AutoTokenizer.from_pretrained(qwen_model_path, trust_remote_code=True)
    config = GenerationConfig.from_pretrained(qwen_model_path, trust_remote_code=True,resume_download=True,)
    model = AutoPeftModelForCausalLM.from_pretrained(
        path_to_adapter,
        device_map="auto",
        trust_remote_code=True,
        bf16=True,fp16=False,fp32=False
        ).eval()
    chat_model = model.merge_and_unload()
    chat_model.generation_config = config
    predicition(chat_model,tokenizer,config)
    print(f'process completely...')
