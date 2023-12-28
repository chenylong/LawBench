import json
import requests
from tqdm import tqdm

def get_answer(url, text):
    data = {
        "scene": "legal_advice",
        "text": text
    }
    response = requests.post(url, json=data)
    result = response.json()
    answer = result.get("data").get("answer")
    return answer

def get_answer_by_json(url, data_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    texts = [data['instruction'] + ' ' + data['question'] for data in data]
    #answers = [data['answer'] for data in data]
    refrs  = [data['answer'] for data in data]
    # 接收问题、答案和反馈结果
    output = {}

    for i in tqdm(range(len(texts))):
        text = texts[i]
        refr = refrs[i]
        response = requests.post(url, json={"scene": "legal_advice", "text": text})
        result = response.json()
        answer = result.get("data").get("answer")
        new_data = {}
        new_data['origin_prompt'] = text
        new_data['prediction'] = answer
        new_data['refr'] = refr
        output[str(i)] = new_data

    print(len(output))
    with open(f'2-2.json', 'w', encoding='utf-8') as fw:
        json.dump(output, fw, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    url = "http://192.168.1.169:8005/nlpsearch"
    text = "酒驾有什么后果"
    data_file = "../data/one_shot/2-2.json"
    # answer = get_answer(url, text)
    # print(answer)
    get_answer_by_json(url, data_file)
