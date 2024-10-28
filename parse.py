def read_grid_mdp_problem_p1(file_path):
    #Your p1 code here
    problem = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    problem['seed'] = lines[0].strip().split(' ')[1]
    problem['noise'] = lines[1].strip().split(' ')[1]
    problem['livingReward'] = lines[2].strip().split(' ')[1]
    problem['grid'] = []
    problem['policy'] = []
    problem['origin_grid'] = []
    i = 0
    for i in range(4,len(lines)):
        if 'policy' in lines[i]:
            break
        problem['origin_grid'].append(lines[i])
        temp = [word for word in lines[i].strip().split(' ') if word.strip()]
        if 'S' in temp:
            for pos in range(len(temp)):
                if temp[pos] == 'S':
                    problem['start'] = [i-4,pos]
                    break
        problem['grid'].append(temp)
    for k in range(i+1, len(lines)):
        if 'policy' in lines[k]:
            continue
        problem['policy'].append([word for word in lines[k].strip().split(' ') if word.strip()])
    return problem

def read_grid_mdp_problem_p2(file_path):
    #Your p2 code here
    problem = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    problem['discount'] = lines[0].strip().split(' ')[1]
    problem['noise'] = lines[1].strip().split(' ')[1]
    problem['livingReward'] = lines[2].strip().split(' ')[1]
    problem['iterations'] = lines[3].strip().split(' ')[1]
    problem['grid'] = []
    problem['policy'] = []
    problem['origin_grid'] = []
    i = 0
    for i in range(5,len(lines)):
        if 'policy' in lines[i]:
            break
        problem['origin_grid'].append(lines[i])
        temp = [word for word in lines[i].strip().split(' ') if word.strip()]
        if 'S' in temp:
            for pos in range(len(temp)):
                if temp[pos] == 'S':
                    problem['start'] = [i-5,pos]
                    break
        problem['grid'].append(temp)
    for k in range(i+1, len(lines)):
        if 'policy' in lines[k]:
            continue
        problem['policy'].append([word for word in lines[k].strip().split(' ') if word.strip()])
    return problem

def read_grid_mdp_problem_p3(file_path):
    #Your p3 code here
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