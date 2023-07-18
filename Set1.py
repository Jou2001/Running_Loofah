# 跳起（深蹲）：3秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
# 攻擊（後跨步蹲抬手）：3秒（重複三次）
# 休息三秒換下一個組合

from tempGame import New_Obstacle
import pygame

def Run(time, all_sprites, obstacles):
    if time == 60 or time == 57 or time == 54:
        New_Obstacle(all_sprites, obstacles, 1)
    elif time == 51 or time == 48 or time == 45:
        New_Obstacle(all_sprites, obstacles, 2)
    elif time == 42 or time == 39 or time == 36:
        New_Obstacle(all_sprites, obstacles, 3)
    
    