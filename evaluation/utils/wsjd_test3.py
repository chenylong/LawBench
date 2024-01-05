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
    os.system('python3 parallel_to_m2.py -f tmp_pred1.para -o tmp_pred.para2.m2 -g char')
    os.system('python3 parallel_to_m2.py -f tmp_gold1.para -o tmp_gold.para2.m2 -g char')


if __name__ == '__main__':

    score = compute_wsjd2()

