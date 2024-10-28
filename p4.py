import random, math, copy
from p2 import judge
import sys
sys.setrecursionlimit(10000)  # 增加最大递归深度

def get_sorted_index(num):
    ans = []
    for i in range(len(num)):
        max_num = -float('inf')
        max_num_index = -1
        for j in range(len(num)):
            if max_num < num[j] and j not in ans:
                max_num = num[j]
                max_num_index = j
        ans.append(max_num_index)
    return ans
def read_grid_mdp_problem_p4(file_path):
    problem = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    problem['discount'] = lines[0].strip().split(' ')[1]
    problem['noise'] = lines[1].strip().split(' ')[1]
    problem['livingReward'] = lines[2].strip().split(' ')[1]
    problem['iterations'] = lines[3].strip().split(' ')[1]
    problem['grid'] = []
    for i in range(5,len(lines)):
        if 'policy' in lines[i]:
            break
        temp = [word for word in lines[i].strip().split(' ') if word.strip()]
        if 'S' in temp:
            for pos in range(len(temp)):
                if temp[pos] == 'S':
                    problem['start'] = [i-4,pos]
                    break
        problem['grid'].append(temp)
    return problem

def exploration(start_pos, Q1_value, Q2_value, policy, point_explored_times, problem, num_changes, explored_area, alpha, bonus, flag, last_pos):
    
    if flag == False:
        return
    
    d_num_mapping = {'N':0, 'E':1, 'S':2, 'W':3}
    num_d_mapping = ['N', 'E', 'S', 'W']
    dd = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
    d_change = {'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}
    i = start_pos[0]
    j = start_pos[1]
    point_explored_times[i][j] += 1
    discount = float(problem['discount'])
    livingreward = float(problem['livingReward'])
    noise = float(problem['noise'])
    grid = problem['grid']
    if problem['grid'][i][j] != 'S' and problem['grid'][i][j] != '_' and problem['grid'][i][j] != '#':
        if policy[i][j] !='x':
            num_changes[0] += 1
        policy[i][j] = 'x'
        grade = float(problem['grid'][i][j])
        for d in range(4):
            Q1_value[i][j][d] += alpha*(grade - Q2_value[i][j][d])
        flag = False
        return
    else:
        samples = []
        for d in range(4):
            action = num_d_mapping[d]
            temp_new = [i + d_change[action][0], j + d_change[action][1]]
            if judge(temp_new, problem['grid']):
                sample = (livingreward + discount*(max(Q2_value[temp_new[0]][temp_new[1]]) + bonus/ point_explored_times[temp_new[0]][temp_new[1]]))
                samples.append(sample)
                # print(f"temp_new:{temp_new}, searching, i,j,d:{i,j,d}, Q1_value:{Q1_value[i][j][d]},f:{bonus/point_explored_times[temp_new[0]][temp_new[1]]}, bonus:{bonus},explored_times{point_explored_times[temp_new[0]][temp_new[1]]}")
            else:
                samples.append(livingreward + discount*(max(Q2_value[i][j]) + bonus/ point_explored_times[i][j]))
                
        # Q2_value = copy.deepcopy(Q1_value)
        max_q = max(samples)
        best_dir_index = d_num_mapping[policy[i][j]]
        if best_dir_index != samples.index(max_q):
            num_changes[0] += 1
        direction = num_d_mapping[samples.index(max_q)]
        prob_dir = dd[direction]
        true_dir = random.choices(population=prob_dir, weights=[1-2*noise,noise,noise])[0]
        # print(f"samples:{i,j, samples},dir:{direction},ture_dir:{true_dir}")
        new_pos = [start_pos[0] + d_change[true_dir][0],start_pos[1] + d_change[true_dir][1]]
        if not judge(new_pos, grid):
            new_pos = start_pos
        # if new_pos not in explored_area:
        explored_area.append(new_pos)
        changed_dir_index = d_num_mapping[direction]
        # true_sample = samples[changed_dir_index]
        Q1_value[i][j][changed_dir_index] += alpha*(livingreward + discount*(max(Q2_value[new_pos[0]][new_pos[1]])) - Q2_value[i][j][changed_dir_index])
        Q2_value = copy.deepcopy(Q1_value)
        policy[i][j] = num_d_mapping[Q1_value[i][j].index(max(Q1_value[i][j]))]
        exploration(new_pos, Q1_value, Q2_value, policy, point_explored_times, problem, num_changes, explored_area, alpha, bonus, flag, start_pos)

def main():
    alpha = 1#learning rate
    no_change_times = 20 #hyperparameter about no change times
    k = 2#hyperparameter: over explored_times

    d_num_mapping = {'N':0, 'E':1, 'S':2, 'W':3}#define the first pos:N, second:E, third: S, forth: W
    file_path = "/Users/lee/work/HKU/7404/HKUassignment/7404/a3/test_cases/p3/2.prob"
    problem = read_grid_mdp_problem_p4(file_path)
    grid = problem['grid']
    m = len(grid)
    n = len(grid[0])
    Q1_value = [[[0.0 for _ in range(4)] for __ in range(n)] for ___ in range(m)]
    
    point_explored_times = [[1 for _ in range(n)] for __ in range(m)]
    policy = [['N' for _ in range(n)] for __ in range(m)]
    
    start = []
    for _ in range(len(grid)):
        for __ in range(len(grid[_])):
            if grid[_][__] == 'S':
                start = [_, __]
            if grid[_][__] == '#':
                policy[_][__] = '#'
    exploration_times = 0
    point_nums = m*n
    times = 0
    while True:
        Q2_value = copy.deepcopy(Q1_value)
        if alpha == 0:
            break
        explored_area = []
        start_pos = start
        num_changes = [0]
        explored_area.append(start_pos)
        flag = True #True represent the agent is still alive

        # test
        # for i in Q1_value:
        #     print(i)
        # for i in point_explored_times:
        #     print(i)
        # input()

        exploration(start_pos, Q1_value, Q2_value, policy, point_explored_times, problem, num_changes, explored_area, alpha, k, flag,[-1,-1])
        # alpha = max(0, alpha - math.e**(-(num_changes[0]+point_nums)))
        exploration_times += 1
        if exploration_times%50 == 0:
            alpha = max(0, alpha - 0.001)
        for i in range(len(Q1_value)):
            for j in range(len(Q1_value[i])):
                for kk in range(len(Q1_value[i][j])):
                    Q1_value[i][j][kk] = round(Q1_value[i][j][kk],2)
        if num_changes[0] == 0:
            if times > no_change_times:
                break
            times += 1
        else:
            times = 0
        
    print(f"alpha:{alpha}, no_changes times:{times}")
    for i in Q1_value:
        print(i)
    for i in policy:
        print(i)
    
if __name__ =='__main__':
    main()