# -*- coding: utf-8 -*-
import random

num_simulations = 100000

switch_count = 0
stay_count = 0

# prize is in door 3
for i in range(num_simulations):
    # random choose from  door 1,2,3
    selected_door = random.randint(1, 3)
    if selected_door == 1:
        # close door 2, we switch to door 3
        selected_door = 3
    elif selected_door == 2:
        # close door 1, we switch to door 3
        selected_door = 3
    else:
        # close door 1 or 2, we switch to door 2 or 1
        selected_door = random.randint(1, 2)

    if selected_door == 3:
        # door 3 has prize
        switch_count += 1
    else:
        stay_count += 1

print("switch win count:", switch_count)
print("stay win count", stay_count)
