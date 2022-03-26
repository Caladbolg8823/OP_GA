import numpy as np
import Parse_OP
from tqdm import tqdm


fileName = 'OP/tsiligirides_problem_1_budget_85.txt'


# TODO 獲取座標、各點獲益值、最大可用時間
coords, benefit, max_time = Parse_OP.getData(fileName)


# TODO 計算距離
def distance(vec1, vec2):
    return np.linalg.norm(np.array(vec1) - np.array(vec2))


# TODO 計算每條路徑的獲益值
def Evaluation(benefit, gens):
    gens = np.copy(gens)
    P = 0
    for i, j in enumerate(gens):
        P += benefit[j]
    return P


# TODO 生成初始路徑
def init_Path(coords):
    path = []
    for i in range(population_num):
        D = 0
        a = 0
        gene = list(range(len(coords)))
        np.random.shuffle(gene)

        for j, g in enumerate(gene):
            if g == 0:
                gene[0], gene[j] = gene[j], gene[0]

        while a < len(gene):
            D += distance(coords[gene[a]], coords[gene[a+1]])
            if D > max_time:
                del gene[a:]
            a += 1
        path.append(gene)
        # print('第{}路線：{}'.format(i+1, path[i]))
    return path


if __name__ == '__main__':
    population_num = 1000
    max_evolution_num = 1
    path = init_Path(coords)

#!----------------------演算法程序-----------------------
    for step in tqdm(range(max_evolution_num)):
        Score = []
        best_Score = []
        [Score.append(Evaluation(benefit, path[i])) for i in range(len(path))]
        if Score >= best_Score:
            best_Score = Score
            best_path_idx = np.argmax(best_Score)

    print("{:=^100s}".format('這是分隔線'))
    print('最佳分數為：{}分'.format(Score[best_path_idx]))
    print('最佳路徑為第{}條路線，共拜訪了{}個點，其路徑為：\n{}'.format(
        best_path_idx+1, len(path[best_path_idx]), path[best_path_idx]))

    print('Wryyyyyyyyy')

'''
最佳分數為：160分
[0, 3, 4, 14, 15, 16, 7, 19, 21, 20, 25, 26, 27, 31, 2, 9, 10]
[0, 21, 24, 22, 26, 20, 25, 30, 27, 28, 18, 12, 11, 10, 15, 5]
[0, 27, 20, 11, 3, 2, 8, 19, 9, 30, 21, 25, 24, 23, 26, 22, 12, 13]
[0, 25, 23, 24, 17, 5, 14, 15, 16, 28, 18, 13, 19, 27, 26, 31]
'''
