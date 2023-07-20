from tempGame import New_Obstacle

# 跳起（深蹲）：3秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
# 攻擊（後跨步蹲抬手）：3秒（重複三次）
# 休息三秒換下一個組合
def Set1(time, all_sprites, obstacles):
    if time == 60 or time == 57 or time == 54 or time == 30 or time == 27 or time == 24:
        New_Obstacle(all_sprites, obstacles, 1)
    elif time == 51 or time == 48 or time == 45 or time == 21 or time == 18 or time == 15:
        New_Obstacle(all_sprites, obstacles, 3)
    elif time == 42 or time == 39 or time == 36 or time == 12 or time == 9 or time == 6:
        New_Obstacle(all_sprites, obstacles, 2)


# 攻擊（後跨步蹲抬手）：3秒（重複五次）
# 趴下（左右跨步蹲）：2秒（重複三次）
# 跳起（深蹲）：3秒（重複三次）
def Set2(time, all_sprites, obstacles):
    if time == 60 or time == 57 or time == 54 or time == 51 or time == 48 or \
        time == 30 or time == 27 or time == 24 or time == 21 or time == 18:
        New_Obstacle(all_sprites, obstacles, 2)
    elif time == 45 or time == 43 or time == 41 or time == 15 or time == 13 or time == 11:
        New_Obstacle(all_sprites, obstacles, 3)
    elif time == 39 or time == 36 or time == 33 or time == 9 or time == 6 or time == 3:
        New_Obstacle(all_sprites, obstacles, 1)


# 跳起（深蹲）：3秒（重複五次）
# 攻擊（後跨步蹲抬手）：2秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
def Set3(time, all_sprites, obstacles):
    if time == 60 or time == 57 or time == 54 or time == 51 or time == 48 or \
        time == 30 or time == 27 or time == 24 or time == 21 or time == 18:
        New_Obstacle(all_sprites, obstacles, 1)
    elif time == 45 or time == 43 or time == 41 or time == 15 or time == 13 or time == 11:
        New_Obstacle(all_sprites, obstacles, 2)
    elif time == 39 or time == 36 or time == 33 or time == 9 or time == 6 or time == 3:
        New_Obstacle(all_sprites, obstacles, 3)


# 攻擊（後跨步蹲抬手）：2秒（重複三次）
# 趴下（左右跨步蹲）：2秒（重複三次）
# 跳起（深蹲）：3秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
def Set4(time, all_sprites, obstacles):
    if time == 60 or time == 58 or time == 56 or time == 30 or time == 28 or time == 26:
        New_Obstacle(all_sprites, obstacles, 2)
    elif time == 54 or time == 52 or time == 50 or time == 24 or time == 22 or time == 20:
        New_Obstacle(all_sprites, obstacles, 3)
    elif time == 48 or time == 45 or time == 42 or time == 18 or time == 15 or time == 12:
        New_Obstacle(all_sprites, obstacles, 1)
    elif time == 39 or time == 36 or time == 33 or time == 9 or time == 6 or time == 3:
        New_Obstacle(all_sprites, obstacles, 3)


# 趴下（左右跨步蹲）：2秒（重複三次）
# 跳起（深蹲）：2秒（重複五次）
# 攻擊（後跨步蹲抬手）：2秒（重複五次）
# 跳起（深蹲）：2秒（重複兩次）
def Set5(time, all_sprites, obstacles):
    if time == 60 or time == 58 or time == 56 or time == 30 or time == 28 or time == 26:
        New_Obstacle(all_sprites, obstacles, 3)
    elif time == 54 or time == 52 or time == 50 or time == 48 or time == 46 or \
        time == 24 or time == 22 or time == 20 or time == 18 or time == 16:
        New_Obstacle(all_sprites, obstacles, 1)
    elif time == 44 or time == 42 or time == 40 or time == 38 or time == 36 or \
        time == 14 or time == 12 or time == 10 or time == 8 or time == 6:
        New_Obstacle(all_sprites, obstacles, 2)
    elif time == 34 or time == 32 or time == 4 or time == 2:
        New_Obstacle(all_sprites, obstacles, 1)
    
    