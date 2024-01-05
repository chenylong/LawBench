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
def compute_wsjd2():

    output = subprocess.check_output("python3 compare_m2_for_evaluation.py -hyp tmp_pred.para.m2 -ref tmp_gold.para.m2", shell = True)

    print("0ut:", output)
    print("de:", output.decode())
    ss = output.decode().split('\t')

    for s in ss:
        print("s:", s)
    print("-1", ss[-1])
    lists = ss[-1].split('\n')
    for i in range(len(lists)):
        print("jg:" ,lists[i])
    score = float(output.decode().split('\t')[-1].split('\n')[0])
    #remove prediction files

    # os.remove('tmp_pred.para')
    # os.remove('tmp_gold.para')
    # os.remove('tmp_pred.para.m2')
    # os.remove('tmp_gold.para.m2')
    #os.chdir('..')
    return {"score": score}
if __name__ == '__main__':

    score = compute_wsjd2()
    print(score)
