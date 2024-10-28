import sys, grader, parse, copy
def judge(temp_new, origin_grid):
    ans = False
    if temp_new[0] >= 0 and temp_new[0] < len(origin_grid):
        if temp_new[1] >=0 and temp_new[1] < len(origin_grid[0]):
            if origin_grid[temp_new[0]][temp_new[1]] != '#':
                ans = True
    return ans
def getnum(grid2, pos, action, noise, discount, livingreward, origin_grid):
    d = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
    d_change = {'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}
    res = 0.0
    prob_d = d[action]
    for i in prob_d:
        temp_new = [pos[0] + d_change[i][0], pos[1] + d_change[i][1]]
        if judge(temp_new, origin_grid):
            if i == action:
                res += (1-2*noise)*(livingreward + discount*grid2[temp_new[0]][temp_new[1]])
            else:
                res += noise*(livingreward + discount*grid2[temp_new[0]][temp_new[1]])
        else:
            if i == action:
                res += (1-2*noise)*(livingreward + discount*grid2[pos[0]][pos[1]])
            else:
                res += noise*(livingreward + discount*grid2[pos[0]][pos[1]])
    return res
def change(grid1, grid2, policy, k, grid, discount, noise, livingreward, origin_grid):
    if k == 1:
        for i in range(len(policy)):
            for j in range(len(policy[i])):
                if policy[i][j] == 'exit':
                    grid1[i][j] = float(grid[i][j])
                elif policy[i][j] == '#':
                    grid1[i][j] = '##### '
                else:
                    grid1[i][j] = livingreward

    else:
        for i in range(len(grid1)):
            for j in range(len(grid1[i])):
                if grid[i][j] == '#':
                    grid1[i][j] = '##### '
                    continue
                action = policy[i][j]
                if action == 'exit':
                    grid1[i][j] = grid2[i][j]
                else:
                    grid1[i][j] = getnum(grid2,[i,j], action, noise, discount, livingreward, origin_grid)

def policy_evaluation(problem):
    discount = float(problem['discount'])
    noise = float(problem['noise'])
    livingreward = float(problem['livingReward'])
    k = int(problem['iterations'])
    grid = problem['grid']
    policy = problem['policy']
    return_value = ''
    grid_1 = [[0.00 for _ in range(len(grid[0]))] for __ in range(len(grid))]
    for _ in range(len(grid)):
        for __ in range(len(grid[0])):
            if grid[_][__] == '#':
                grid_1[_][__] = '##### '
    grid_2 = [[0.00 for _ in range(len(grid[0]))] for __ in range(len(grid))]
    for i in range(k):
        if i == 0:
            return_value += f"V^pi_k={i}"
            for line in grid_1:
                return_value += f"\n"
                for element in line:
                    if type(element) == str:
                        return_value += '|' + "".join(f"{element:>7}") + '|'
                    else:
                        return_value += '|' + "".join(f"{0:>7.2f}") + '|'
        else:
            return_value += f"\nV^pi_k={i}"
            change(grid_1, grid_2, policy, i, grid, discount, noise, livingreward, grid)
            for line in grid_1:
                return_value += f"\n"
                for element in line:
                    if type(element) == str:
                        return_value += '|' + "".join(f"{element:>7}") + '|'
                    else:
                        return_value += '|' + "".join(f"{element:>7.2f}") + '|'
        grid_2 = copy.deepcopy(grid_1)
    return return_value

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)