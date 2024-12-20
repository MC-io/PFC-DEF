import numpy as np

def get_reference_point(pareto_front):
    worst_f1 = 0
    for sol in pareto_front:
        if sol.objectives[0] > worst_f1:
            worst_f1 = sol.objectives[0]
    worst_f2 = 0
    for sol in pareto_front:
        if sol.objectives[1] > worst_f2:
            worst_f2 = sol.objectives[1]
    return [worst_f1 * 1.2, worst_f2 * 1.2]


def calculate_hypervolume(pareto_front_list):

    reference_point = get_reference_point(pareto_front_list)

    func = [i.objectives for i in pareto_front_list]

    pareto_front = [[i[0], i[1]] for i in func]
    
    pareto_front = np.array(pareto_front)
    reference_point = np.array(reference_point)

    if pareto_front.shape[1] != len(reference_point):
        raise ValueError("The dimensions of the Pareto front and reference point do not match.")

    pareto_front = pareto_front[np.argsort(-pareto_front[:, 0])]

    hypervolume = 0.0
    previous_point = reference_point.copy()

    for point in pareto_front:
        volume = np.prod(previous_point - point)
        hypervolume += volume

        previous_point = point

    return hypervolume