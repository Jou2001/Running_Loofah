from Obstacle import New_AttackObstacle, New_JumpObstacle, New_SlideObstacle

# 跳起（深蹲）：3秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
# 攻擊（後跨步蹲抬手）：3秒（重複三次）
# 休息三秒換下一個組合
def Set1(time, all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up):
    now = time % 40
    if  now == 33 or now == 31 or now == 29:
        New_JumpObstacle(all_sprites, obstacles)
        # New_AttackObstacle(all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up)
    elif now == 19 or now == 17 or now == 15:
        New_SlideObstacle(all_sprites, obstacles)
        # New_AttackObstacle(all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up)
    #elif now == 10 or now == 7 or now == 4:
    elif now == 9 or now == 6 or now == 3:
        New_AttackObstacle(all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up)


# 攻擊（後跨步蹲抬手）：3秒（重複五次）
# 趴下（左右跨步蹲）：2秒（重複三次）
# 跳起（深蹲）：3秒（重複三次）
def Set2(time, all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up):
    now = time % 40
    if now == 33 or now == 31:
        New_AttackObstacle(all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up)
    elif now == 21 or now == 19 or now == 17:
        New_SlideObstacle(all_sprites, obstacles)
    elif now == 7 or now == 5 or now == 3:
        New_JumpObstacle(all_sprites, obstacles)


# 跳起（深蹲）：3秒（重複五次）
# 攻擊（後跨步蹲抬手）：2秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
def Set3(time, all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up):
    now = time % 40
    if now == 33 or now == 31:
        New_JumpObstacle(all_sprites, obstacles)
    elif now == 21 or now == 19 :
        New_AttackObstacle(all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up)
    elif now == 9 or now == 6 or now == 3:
        New_SlideObstacle(all_sprites, obstacles)
        

# 攻擊（後跨步蹲抬手）：2秒（重複三次）
# 趴下（左右跨步蹲）：2秒（重複三次）
# 跳起（深蹲）：3秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
def Set4(time, all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up):
    now = time % 40
    if now == 33 or now == 31 or now == 29:
        New_SlideObstacle(all_sprites, obstacles)
    elif now == 19 or now == 17 or now == 15:
        New_JumpObstacle(all_sprites, obstacles)
    elif now == 5 or now == 3:
        New_SlideObstacle(all_sprites, obstacles)


# 趴下（左右跨步蹲）：2秒（重複三次）
# 跳起（深蹲）：2秒（重複五次）
# 攻擊（後跨步蹲抬手）：2秒（重複五次）
def Set5(time, all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up):
    now = time % 40
    if now == 33 or now == 31 or now == 29:
        New_SlideObstacle(all_sprites, obstacles)
    elif now == 19 or now == 17:
        New_JumpObstacle(all_sprites, obstacles)
    elif now == 7 or now == 5 or now == 3:
        New_AttackObstacle(all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up )
    
    
    
    