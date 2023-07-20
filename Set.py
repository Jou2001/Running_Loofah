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
    if time == 60 or time == 57 or time == 54 or time == 30 or time == 27 or time == 24:
        New_Obstacle(all_sprites, obstacles, 1)
    elif time == 51 or time == 48 or time == 45 or time == 21 or time == 18 or time == 15:
        New_Obstacle(all_sprites, obstacles, 2)
    elif time == 42 or time == 39 or time == 36 or time == 12 or time == 9 or time == 6:
        New_Obstacle(all_sprites, obstacles, 3)


# 跳起（深蹲）：3秒（重複五次）
# 攻擊（後跨步蹲抬手）：2秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
def Set3(time, all_sprites, obstacles):
    if time == 60 or time == 57 or time == 54 or time == 30 or time == 27 or time == 24:
        New_Obstacle(all_sprites, obstacles, 1)
    elif time == 51 or time == 48 or time == 45 or time == 21 or time == 18 or time == 15:
        New_Obstacle(all_sprites, obstacles, 2)
    elif time == 42 or time == 39 or time == 36 or time == 12 or time == 9 or time == 6:
        New_Obstacle(all_sprites, obstacles, 3)


# 攻擊（後跨步蹲抬手）：2秒（重複三次）
# 趴下（左右跨步蹲）：2秒（重複三次）
# 跳起（深蹲）：3秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
def Set4(time, all_sprites, obstacles):
    if time == 60 or time == 57 or time == 54 or time == 30 or time == 27 or time == 24:
        New_Obstacle(all_sprites, obstacles, 1)
    elif time == 51 or time == 48 or time == 45 or time == 21 or time == 18 or time == 15:
        New_Obstacle(all_sprites, obstacles, 2)
    elif time == 42 or time == 39 or time == 36 or time == 12 or time == 9 or time == 6:
        New_Obstacle(all_sprites, obstacles, 3)


# 趴下（左右跨步蹲）：2秒（重複三次）
# 跳起（深蹲）：2秒（重複五次）
# 攻擊（後跨步蹲抬手）：2秒（重複五次）
# 跳起（深蹲）：2秒（重複兩次）
def Set5(time, all_sprites, obstacles):
    if time == 60 or time == 57 or time == 54 or time == 30 or time == 27 or time == 24:
        New_Obstacle(all_sprites, obstacles, 1)
    elif time == 51 or time == 48 or time == 45 or time == 21 or time == 18 or time == 15:
        New_Obstacle(all_sprites, obstacles, 2)
    elif time == 42 or time == 39 or time == 36 or time == 12 or time == 9 or time == 6:
        New_Obstacle(all_sprites, obstacles, 3)
    
    