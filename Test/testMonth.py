import math

if __name__ == '__main__':
    score_list = []
    a = abs(math.log(12 + 1) - math.log(13 + 1))
    print(math.log(3 + 1))
    print(math.log(4 + 1))
    print(a)
    b = abs(math.log(6 + 1) - math.log(9 + 1))
    score_list.append(a)
    score_list.append(b)
    log_distance = sum(score_list) / len(score_list)
    # normalize the score to between 0 and 1
    log_distance = (math.log(216) - log_distance) / math.log(216)

    print("评分 ：",log_distance)

    ss = 'TP	FP	FN	Prec	Rec	F0.5\n1	0	0	1.0	1.0	1.0'
    ss.split('\n')[0]
    print(ss)