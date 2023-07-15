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

#
# 如果有可能打开已经被选择的无奖房间，则可将  step A1 和 A3 下面的那一行用 # 注释掉即可
#

for i in range(num_simulations):

    # 每次将候选列表初始化为 所有无奖房间
    room_candidate = no_prize_room[:]

    # 随机从所有门选择
    selected_door = random.choice(total_room)

    if selected_door in no_prize_room:
        # 第一次就选择到无奖品房间

        # step A1  先将刚刚已经选择的房间临时排除掉 (为了从"未选择"的无奖房间中选择)
        room_candidate.remove(selected_door)
        # open_room 为要打开的无奖房间
        open_room = random.choice(room_candidate)
        # step A2  将这个房间从可选择列表 移除
        if open_room in room_candidate:
            room_candidate.remove(open_room)

        # step A3  将 step 1 中临时移除的已选择房间加回来
        room_candidate.append(selected_door)

        # step A4  将有奖品房间加入候选列表
        room_candidate.append(prize_room)

        # step A5 由于这里是统计无脑"换"，因此再将选择的房间排除掉 (如果它在)
        if selected_door in room_candidate:
            room_candidate.remove(selected_door)

        # step A6 从候选列表重新选择一个
        selected_door = random.choice(room_candidate)
    else:
        # 第一次就选择到有奖品房间
        # step B1 随机从一个未选择的无奖品房间 打开一个
        open_room = random.choice(room_candidate)
        if open_room in room_candidate:
            room_candidate.remove(open_room)

        # step B2 执行无脑"换"，从其他剩余候选列表重新选择一个 (其实这里肯定不会选择到有奖房间了....)
        selected_door = random.choice(room_candidate)


    # 如果最终选择到有奖品房间, 无脑"换" 的中奖次数+1
    if selected_door == prize_room:
        switch_count += 1

print("switch win count:", switch_count)
