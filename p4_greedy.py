import random, math, copy
from p2 import judge

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
    problem['discount'] = float(lines[0].strip().split(' ')[1])
    problem['noise'] = float(lines[1].strip().split(' ')[1])
    problem['livingReward'] = float(lines[2].strip().split(' ')[1])
    problem['iterations'] = lines[3].strip().split(' ')[1]
    problem['grid'] = []
    for i in range(5,len(lines)):
        if 'policy' in lines[i]:
            break
        temp = [word for word in lines[i].strip().split(' ') if word.strip()]
        if 'S' in temp:
            for pos in range(len(temp)):
                if temp[pos] == 'S':
                    problem['start'] = [i-5,pos]
                    break
        problem['grid'].append(temp)
    return problem
def exploitation(start_pos, epsilon, alpha, q_value, policy, problem,flag, change_times):
    i = start_pos[0]
    j = start_pos[1]
    noise = float(problem['noise'])
    if not flag:
        return
    if problem['grid'][i][j] != 'S' and problem['grid'][i][j] != '_' and problem['grid'][i][j] != '#':
        policy[i][j] = 'x'
        grade = float(problem['grid'][i][j])
        for d in range(4):
            q_value[i][j][d] =grade
        flag = False
        return
    else:
        num_d_mapping = ['N', 'E', 'S', 'W']
        d_num_mapping = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        d_change = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
        dd = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
        m = len(q_value)
        n = len(q_value[0])
        prob_actions = ['R', 'P'] #'R' for random choices, 'P' for policy
        true_action = random.choices(prob_actions, weights=[1-epsilon, epsilon])[0]
        if true_action == 'R':
            direction = num_d_mapping[random.randint(0, 3)]
        else:
            direction = policy[start_pos[0]][start_pos[1]]
        true_direction = random.choices(dd[direction],weights=[1-2*noise, noise, noise])[0]
        next_pos = [start_pos[0] + d_change[true_direction][0], start_pos[1] + d_change[true_direction][1]]
        if judge(next_pos, problem['grid']):
            sample = problem['livingReward'] + problem['discount'] * max(q_value[next_pos[0]][next_pos[1]])
        else:
            next_pos = start_pos
            sample = problem['livingReward'] + problem['discount'] * max(q_value[start_pos[0]][start_pos[1]])
        differ = sample - q_value[start_pos[0]][start_pos[1]][d_num_mapping[direction]]
        q_value[start_pos[0]][start_pos[1]][d_num_mapping[direction]] += alpha * differ
        max_q = max(q_value[start_pos[0]][start_pos[1]])
        before_policy = policy[start_pos[0]][start_pos[1]]
        max_index = []
        for x in range(4):
            if q_value[start_pos[0]][start_pos[1]][x] == max_q:
                max_index.append(x)
        policy[start_pos[0]][start_pos[1]] = num_d_mapping[random.choice(max_index)]
        if before_policy != policy[start_pos[0]][start_pos[1]]:
            change_times[0] += 1
        # print(f"i,j{i,j}, next_pos{next_pos},sample{sample},differ{differ},policy:{policy[i][j]},true_action:{true_action},direction:{direction},max_index{max_index}")
        # input()
        exploitation(next_pos, epsilon, alpha, q_value, policy, problem,flag, change_times)
        if not flag:
            return
def main():
    d_num_mapping = {'N': 0, 'E': 1, 'S': 2, 'W': 3}  # define the first pos:N, second:E, third: S, forth: W
    file_path = "/Users/lee/work/HKU/7404/HKUassignment/7404/a3/test_cases/p3/2.prob"
    problem = read_grid_mdp_problem_p4(file_path)
    grid = problem['grid']
    m = len(grid)
    n = len(grid[0])
    Q_value = [[[0.0 for _ in range(4)] for __ in range(n)] for ___ in range(m)]
    policy = [['N' for _ in range(n)] for __ in range(m)]
    for _ in range(len(grid)):
        for __ in range(len(grid[_])):
            if grid[_][__] == 'S':
                start_pos = [_, __]
            if grid[_][__] == '#':
                policy[_][__] = '#'
    epsilon = 1
    alpha = 1
    search_times = 0
    flag = True
    change_times = [0]
    no_change_times = 0
    while True:
        change_times[0] = 0
        exploitation(start_pos, epsilon, alpha, Q_value, policy, problem,flag,change_times)
        search_times += 1
        if search_times %80== 0:
            alpha = max(0, alpha -0.001)
            epsilon = max(0, epsilon-0.0008)
        if alpha == 0:
            break
        if change_times[0] == 0:
            no_change_times += 1
        else:
            no_change_times = 0
        if no_change_times >= 70:
            break
        # print(f"search_times:{search_times},no_change_times:{no_change_times}")
        # input()
    print(f"epsilon:{epsilon},alpha:{alpha},no_change_times:{no_change_times}")
    for i in Q_value:
        print(i)
    for i in policy:
        print(i)
if __name__ == '__main__':
    main()