from rouge_chinese import Rouge
import jieba
from nltk.translate.gleu_score import corpus_gleu

def compute_f1_two_sets(pred_set, gt_set):
    precision = len(pred_set.intersection(gt_set)) / len(pred_set) if len(pred_set) > 0 else 0
    recall = len(pred_set.intersection(gt_set)) / len(gt_set) if len(gt_set) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
    return f1

# 这段代码定义了一个名为multi_choice_judge的函数，用于判断预测结果与选项列表之间的匹配情况。
# 函数使用一个字典count_dict来统计预测结果中每个选项的出现次数。如果预测结果中没有任何选项，则 abstention为1。
# 如果预测结果中包含答案选项，并且只包含一个选项，则 accuracy为1。最后，函数返回一个包含score和abstention的字典
def multi_choice_judge(prediction, option_list, answer_token):
    # a dict, key: letters in the option list, value: count of the letter in the prediction
    count_dict, abstention, accuracy = {}, 0, 0
    for option in option_list:
        option_count = prediction.count(option)
        count_dict[option] = 1 if option_count > 0 else 0  # multiple occurrence of the same letter is counted as 1

    if sum(count_dict.values()) == 0:
        abstention = 1
    # if the answer token is the only predicted token, the prediction is correct 
    elif count_dict[answer_token] == 1 and sum(count_dict.values()) == 1:
        accuracy = 1
    return {"score": accuracy, "abstention": abstention}

"""
compute the rouge score.
hyps and refs are lists of hyposisis and reference strings
empty predictions are replaces with 无内容
"""


def compute_rouge(hyps, refs):
    assert(len(hyps) == len(refs))
    # 使用 使用结巴分词工具对假设结巴分词工具对假设和参考进行分词
    hyps = [' '.join(jieba.cut(h)) for h in hyps]
    # 对假设和参考中为空内容的字符串进行处理，参考中的空字符串进行处理，替换为"无内容"
    hyps = [h if h.strip() != "" else "无内容" for h in hyps]
    refs = [' '.join(jieba.cut(r)) for r in refs]
    return Rouge().get_scores(hyps, refs)


"""
compute the gleu score.
hyps and refs are lists of hyposisis and reference strings
empty predictions are replaces with 无内容
"""
def compute_gleu(hyps, refs):
    assert(len(hyps) == len(refs))
    hyps = [' '.join(jieba.cut(h)) for h in hyps]
    hyps = [h if h.strip() != "" else "无内容" for h in hyps]
    refs = [[' '.join(jieba.cut(r))] for r in refs]
    return corpus_gleu(refs, hyps)
