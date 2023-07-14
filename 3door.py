# -*- coding: utf-8 -*-
import random

# 模拟次数
num_simulations = 100000

# 统计计数(选择变换)
switch_count = 0

# 房间奖品设置, 以下设置为 3号房间有奖
prize_room = 3
no_prize_room = [1, 2]


for i in range(num_simulations):
    # 随机从 1~3 选择
    selected_door = random.randint(1, 3)

    # 选择到无奖品房间, 由于另一个无奖品房间会被关闭，选择变换可以到有奖房间
    if selected_door == no_prize_room[0]:
        selected_door = prize_room
    # 选择到另一个无奖品房间, 由于另一个无奖品房间会被关闭，选择变换可以到有奖房间
    elif selected_door == no_prize_room[1]:
        selected_door = prize_room
    # 选择到有奖品房间, 一个随机的无奖品房间会被关闭，我们选择另一个
    elif selected_door == prize_room:
        selected_door = random.choice(no_prize_room)

    # 如果最终选择到有奖品房间, 中奖计数+1
    if selected_door == prize_room:
        switch_count += 1

print("switch win count:", switch_count)
