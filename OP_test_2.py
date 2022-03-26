import numpy as np
import Parse_OP
from tqdm import trange

fileName = 'OP/tsiligirides_problem_1_budget_85.txt'


# TODO 獲取座標、各點獲益值、最大可用時間
coords, benefit, max_time = Parse_OP.getData(fileName)


# TODO 距離矩陣
def compute_dis_mat(population_num, coords):
    dis_array = np.zeros((population_num, population_num))
    for i in range(population_num):
        for j in range(population_num):
            if i == j:
                dis_array[i][j] = np.inf
                continue
            a = coords[i]
            b = coords[j]
            tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))
            dis_array[i][j] = tmp
    return dis_array


# TODO 計算每條路徑的獲益值
def Evaluation(benefit, gens):
    gens = np.copy(gens)
    P = 0
    for i, j in enumerate(gens):
        if i == 0:
            continue
        P += benefit[j]
    return P


# TODO 初始路徑(貪婪法)
def init_greedy(dis_array, population_num, benefit):
    start_index = 0
    path = []
    for i in range(population_num):
        use_time = 0
        node = [x for x in range(0, population_num)]
        current = start_index
        node.remove(current)
        result_one = [current]
        while use_time <= max_time:  # ? 尋找每步最大獲益、最小距離的點
            point_max = -1
            tmp_choose = -1
            for x in node:
                greedy_point = benefit[x] / dis_array[current][x]
                if greedy_point > point_max:
                    point_max = greedy_point  # ? 當前最大獲益
                    min_time = dis_array[current][x]  # ? 當前最短時間
                    tmp_choose = x
            use_time += min_time

            current = tmp_choose
            result_one.append(tmp_choose)
            node.remove(tmp_choose)

        # ? 去掉超過的時間及點
        use_time -= min_time
        del result_one[-1]

        path.append(result_one)
        start_index += 1

    return path


# TODO 選擇優良父代
def choice(path):
    n = len(path)
    score = []
    [score.append(Evaluation(benefit, path[i])) for i in range(n)]
    score = np.array(score)

    sort_index = np.argsort(-score).copy()
    sort_index = sort_index[0:int(
        choice_pro * len(sort_index))]  # ? 選出分數前20%的路徑

    parents = []
    parents_score = []
    for index in sort_index:
        parents.append(path[index])
        parents_score.append(score[index])
    return parents


# TODO 輪盤法
def roulette_wheel(score, path):
    total_score = sum(score)
    pick = np.random.random()
    p = 0
    for j in range(len(path)):
        p += score[j] / total_score
        # print(p)
        if p >= pick:
            return j


# TODO 使新路線符合長度
def fix_path(dis_array, bug_path):
    bug_path = list(set(bug_path))  # ? 去除重複元素
    for i, v in enumerate(bug_path):
        if v == dummy:
            del bug_path[i]

    use_time = 0
    a = 0
    while a < len(bug_path)-1:
        use_time += dis_array[bug_path[a]][bug_path[a+1]]
        if use_time > max_time:
            del bug_path[a:]
        a += 1
    return bug_path


