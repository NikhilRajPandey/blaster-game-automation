# Background : Photo by Francesco Ungaro from Pexels
# Music : https://www.youtube.com/watch?v=QglaLzo_aPk&list=PLKUA473MWUv03VnZLb98iAxdbCLxl0qG3

import pygame
import random

pygame.init()
pygame.mixer.init()

screen_width = 800
screen_height = 800
game_title = "Blaster"

background = pygame.image.load('images/background.jpg')


white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,128,0)

game_over = False
game_quit = False
game_started = False
game_over_reason = ""

pygame.display.set_caption(game_title)
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

heading_style = pygame.font.SysFont(None,200)
sub_heading_style = pygame.font.SysFont(None, 85)
fps = 75

player_position_x = 400
player_position_y = 600
height = 30  # One Box Height and width
PLAYER_VELOCITY = 5 # Constant of player velocity
player_velocity =  0 # PLAYER_VELOCITY
last_velocity_changed_x = -1

enemy_position_x_list = [random.randint(50,750),random.randint(50,750),random.randint(50,750)]

enemy_height = 45
enemy_position_y_list = [5,5,5]
enemy_velocity = 5
enemy_list = []

missile_height = 10
missile_position_list = []
missile_velocity = 12

def IN(A,B,C):
    # Defined for numbers
    return A >= B and A <= C
    
def fire():
    new_missile_x = player_position_x + height/2 - missile_height/2
    if len(missile_position_list) > 0:
        if player_position_y - missile_position_list[-1][1] < missile_height * 8: return
        
    missile_position_list.append([new_missile_x, player_position_y, True])
    
def plot_missile():
    for missile_position_x,missile_position_y,is_missile_launched in missile_position_list:
        if is_missile_launched:
            pygame.draw.rect(screen,red,[missile_position_x,missile_position_y,missile_height,missile_height])

def plot_enemy():
    for enemy_x,enemy_y in enemy_list:
        pygame.draw.rect(screen,green,[enemy_x,enemy_y,enemy_height,enemy_height])

def is_square_collision(a_x, a_y, a_h, b_x, b_y, b_h):
    # Just give you whether square a and square b have collided
    big_x, small_x = a_x, b_x
    big_y, small_y = a_y, b_y
    big_h, small_h = a_h, b_h
    
    if a_h < b_h:
        big_x, small_x = small_x, big_x
        big_y, small_y = small_y, big_y
        big_h, small_h = small_h, big_h

    x_check = IN(small_x, big_x, big_x + big_h) or IN(small_x + small_h, big_x, big_x + big_h)
    y_check = IN(small_y, big_y, big_y + big_h) or IN(small_y + small_h, big_y, big_y + big_h)

    return x_check and y_check

def is_missile_hit_enemy(enemy_x, enemy_y, missile_x, missile_y):
    return is_square_collision(enemy_x, enemy_y, enemy_height, missile_x, missile_y, missile_height)

def hardcoded_system():
    is_shoot = False
    direction = 0 # 0 means do nothing, 1 means left, 2 means right

    for i in range(len(enemy_position_x_list)):
        enemy_x, enemy_y = enemy_position_x_list[i], enemy_position_y_list[i]
        is_new_shoot =  IN(player_position_x + height/2, enemy_x, enemy_x + enemy_height)
        new_direction = 0

        """
        Extended player x is like imaginary boundary of the player, and if the enemy touch this imaginary
        boundary then system will change its velocity direction
        """
        ex_player_x = player_position_x - height
        ex_player_y = player_position_y - height
        ex_height = height * 3

        is_collide = is_square_collision(ex_player_x, ex_player_y, ex_height, enemy_x, enemy_y, enemy_height)
        
        if is_collide and player_position_x + height/2 < enemy_x + enemy_height:
            new_direction = 1
        elif is_collide and player_position_x + height/2 > enemy_x + enemy_height:
            new_direction = 2
            
        is_shoot = is_shoot or is_new_shoot
        direction =  direction or new_direction # Remember 0 or 2 = 2, 0 or 1 = 1

    # Prevention from wall collidation
    if screen_width - player_position_x <= height * 2 and player_velocity > 0:
        direction = 1
    elif player_position_x <= height * 2 and player_velocity < 0:
        direction = 2

    return [is_shoot, direction]


