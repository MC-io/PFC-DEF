import random

def get_redistribution_plan(lists, m):
    if not lists or m <= 0:
        return {"from": [], "to": []}

    redistribution_plan = {"from": [], "to": []}
    total_lists = len(lists)

    for i, lst in enumerate(lists):
        if len(lst) > 0:
            selected_indices = random.sample(range(len(lst)), min(m, len(lst)))
            redistribution_plan["from"].append({
                "list_index": i,
                "element_indices": selected_indices
            })

            for idx in selected_indices:
                element = lst[idx]

                target_list_index = random.choice([x for x in range(total_lists) if x != i])


                redistribution_plan["to"].append({
                    "source_list": i,
                    "target_list": target_list_index,
                    "source_element_index": idx,
                })

    return redistribution_plan

# Example lists
lists = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9],
    [10, 11, 12],
    [13, 14, 15, 16, 16],
    [18, 19, 20,]
]

# Get redistribution plan for 2 elements from each list
plan = get_redistribution_plan(lists, 2)

# Print the redistribution plan
print("Redistribution Plan:")
print(plan)
