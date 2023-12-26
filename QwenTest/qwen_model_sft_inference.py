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

dir_name = '/home/caijj/huixin/model_val/evaluate_datasets'
output_dir_name = '/home/caijj/huixin/model_val/evaluate_datasets_output'
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
            json.dump(output,fw,ensure_ascii=False)

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
