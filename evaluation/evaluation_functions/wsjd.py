# -*- coding: utf-8 -*-
import re
import os
import subprocess

"""
Task: legal document grammar correction
Metric: F0.5 score
文书校对
该函数用于计算WSJD分数。输入为一个数据字典，
输出为一个包含分数的字典。函数内部步骤包括：
从数据字典中提取原始问题、预测结果和参考结果，并将它们存储在列表中；
生成用于ChERRANT输入的文件；
设置环境变量并调用脚本将预测结果和参考结果转换为不同格式的文件；
调用评估脚本进行比较并获取分数；删除临时文件并返回包含分数的字典。

"""
def compute_wsjd(data_dict):
    origins, references, predictions = [], [], []
    for example in data_dict:
        question, prediction, answer = example["origin_prompt"], example["prediction"], example["refr"]
        if isinstance(question, list):
            question = question[0]['prompt']
        start = question.index('句子：\n') + 4
        origins.append(re.sub(r'\n|\t', '', question[start:].split('\n')[0]))
        # truncate predictions >5 tokens longer than the reference
        prediction = re.sub(r'\n|\t', '', prediction)
        if len(prediction) - len(answer) > 5:
            prediction = prediction[:len(answer) + 5]
        if len(prediction) == 0:
            prediction = "无内容"
        predictions.append(prediction)
        references.append(re.sub(r'\n|\t', '', answer))

    #generate input files for ChERRANT
    preds = [f'{i} \t {origin} \t {prediction} \n' for i, (origin, prediction) in enumerate(zip(origins, predictions))]
    golds = [f'{i} \t {origin} \t {reference} \n' for i, (origin, reference) in enumerate(zip(origins, references))]
    os.chdir('utils')
    with open('tmp_pred.para', 'w', encoding="utf-8") as f:
        f.writelines(preds)
    with open('tmp_gold.para', 'w', encoding="utf-8") as f:
        f.writelines(golds)
    os.environ['KMP_DUPLICATE_LIB_OK']='True'

    os.system('python3 parallel_to_m2.py -f tmp_pred.para -o tmp_pred.para.m2 -g char')
    os.system('python3 parallel_to_m2.py -f tmp_gold.para -o tmp_gold.para.m2 -g char')
    output = subprocess.check_output("python3 compare_m2_for_evaluation.py -hyp tmp_pred.para.m2 -ref tmp_gold.para.m2", shell = True)
    score = float(output.decode().split('\t')[-1].split('\n')[0])
    #remove prediction files

    os.remove('tmp_pred.para')
    os.remove('tmp_gold.para')
    os.remove('tmp_pred.para.m2')
    os.remove('tmp_gold.para.m2')
    os.chdir('..')
    return {"score": score}