# TODO 交配
def cross(path):
    while len(path) < population_num:
        n = len(path)
        score = []
        [score.append(Evaluation(benefit, path[i])) for i in range(n)]
        score = np.array(score)

        parent1 = roulette_wheel(score, path)  # ? 利用輪盤法選出好的染色體
        parent2 = roulette_wheel(score, path)

        if parent1 == parent2:
            continue

        while len(path[parent1]) - len(path[parent2]) < 0:
            path[parent1].append(dummy)
        while len(path[parent1]) - len(path[parent2]) > 0:
            path[parent2].append(dummy)

        gens_len = len(path[parent1])

        index1 = np.random.randint(1, gens_len)  # ? 第一切點
        index2 = np.random.randint(index1, gens_len)  # ? 第二切點

        if index1 == index2:
            continue

        temp_gen1 = path[parent1][index1:index2]  # 交配的基因片段1
        temp_gen2 = path[parent2][index1:index2]  # 交配的基因片段2

        # 交配、插入基因片段
        temp_parent1, temp_parent2 = np.copy(
            path[parent1]).tolist(), np.copy(path[parent2]).tolist()
        temp_parent1[index1:index2] = temp_gen2
        temp_parent2[index1:index2] = temp_gen1

        # 消除衝突
        pos = index1 + len(temp_gen1)  # 插入交配基因片段的结束位置
        conflict1_ids, conflict2_ids = [], []
        [conflict1_ids.append(i) for i, v in enumerate(temp_parent1) if v in temp_parent1[index1:pos]
         and i not in list(range(index1, pos))]  # ? i引數；v為值
        [conflict2_ids.append(i) for i, v in enumerate(temp_parent2) if v in temp_parent2[index1:pos]
         and i not in list(range(index1, pos))]
        for i, j in zip(conflict1_ids, conflict2_ids):
            temp_parent1[i], temp_parent2[j] = temp_parent2[j], temp_parent1[i]

        # 修正路線使之在規定時間內
        temp_parent1 = fix_path(dis_array, temp_parent1)
        temp_parent2 = fix_path(dis_array, temp_parent2)

        x_score = Evaluation(benefit, temp_parent1)
        y_score = Evaluation(benefit, temp_parent2)
        # 擇優加入
        if x_score > y_score and (not temp_parent1 in path):
            path.append(temp_parent1)
        elif x_score <= y_score and (not temp_parent1 in path):
            path.append(temp_parent2)
        elif x_score > y_score:
            path.append(temp_parent1)
        else:
            path.append(temp_parent2)

        # 消除 dummy
        while -1 in path[parent1]:
            for i, v in enumerate(path[parent1]):
                if v == dummy:
                    del path[parent1][i]

        while -1 in path[parent2]:
            for i, v in enumerate(path[parent2]):
                if v == dummy:
                    del path[parent2][i]

    return path


# TODO 突變
def mutation(path):
    n = len(path)
    for i in range(n):
        index1 = np.random.randint(0, len(path[i]))
        index2 = np.random.randint(0, len(path[i]))
        if index1 == index2:
            continue
        cur_pro = np.random.random()  # ? 決定是否要突變
        # 不突變
        if cur_pro > mutation_pro:
            continue
        else:
            path[i][index1], path[i][index2] = path[i][index2], path[i][index1]

        path[i] = fix_path(dis_array, path[i])
    return path


#! 染色體反轉
def reverse(path):
    n = len(path)
    for i in range(n):
        flag = 0
        while flag == 0:
            index1 = np.random.randint(1, len(path[i])+1)
            index2 = np.random.randint(index1, len(path[i])+1)
            if index1 == index2:
                continue
            temp_chrom = np.copy(path[i])
            temp_chrom = temp_chrom.tolist()
            temp_gen = temp_chrom[index1:index2]
            temp_gen.reverse()
            temp_chrom[index1:index2] = temp_gen
            fit_score1 = Evaluation(benefit, path[i])
            fit_score2 = Evaluation(benefit, temp_chrom)
            # 如果反轉後的染色體比原本的還好
            if fit_score2 > fit_score1:
                path[i] = temp_chrom  # ? 更新染色體為反轉後的染色體
            flag = 1
    return path


if __name__ == '__main__':
    population_num = len(coords)
    max_evolution_num = 100
    choice_pro = 0.2
    mutation_pro = 0.05
    best_step_index = 0
    max_score = 0
    dummy = -1
    dis_array = compute_dis_mat(population_num, coords)
    path = init_greedy(dis_array, population_num, benefit)


#!----------------------演算法程序-----------------------
    for step in range(max_evolution_num):
        path = choice(path)
        path = cross(path)
        path = mutation(path)
        path = reverse(path)

        Score = []
        [Score.append(Evaluation(benefit, path[i])) for i in range(len(path))]

        best_path_idx = np.argmax(Score)  # ? 找到最好染色體位置

        if Score[best_path_idx] > max_score:
            max_score = Score[best_path_idx]  # ? 更新最高獲益值
            best_path = path[best_path_idx]  # ? 更新最佳染色體
            if best_step_index <= step:
                best_step_index = step + 1

        print('第{}代：{}分'.format(step + 1, max_score))

    print('{:=^100s}'.format('這是分隔線'))
    print('最佳分數為：{}分'.format(max_score))
    print('最佳路徑出現在第{}代，共拜訪了{}個點，其路徑為：\n{}'.format(
        best_step_index, len(best_path), best_path))

    print('Wryyyyyyyy')
