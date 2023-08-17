from Obstacle import New_AttackObstacle, New_JumpObstacle, New_SlideObstacle

# 跳起（深蹲）：3秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
# 攻擊（後跨步蹲抬手）：3秒（重複三次）
# 休息三秒換下一個組合
def Set1(time, all_sprites, obstacles, attackObstacles):
    now = time % 30
    if now == 0 or now == 27 or now == 24:
        New_JumpObstacle(all_sprites, obstacles)
    elif now == 21 or now == 18 or now == 15:
        New_SlideObstacle(all_sprites, obstacles)
    #elif now == 10 or now == 7 or now == 4:
    elif now <= 10:
        New_AttackObstacle(all_sprites, obstacles, attackObstacles)


# 攻擊（後跨步蹲抬手）：3秒（重複五次）
# 趴下（左右跨步蹲）：2秒（重複三次）
# 跳起（深蹲）：3秒（重複三次）
def Set2(time, all_sprites, obstacles, attackObstacles):
    now = time % 30
    if now == 0 or now == 27 or now == 24 or now == 21 or now == 18:
        New_AttackObstacle(all_sprites, obstacles, attackObstacles)
    elif now == 15 or now == 13 or now == 11:
        New_SlideObstacle(all_sprites, obstacles)
    elif now == 9 or now == 6 or now == 3:
        New_JumpObstacle(all_sprites, obstacles)


# 跳起（深蹲）：3秒（重複五次）
# 攻擊（後跨步蹲抬手）：2秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
def Set3(time, all_sprites, obstacles, attackObstacles):
    now = time % 30
    if now == 0 or now == 27 or now == 24 or now == 21 or now == 18:
        New_JumpObstacle(all_sprites, obstacles)
    elif now == 15 or now == 13 or now == 11:
        New_AttackObstacle(all_sprites, obstacles, attackObstacles)
    elif now == 9 or now == 6 or now == 3:
        New_SlideObstacle(all_sprites, obstacles)
        


# 攻擊（後跨步蹲抬手）：2秒（重複三次）
# 趴下（左右跨步蹲）：2秒（重複三次）
# 跳起（深蹲）：3秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
def Set4(time, all_sprites, obstacles, attackObstacles):
    now = time % 30
    if now == 0 or now == 28 or now == 26:
        New_AttackObstacle(all_sprites, obstacles, attackObstacles)
    elif now == 24 or now == 22 or now == 20:
        New_SlideObstacle(all_sprites, obstacles)
    elif now == 18 or now == 15 or now == 12:
        New_JumpObstacle(all_sprites, obstacles)
    elif now == 9 or now == 6 or now == 3:
        New_SlideObstacle(all_sprites, obstacles)


# 趴下（左右跨步蹲）：2秒（重複三次）
# 跳起（深蹲）：2秒（重複五次）
# 攻擊（後跨步蹲抬手）：2秒（重複五次）
# 跳起（深蹲）：2秒（重複兩次）
def Set5(time, all_sprites, obstacles, attackObstacles):
    now = time % 30
    if now == 0 or now == 28 or now == 26:
        New_SlideObstacle(all_sprites, obstacles)
    elif now == 24 or now == 22 or now == 20 or now == 18 or now == 16:
        New_JumpObstacle(all_sprites, obstacles)
    elif now == 14 or now == 12 or now == 10 or now == 8 or now == 6:
        New_AttackObstacle(all_sprites, obstacles, attackObstacles)
    elif now == 4 or now == 2:
        New_JumpObstacle(all_sprites, obstacles)
    
    