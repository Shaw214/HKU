import sys, grader, parse, copy
from p2 import judge, getnum
def change(grid1, grid2, policy, k, grid, discount, noise, livingreward, origin_grid):
    if k == 1:
        for i in range(len(policy)):
            for j in range(len(policy[i])):
                if policy[i][j] == 'x':
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
                if action == 'x':
                    grid1[i][j] = grid2[i][j]
                else:
                    grid1[i][j] = getnum(grid2,[i,j], action, noise, discount, livingreward, origin_grid)
                    
def update_pi(policy, grid1,grid2, noise, discount, livingreward, origin_grid):
    directions = ('N', 'E', 'S', 'W')
    for i in range(len(policy)):
        for j in range(len(policy[i])):
            if policy[i][j] == 'x' or policy[i][j] == '#':
                continue
            max_dir = [-float('inf'), policy[i][j]]
            for each_ori in directions:
                grade = getnum(grid2, [i,j], each_ori,noise, discount, livingreward, origin_grid)
                if grade > max_dir[0]:
                    max_dir = [grade, each_ori]
                
            policy[i][j] = max_dir[1]
def value_iteration(problem):
    return_value = ''
    discount = float(problem['discount'])
    noise = float(problem['noise'])
    livingreward = float(problem['livingReward'])
    k = int(problem['iterations'])
    grid = problem['grid']
    policy = []
    for i in range(len(grid)):
        temp = []
        for j in range(len(grid[i])):
            if grid[i][j] == '_' or grid[i][j] == 'S':
                temp.append('N')
            elif grid[i][j] == '#':
                temp.append('#')
            else:
                temp.append('x')
        policy.append(temp)
    grid_1 = [[0.00 for _ in range(len(grid[0]))] for __ in range(len(grid))]
    for _ in range(len(grid)):
        for __ in range(len(grid[0])):
            if grid[_][__] == '#':
                grid_1[_][__] = '##### '
    grid_2 = [[0.00 for _ in range(len(grid[0]))] for __ in range(len(grid))]
    for i in range(k):
        if i == 0:
            return_value += f"V_k={i}"
            for line in grid_1:
                return_value += f"\n"
                for element in line:
                    if type(element) == str:
                        return_value += '|' + "".join(f"{element:>7}") + '|'
                    else:
                        return_value += '|' + "".join(f"{0:>7.2f}") + '|'
        else:
            return_value += f"\nV_k={i}"
            change(grid_1, grid_2, policy, i, grid, discount, noise, livingreward, grid)
            grid_2 = copy.deepcopy(grid_1)
            for line in grid_1:
                return_value += f"\n"
                for element in line:
                    if type(element) == str:
                        return_value += '|' + "".join(f"{element:>7}") + '|'
                    else:
                        return_value += '|' + "".join(f"{element:>7.2f}") + '|'
            return_value += f"\npi_k={i}"
            for line in policy:
                return_value += '\n'
                for element in line:
                    return_value += '|' + "".join(f"{element:^3}") + '|'
            update_pi(policy, grid_1, grid_2, noise, discount, livingreward, grid)
        
    return return_value

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)