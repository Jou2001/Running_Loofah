import os
from PIL import Image, ImageDraw, ImageFont
import Material
import shutil

# Compare with the score in score.txt to see if the player's score needs to be put in.
def compare_score(score):
    file_path = "./rank/score.txt"
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            # The file is empty or the number of data entries is less than three.
            if not lines or len(lines) < 3:
                return True
            
            else:
                lines = [line.strip().split(",") for line in lines]
                top_scores = sorted([int(parts[0]) for parts in lines], reverse=True)
                
                if score > top_scores[-1]:    
                    delete_lowest_score()
                    return True
                else:
                    return False
    else:
        return True

# Delete the lowest score in score.txt.
def delete_lowest_score():
    file_path = "./rank/score.txt"
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            lines = [line.strip().split(",") for line in lines]
            if len(lines) == 3:
                lowest_score_index = lines.index(min(lines, key=lambda x: int(x[0])))
                lowest_score_photo_path = lines[lowest_score_index][1]
                
                del lines[lowest_score_index]
                
                if os.path.exists(lowest_score_photo_path):
                    os.remove(lowest_score_photo_path)
                
                with open(file_path, "w") as file:
                    for line in lines:
                        file.write(f"{line[0]},{line[1]}\n")

# Add new score and photo path to score.txt.
def add_score(score):
    scores = load_score_data()[:2]
    photo_path = save_photo()
    player_data = {
        "score": score,
        "photo_path": photo_path
    }
    scores.append(player_data)
    scores.sort(key=lambda x: x["score"], reverse=True)

    save_scores(scores)

# Get all data from score.txt. 
def load_score_data():
    scores = []
    with open("./rank/score.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(",")
                if len(parts) == 2:
                    player_data = {
                        "score": int(parts[0]),
                        "photo_path": parts[1].strip()
                    }
                    scores.append(player_data)
    return scores

# Save player's data to file.
def save_scores(scores):
    with open("./rank/score.txt", "w") as file:  # 指定完整的文件路径
        for player_data in scores:
            file.write(f"{player_data['score']},{player_data['photo_path']}\n")

def save_photo():
    number = str(find_missing_player_number())

    dst = './rank/Player/player' + number + '.png'
    src = './picture/player/HEALTHHEAD_1.png'

    if not os.path.exists('./rank/Player'):
        os.makedirs('./rank/Player')

    image = Image.open(src)
    resized_image = image.resize((245, 245))
    resized_image.save(dst)

    return dst

def find_missing_player_number():
    used_numbers = set()
    
    folder_path = "./rank/Player"
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        if not any(filename.startswith("player") and filename.endswith(".png") for filename in os.listdir(folder_path)):
            return 1
        else:
            for filename in os.listdir(folder_path):
                if filename.startswith("player") and filename.endswith(".png"):
                    number_str = filename[6:-4]
                    if number_str.isdigit():
                        number = int(number_str)
                        used_numbers.add(number)
                    
        for i in range(1, 4):
            if i not in used_numbers:
                return i
    
    return None

# Get new data to make the leaderboard.
def make_leaderboard():
    scores = load_score_data()
    leaderboard_path = './rank/Leaderboard/leaderboard.png'
    
    if os.path.exists(leaderboard_path):
        new_leaderboard_path = './rank/Leaderboard/newLeaderboard.png'
        shutil.copyfile(leaderboard_path, new_leaderboard_path)
        
        leaderboard = Image.open(new_leaderboard_path).convert('RGB')
        draw = ImageDraw.Draw(leaderboard)
        
        for i in range(min(len(scores), 3)):
            player_photo_path = scores[i]["photo_path"]
            player_score = scores[i]["score"]
            player_photo = Image.open(player_photo_path).convert('RGBA')
            
            # NO.1 position
            if i == 0:
                photo_x = 835
                photo_y = 395
                score_x = 844
                score_y = 720

            # # NO.2 position
            elif i == 1:
                photo_x = 447
                photo_y = 520
                score_x = 456
                score_y = 846

            # NO.13 position
            elif i == 2:
                photo_x = 1223
                photo_y = 520
                score_x = 1236
                score_y = 846
            
            leaderboard.paste(player_photo, (photo_x, photo_y), player_photo)

            font_size = 55
            font = ImageFont.truetype("Handwriting.ttf", size=font_size)
            text = str(player_score)

            text_width = len(text) * (font_size // 2)
            text_height = font_size

            target_width = 232
            target_height = 67

            x = score_x + (target_width - text_width) // 2
            y = score_y + (target_height - text_height) // 2

            draw.text((x, y), text, font=font, fill=(0, 0, 0))

        leaderboard.save(new_leaderboard_path, "PNG")

# if __name__ == '__main__':
def Make_Leaderboard(score):
    if compare_score(score):
        add_score(score)
    make_leaderboard()


