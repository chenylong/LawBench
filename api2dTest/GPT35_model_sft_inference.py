import http.client
import json
import os
import time
from time import sleep

import requests
from tqdm import tqdm

dir_name = 'E:/github/LawBenchGit/data/one_shot/'
output_dir_name = 'E:/github/LawBenchGit/api2dTest/one_shot/'
def get_answer(text):
    conn = http.client.HTTPSConnection("oa.api2d.net")
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ],
        "safe_mode": False
    })
    headers = {
        'Authorization': 'Bearer fk221359-1TrNn4btmHyLjlvp0EvnVMG8F1MsImng',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }


    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_str = data.decode("utf-8")
    datajson = json.loads(json_str,strict=False)
    print(datajson)
    content = datajson['choices'][0]['message']['content']
    print(content)
    time.sleep(5)
    return content



def get_answer_by_json(url, data_file):
    # with open(data_file, 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    dir_name = data_file

    for name in os.listdir(dir_name):
        i = 0
        print(name)
        if not str(name).endswith('.json') :
            continue

        if name != '1-2.json':
            continue
            print(name)
        path = os.path.join(dir_name, name)
        with open(path, encoding='utf-8') as fr:
            data = json.load(fr)
        texts = [data['instruction'] + ' ' + data['question'] +' 另外，请注意反馈结果的格式要求。' for data in data]
        #answers = [data['answer'] for data in data]
        refrs  = [data['answer'] for data in data]
        # 接收问题、答案和反馈结果
        output = {}

        for i in tqdm(range(len(texts))):
            text = texts[i]
            refr = refrs[i]
            # response = requests.post(url, json={"scene": "legal_advice", "text": text})
            # result = response.json()
            # answer = result.get("data").get("answer")
            new_data = {}
            new_data['origin_prompt'] = text
            new_data['prediction'] = get_answer(text)
            new_data['refr'] = refr
            output[str(i)] = new_data

        print(len(output))
        with open(f'{output_dir_name}/{name}', 'w', encoding='utf-8') as fw:
            json.dump(output, fw, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    url = ''
    # text = "请写首唐诗"
    # get_answer(url, text)

    get_answer_by_json(url, dir_name)