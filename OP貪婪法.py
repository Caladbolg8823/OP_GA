import numpy as np
import pandas as pd
from numpy import inf

fileName = 'OP/tsiligirides_problem_1_budget_85.txt'
get_data = pd.read_csv(fileName, header=None, delim_whitespace=True)

# TODO 指定最大時間或距離
max_time = get_data.iloc[-1].values
max_time = int(max_time[0])
use_time = max_time

# TODO 創建距離矩陣
dist = []
for i in range(len(get_data)-1):
    a = get_data.iloc[i+1]
    a = np.array(a)
    a = np.delete(a, 2)
    for j in range(len(get_data)-1):
        if i != j:
            b = get_data.iloc[j+1]
            b = np.array(b)
            b = np.delete(b, 2)
            dist.append(int(np.linalg.norm(a-b)))
        elif i == j:
            dist.append(99999)


distance = np.array(dist)
distance = distance.reshape(len(get_data)-1, len(get_data)-1)

# TODO 取得每點的獲益值
benefit = []
for i in range(len(get_data)-2):
    c = get_data.iloc[i]
    c = [int(i) for i in c]
    del c[0]
    del c[0]
    c = c[0]
    benefit.append(c)
print('各點獲益值：{}'.format(benefit))


# TODO 尋找下一節點
def Next_node(actual_position, distance, benefit):
    profits = []
    for i in range(len(benefit)):
        a = benefit[i]
        b = distance[actual_position][i]
        cc = a/b
        profits.append(cc)

        # profits.append(benefit[i]/distance[actual_position][i])
    profits = np.asarray(profits)
    profits[np.isnan(profits)] = 0
    profits[profits == inf] = 0
    next_node = np.argmax(profits)
    return(next_node)


Score = 0
init_position = 0
visit_nodes = []
visit_nodes.append(init_position)
actual_position = init_position


# TODO 迭代至時間用完
while max_time > 0:
    for i in range(len(visit_nodes)):
        distance[actual_position][visit_nodes[i]] = 999999
    next_node = Next_node(actual_position, distance, benefit)
    Score += benefit[next_node]
    if max_time-distance[actual_position][next_node] < 0:
        break
    max_time -= distance[actual_position][next_node]
    benefit[next_node] = 0  # ? 選過的獲益值設為0
    visit_nodes.append(next_node)  # ? 加入路線內
    actual_position = next_node
print('路線：{}'.format(visit_nodes))
print('花費總時間：{}'.format(use_time - max_time))
print('總獲益值：{}'.format(Score))
