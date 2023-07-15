# -*- coding: utf-8 -*-
import random

# 模拟次数
num_simulations = 100000

# 统计计数(选择变换)
switch_count = 0

# 所有房间
total_room = [1, 2, 3]

# 房间奖品设置, 以下设置为 3号房间有奖
prize_room = 3
no_prize_room = [1, 2]

for i in range(num_simulations):

    # 候选列表
    room_candidate = no_prize_room[:]

    # 随机从所有门选择
    selected_door = random.choice(total_room)

    # 选择到无奖品房间
    if selected_door in no_prize_room:
        # 随机从一个未选择的无奖品房间 关闭一个
        room_candidate.remove(selected_door)
        close_room = random.choice(room_candidate)
        room_candidate.remove(close_room)

        # 将有奖品房间加入候选列表
        room_candidate.append(prize_room)

        # 从候选列表重新选择一个
        selected_door = random.choice(room_candidate)
    # 选择到有奖品房间
    else:
        # 随机从一个未选择的无奖品房间 关闭一个
        close_room = random.choice(room_candidate)
        room_candidate.remove(close_room)
        # 从候选列表重新选择一个
        selected_door = random.choice(room_candidate)


    # 如果最终选择到有奖品房间, 中奖计数+1
    if selected_door == prize_room:
        switch_count += 1

print("switch win count:", switch_count)
