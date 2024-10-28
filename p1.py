import sys, grader, parse, random
def judge(newpos, grid_size, grid):
    if newpos[0] >= 0 and newpos[0] < grid_size[0]:
        if newpos[1] >=0 and newpos[1] < grid_size[1]:
            if grid[newpos[0]][newpos[1]] !='#':
                return True
    return False
def play_episode(problem):
    seed = int(problem['seed'])
    grid = problem['grid']
    livingreward = float(problem['livingReward'])
    policy = problem['policy']
    origin_grid = problem['origin_grid']
    noise = float(problem['noise'])
    if seed != -1:
        random.seed(seed, version = 1)
    d = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
    # print(random.choices(population=d['N'], weights=[0.8, 0.1, 0.1]))
    d_change = {'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}
    grid_size = (len(grid), len(grid[0]))
    P_pos = problem['start']
    grid[P_pos[0]][P_pos[1]] = 'P'
    reward_sum = 0.0
    experience = ''
    experience +='Start state:\n' 
    for i in grid:
        line = "".join(f"{num:>5}" for num in i)
        experience += line + '\n'
    experience += f"Cumulative reward sum: 0.0"
    last_word = 'S'
    while True:
        intended_action = policy[P_pos[0]][P_pos[1]]
        if intended_action == 'exit':
            reward_sum += float(last_word)
            experience +='\n-------------------------------------------- \n'
            experience += f'Taking action: exit (intended: exit)\nReward received: {round(float(last_word),2)}\n'
            experience += 'New state:\n'
            for i in origin_grid:
                experience += i
            experience += f'Cumulative reward sum: {round(reward_sum,2)}' 
            break
        true_action = random.choices(population= d[intended_action], weights= [1-2*noise, noise, noise])[0]
        new_pos = [P_pos[0] + d_change[true_action][0], P_pos[1] + d_change[true_action][1]]
        temp_experience = ""
        if judge(new_pos, grid_size, grid):
            grid[P_pos[0]][P_pos[1]] = last_word
            last_word = grid[new_pos[0]][new_pos[1]]
            grid[new_pos[0]][new_pos[1]] = 'P'
            P_pos[0] = new_pos[0]
            P_pos[1] = new_pos[1]
        
        temp_experience += '\n-------------------------------------------- \n'
        temp_experience += f"Taking action: {true_action} (intended: {intended_action})\n"
        temp_experience += f'Reward received: {livingreward}\n'
        temp_experience += 'New state:\n'
        for i in grid:
            line = "".join(f"{num:>5}" for num in i)
            temp_experience += line + '\n'
        reward_sum += livingreward
        temp_experience += f"Cumulative reward sum: {round(reward_sum,2)}"
        experience += temp_experience
    return experience

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)