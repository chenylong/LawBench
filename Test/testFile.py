import json
import os

from tqdm import tqdm

dir_name = 'E:/github/LawBenchGit/data/one_shot/'
output_dir_name = 'E:/github/LawBenchGit/nlpsearchTest/one_shot/'

def get_answer_by_json(url, data_file):
    # with open(data_file, 'r', encoding='utf-8') as f:
    #     data = json.load(f)

    dir_name = data_file

    for name in os.listdir(dir_name):
        i = 0
        if not str(name).endswith('.json'):
            continue
        path = os.path.join(dir_name, name)
        with open(path, encoding='utf-8') as fr:
            data = json.load(fr)
        texts = [data['instruction'] + ' ' + data['question'] for data in data]
        #answers = [data['answer'] for data in data]
        refrs  = [data['answer'] for data in data]
        # 接收问题、答案和反馈结果
        output = {}

        for i in tqdm(range(len(texts))):
            text = texts[i]
            refr = refrs[i]
            answer = "ok"
            new_data = {}
            new_data['origin_prompt'] = text
            new_data['prediction'] = answer
            new_data['refr'] = refr
            output[str(i)] = new_data

        print(len(output))
        with open(f'{output_dir_name}/{name}', 'w', encoding='utf-8') as fw:
            json.dump(output, fw, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    url = "http://192.168.1.169:8005/nlpsearch"

    # answer = get_answer(url, text)
    # print(answer)
    get_answer_by_json(url, dir_name)