while not game_quit:
    if not game_started:
        screen.blit(background, [0, 0])

        # Intro
        heading = heading_style.render("Blaster",True,white)
        sub_heading = sub_heading_style.render("Enter to play this game", True, white)
        screen.blit(heading,[155,150])
        screen.blit(sub_heading,[70,300])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_started = True

    elif game_over:
        screen.blit(background, [0, 0])
        heading = heading_style.render("Game Over",True,white)
        sub_heading = sub_heading_style.render(game_over_reason,True,white)
        sub_heading_2 = sub_heading_style.render("Enter to play again", True, green)
        pygame.mixer.music.stop()

        screen.blit(heading,[10,50])
        screen.blit(sub_heading,[25,200])
        screen.blit(sub_heading_2, [120, 400])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_position_x = 400
                    player_position_y = 600
                    player_velocity = 0

                    enemy_position_x_list = [random.randint(50, 750), random.randint(50, 750), random.randint(50, 750)]
                    enemy_position_y_list = [5, 5, 5]
                    enemy_list = []

                    missile_position_list = []
                    game_over = False
    else:
        screen.blit(background, [0, 0])
        can_change_velocity = abs(player_position_x - last_velocity_changed_x) > height / 2
        
        model_result = hardcoded_system()        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dataset.to_csv("dataset.csv", index=False)
                game_quit = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and can_change_velocity:
                    last_velocity_changed_x = player_position_x
                    player_velocity = PLAYER_VELOCITY
                if event.key == pygame.K_LEFT and can_change_velocity:
                    last_velocity_changed_x = player_position_x
                    player_velocity = -PLAYER_VELOCITY
                if event.key == pygame.K_SPACE:
                    print(len(dataset[dataset["label_direction"] == 2]), len(dataset[dataset["label_shoot"] == 1]) )
                    fire()

        # model's Playing the game
        if model_result[0]:
            fire()
        if model_result[1] == 1 and can_change_velocity:
            last_velocity_changed_x = player_position_x
            player_velocity = -PLAYER_VELOCITY
        elif model_result[1] == 2 and can_change_velocity:
            last_velocity_changed_x = player_position_x
            player_velocity = PLAYER_VELOCITY
        
        # Declaring Enemy and player
        player = pygame.draw.rect(screen,white,[player_position_x,player_position_y,height,height])
        enemy_list.append([enemy_position_x_list[0], enemy_position_y_list[0]])
        enemy_list.append([enemy_position_x_list[1], enemy_position_y_list[1]])
        enemy_list.append([enemy_position_x_list[2], enemy_position_y_list[2]])

        if len(enemy_list) >= 6:  # If it was not written then enemy will become so long
            del enemy_list[0]
            del enemy_list[0]
            del enemy_list[0]

        plot_enemy()
        plot_missile()

        # Updating the position of the player,enemy and Missile
        player_position_x = player_position_x + player_velocity

        for enemy_position_y in enemy_position_y_list:
            current_position_index = enemy_position_y_list.index(enemy_position_y)
            enemy_position_y_list[current_position_index] = enemy_position_y_list[current_position_index] + enemy_velocity

        count_missile = 0  # In this for loop the enumerate function is not working so i used this

        for missile_position_y,missile_position_x,launched in missile_position_list:
            if launched:
                missile_position_list[count_missile][1] = missile_position_list[count_missile][1] - missile_velocity
            if missile_position_list[count_missile][1] < 0:  # Means The missile is collide
                del missile_position_list[count_missile]
            count_missile = count_missile + 1

        # Checking the player is out or not
        if player_position_x < 0 or player_position_x > (screen_width-25):
            game_over_reason = "You had collide with walls "
            game_over = True

        for enemy_x, enemy_y in enemy_list:
            if is_square_collision(enemy_x, enemy_y, enemy_height, player_position_x, player_position_y, height):
                game_over_reason = "You had collide with Enemy"
                game_over = True

        no_of_kills = 0  # I will use this later

        # Destroying Enemy when missile hit them
        for missile_count,(missile_x, missile_y, launched) in enumerate(missile_position_list):
            deleted_missile = False
            if launched:
                for enemy_count,(enemy_x, enemy_y) in enumerate(enemy_list):
                    # Means Missile hit the enemy
                    if is_missile_hit_enemy(enemy_x, enemy_y, missile_x, missile_y) and not deleted_missile:
                        curent_enemy_index = enemy_list.index([enemy_x, enemy_y])
                        
                        del enemy_list[curent_enemy_index]
                        del missile_position_list[missile_count]
                        
                        deleted_missile = True
                        enemy_position_x_list[curent_enemy_index] = random.randint(50,750)
                        enemy_position_y_list[curent_enemy_index] = 5

        # Taking Enemy Position 0 when it collides
        for enemy_position_y in enemy_position_y_list:
            if int(enemy_position_y) >= screen_height:
                index_of_current_position = enemy_position_y_list.index(enemy_position_y)
                enemy_position_y_list[index_of_current_position] = 5
                enemy_position_x_list[index_of_current_position] = random.randint(5,750)

        enemy_list = []

        pygame.display.update()
        clock.tick(fps)
        
