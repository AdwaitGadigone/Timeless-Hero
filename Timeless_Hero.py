"""
Timeless Hero
-------------
A 6-level time-travel platformer game built in Python using PyGame and Tkinter.
Created by Adwait, Richard, and Aditya for the 2025 Game Making Competition.
"""
#import modules and libraries 
import sys
import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import tkinter as tk

def center_window(window, width=1000, height=600):
    """Helper function to center Tkinter windows on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def dialogue():
    # Defining what happens when the user clicks the continue button to proceed to the next screen
    def continue_clicked():
        root.destroy()
        dialogue2()

    # Setting up the Tkinter window for the first dialogue box
    root = tk.Tk()
    root.title("Timeless Hero - Intro")
    center_window(root)
    root.configure(bg="#2c3e50")  # Dark background color for a sleek look

    # Text properties for the "Timeless Hero" label (larger size)
    title_label = tk.Label(root, wraplength=580, font=("Impact", 32, "bold"), text="TIMELESS HERO", bg="#2c3e50", fg="white", justify="center")
    title_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    # Text properties for the "Created by..." label (smaller size)
    created_by_label = tk.Label(root, wraplength=580, font=("Comic Sans MS", 16), text="A game created by Adwait and Aditya\nfor the 2025 Game Making Competition", bg="#2c3e50", fg="white", justify="center")
    created_by_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create button with improved styling
    button = tk.Button(root, text="Continue", width=15, height=2, font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", relief="flat", command=continue_clicked)
    button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    # Add hover effect for the button
    def on_enter(e):
        button.config(bg="#45a049")

    def on_leave(e):
        button.config(bg="#4CAF50")

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    root.mainloop()


# Second dialogue box
def dialogue2():
    # Function triggered when the Continue button is clicked
    def continue_clicked():
        root.destroy()
        dialogue3()  # Proceed to dialogue3 (Objective)

    # Create the Tkinter window for the storyline screen
    root = tk.Tk()
    root.title("Timeless Hero - Storyline")
    center_window(root)
    root.configure(bg="#2c3e50")  # Dark background color for aesthetic

    # Title/Heading Label
    story_header = tk.Label(root, text="STORYLINE", font=("Impact", 20, "bold"),
                            fg="white", bg="#2c3e50")
    story_header.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    # Main storyline text
    story_text = (
        "\nTrapped in time, the hero needs your help to find a way back.\n\n"
        "Advance through different eras, collect timers, and reach the time machines.\n\n"
        "Each time machine will transport him to a new point in history.\n\n"
        "But be careful—time goons lurk across timelines trying to stop you.\n\n"
        "Help the hero get back to the future?"
    )

    # Display the storyline in the center
    label = tk.Label(root, text=story_text, font=("Comic Sans MS", 14),
                     fg="white", bg="#2c3e50", justify="center", wraplength=800)
    label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

    # Continue Button
    button = tk.Button(root, text="Continue", width=15, height=2,
                       font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                       relief="flat", command=continue_clicked)
    button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    # Button hover effects
    def on_enter(e): button.config(bg="#45a049")
    def on_leave(e): button.config(bg="#4CAF50")

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    root.mainloop()

# Third dialogue box 
def dialogue3():
    import os
    from PIL import ImageTk, Image

    def start_adventure():
        control_window.destroy()

    # Set up the controls dialogue window
    control_window = tk.Tk()
    control_window.title("Timeless Hero - Controls")
    center_window(control_window)
    control_window.configure(bg="#2c3e50")  

    # Heading Label ("CONTROLS")
    header = tk.Label(control_window, text="CONTROLS", font=("Impact", 30, "bold"),
                      fg="white", bg="#2c3e50")
    header.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    # Image display 
    img_path = "img/controls.png"  # Replace with your image path
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img = img.resize((400, 250))  # Adjust size as needed
        img_tk = ImageTk.PhotoImage(img)
        img_label = tk.Label(control_window, image=img_tk, bg="#2c3e50")
        img_label.image = img_tk  # Keep reference t
        img_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    else:
        img_label = tk.Label(control_window, text="[Image Missing]", font=("Helvetica", 12),
                             fg="gray", bg="#2c3e50")
        img_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Start button
    start_button = tk.Button(control_window, text="Start Adventure", width=15, height=2,
                             font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", relief="flat",
                             command=start_adventure)
    start_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    # Hover effects
    def on_enter(e): start_button.config(bg="#45a049")
    def on_leave(e): start_button.config(bg="#4CAF50")

    start_button.bind("<Enter>", on_enter)
    start_button.bind("<Leave>", on_leave)

    control_window.mainloop()


###################


#Actual Platformer Game
def platformer():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()
    pygame.init()

    clock = pygame.time.Clock()
    fps = 60

    screen_width = 1000
    screen_height = 800

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Timeless Hero')

    # Camera variables
    camera_offset_x = 0
    camera_offset_y = 0
    
    # Function to update camera position based on player position
    def update_camera(player_rect):
        nonlocal camera_offset_x, camera_offset_y
        
        # Center player horizontally with some lookahead based on direction
        target_offset_x = screen_width//2 - player_rect.centerx
        
        # Center player vertically with some bottom bias
        target_offset_y = screen_height//2 - player_rect.centery + 100
        
        # Smooth camera movement (lerping)
        camera_offset_x += (target_offset_x - camera_offset_x) * 0.1
        camera_offset_y += (target_offset_y - camera_offset_y) * 0.1
        
        # Optional: Limit camera to level bounds if you know level dimensions
        # For now, we'll just ensure we don't show empty space on the left or top
        camera_offset_x = min(0, camera_offset_x)
        camera_offset_y = min(0, camera_offset_y)

    #define font
    font = pygame.font.SysFont('Bauhaus 93', 70)
    font_score = pygame.font.SysFont('Bauhaus 93', 30)

    #game variables
    tile_size = 50
    game_over = 0
    main_menu = True
    level = 0
    max_levels = 4 # counting form index 0
    score = 0

    #define colours
    white = (255, 255, 255)
    blue = (0, 0, 255)

    #load images
    restart_img = pygame.image.load('img/restart_btn.png')
    start_img = pygame.image.load('img/start_btn.png')
    exit_img = pygame.image.load('img/exit_btn.png')

    # Load title screen (sky image) background
    title_bg = pygame.image.load('TimelessHero-assets/title_sky.gif')
    title_bg = pygame.transform.scale(title_bg, (screen_width, screen_height))  # Scale it to the screen size

    # Create a list of background images for each level
    bg_images = []
    for level_num in range(max_levels + 1):  # +1 because levels start at 0
        try:
            # Try to load a level-specific background
            bg_img = pygame.image.load(f'TimelessHero-assets/bg_level{level_num}.png')
        except:
            # If level-specific background doesn't exist, use menu
            bg_img = pygame.image.load('TimelessHero-assets/title_sky.gif')
        bg_images.append(bg_img)

    # Current background image
    current_bg = title_bg  # Initially, the title screen background is shown

    #load sounds
    pygame.mixer.music.load('img/music.wav')
    pygame.mixer.music.play(-1, 0.0, 5000)
    coin_fx = pygame.mixer.Sound('img/coin.wav')
    coin_fx.set_volume(0.5)
    jump_fx = pygame.mixer.Sound('img/jump.wav')
    jump_fx.set_volume(0.5)
    game_over_fx = pygame.mixer.Sound('img/game_over.wav')
    game_over_fx.set_volume(0.5)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    #function to reset level
    def reset_level(level):
        player.reset(100, screen_height - 130)
        blob_group.empty()
        platform_group.empty()
        coin_group.empty()
        lava_group.empty()
        exit_group.empty()

        world_data = []  # Initialize world_data

        #load in level data and create world
        if path.exists(f'leveldata/level{level}_data'):
            pickle_in = open(f'leveldata/level{level}_data', 'rb')
            world_data = pickle.load(pickle_in)
        
        world = World(world_data)
        return world


    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False

        def draw(self):
            action = False

            #get mouse position
            pos = pygame.mouse.get_pos()

            #check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #draw button (UI elements don't use camera offset)
            screen.blit(self.image, self.rect)

            return action


    class Player():
        """
        The main hero of the game! This class handles the player's movement,
        jumping physics, animations, and collision detection with platforms, enemies, and lava.
        """
        def __init__(self, x, y):
            self.reset(x, y)

        def update(self, game_over):
            dx = 0
            dy = 0
            walk_cooldown = 5
            col_thresh = 20

            if game_over == 0:
                #get keypresses
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                    jump_fx.play()
                    self.vel_y = -15
                    self.jumped = True
                if key[pygame.K_SPACE] == False:
                    self.jumped = False
                if key[pygame.K_LEFT]:
                    dx -= 5
                    self.counter += 1
                    self.direction = -1
                if key[pygame.K_RIGHT]:
                    dx += 5
                    self.counter += 1
                    self.direction = 1
                if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                    self.counter = 0
                    self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

                #handle animation
                if self.counter > walk_cooldown:
                    self.counter = 0    
                    self.index += 1
                    if self.index >= len(self.images_right):
                        self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

                #add gravity
                self.vel_y += 1
                if self.vel_y > 10:
                    self.vel_y = 10
                dy += self.vel_y

                #check for collision
                self.in_air = True
                for tile in world.tile_list:
                    #check for collision in x direction
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    #check for collision in y direction
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        #check if below the ground i.e. jumping
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0
                        #check if above the ground i.e. falling
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0
                            self.in_air = False

                #check for collision with enemies
                if pygame.sprite.spritecollide(self, blob_group, False):
                    game_over = -1
                    game_over_fx.play()

                #check for collision with lava
                if pygame.sprite.spritecollide(self, lava_group, False):
                    game_over = -1
                    game_over_fx.play()

                #check for collision with exit
                if pygame.sprite.spritecollide(self, exit_group, False):
                    game_over = 1

                #check for collision with platforms
                for platform in platform_group:
                    #collision in the x direction
                    if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    #collision in the y direction
                    if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        #check if below platform
                        if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                            self.vel_y = 0
                            dy = platform.rect.bottom - self.rect.top
                        #check if above platform
                        elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                            self.rect.bottom = platform.rect.top - 1
                            self.in_air = False
                            dy = 0
                        #move sideways with the platform
                        if platform.move_x != 0:
                            self.rect.x += platform.move_direction

                #update player coordinates
                self.rect.x += dx
                self.rect.y += dy

            elif game_over == -1:
                self.image = self.dead_image
                draw_text('GAME OVER!', font, white, (screen_width // 2) - 200, screen_height // 2)
                if self.rect.y > 200:
                    self.rect.y -= 5

            #draw player onto screen with camera offset
            screen.blit(self.image, (self.rect.x + camera_offset_x, self.rect.y + camera_offset_y))

            return game_over

        def reset(self, x, y):
            self.images_right = []
            self.images_left = []
            self.index = 0
            self.counter = 0
            for num in range(0, 6):
                img_right = pygame.image.load(f'TimelessHero-assets/guy{num}.gif')
                img_right = pygame.transform.scale(img_right, (35, 80))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
            self.dead_image = pygame.image.load('img/ghost.png')
            self.image = self.images_right[self.index]
            self.draw_rect = self.image.get_rect()
            self.draw_rect.x = x
            self.draw_rect.y = y
               
            # Create a smaller rect for collision detection (hitbox)
            self.rect = pygame.Rect(0, 0, 40, 80)  # Smaller width and height
            self.rect.centerx = self.draw_rect.centerx  # Center the hitbox horizontally
            self.rect.bottom = self.draw_rect.bottom    # Align to bottom of sprite
            
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.vel_y = 0
            self.jumped = False
            self.direction = 0
            self.in_air = True


    class World():
        """
        Constructs the current level using grid data. Places dirt, grass, enemies,
        lava, coins, and the exit based on tile numbers defined in the level file.
        """
        def __init__(self, data):
            self.tile_list = []

            #load images
            dirt_img = pygame.image.load('img/dirt.png')
            grass_img = pygame.image.load('img/grass.png')

            row_count = 0
            for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 2:
                        img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 3:
                        blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                        blob_group.add(blob)
                    if tile == 4:
                        platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                        platform_group.add(platform)
                    if tile == 5:
                        platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                        platform_group.add(platform)
                    if tile == 6:
                        lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        lava_group.add(lava)
                    if tile == 7:
                        coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                        coin_group.add(coin)
                    if tile == 8:
                        exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                        exit_group.add(exit)
                    col_count += 1
                row_count += 1

        def draw(self):
            for tile in self.tile_list:
                # Apply camera offset when drawing tiles
                screen.blit(tile[0], (tile[1].x + camera_offset_x, tile[1].y + camera_offset_y))


    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('TimelessHero-assets/blob.gif')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.move_direction = 1
            self.move_counter = 0

        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 1
            if abs(self.move_counter) > 50:
                self.move_direction *= -1
                self.move_counter *= -1
                
        def draw(self, screen):
            # Draw with camera offset
            screen.blit(self.image, (self.rect.x + camera_offset_x, self.rect.y + camera_offset_y))


    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y, move_x, move_y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('img/platform.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.move_counter = 0
            self.move_direction = 1
            self.move_x = move_x
            self.move_y = move_y

        def update(self):
            self.rect.x += self.move_direction * self.move_x
            self.rect.y += self.move_direction * self.move_y
            self.move_counter += 1
            if abs(self.move_counter) > 50:
                self.move_direction *= -1
                self.move_counter *= -1
                
        def draw(self, screen):
            # Draw with camera offset
            screen.blit(self.image, (self.rect.x + camera_offset_x, self.rect.y + camera_offset_y))


    class Lava(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('img/lava.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            
        def draw(self, screen):
            # Draw with camera offset
            screen.blit(self.image, (self.rect.x + camera_offset_x, self.rect.y + camera_offset_y))


    class Coin(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('img/coin.png')
            self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            
        def draw(self, screen):
            # Draw with camera offset
            screen.blit(self.image, (self.rect.x + camera_offset_x, self.rect.y + camera_offset_y))

    class Exit(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('TimelessHero-assets/exit.png')
            self.image = pygame.transform.scale(img, (int(tile_size * 1.25), int(tile_size * 1.875)))
            self.rect = self.image.get_rect()
            self.rect.x = x - 10
            self.rect.y = y - 18
            
        def draw(self, screen):
            # Draw with camera offset
            screen.blit(self.image, (self.rect.x + camera_offset_x, self.rect.y + camera_offset_y))

    def show_congratulations_screen():
        """
        Displays a congratulatory message when the player finishes all 6 levels.
        Waits for the player to click the exit button before closing the game.
        """
        # Load ending image
        congrats_img = pygame.image.load('TimelessHero-assets/endscreen.png')
        congrats_img = pygame.transform.scale(congrats_img, (screen_width, screen_height))

        # Display ending congratulations image
        screen.blit(congrats_img, (0, 0))

       # Resize the exit button image to make it smaller
        exit_img_small = pygame.transform.scale(exit_img, (150, 70))
        # Create an exit button (position it near the bottom of the screen)
        exit_button = Button(screen_width // 2 - 75, screen_height - 100, exit_img_small)  # Position near bottom

        # Draw the exit button
        exit_button.draw()

        pygame.display.update()

        # Wait for the user to click the exit button to exit the game
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True # Signal to quit the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                        # Exit the game if the exit button is clicked
                        return True
        return False

    #new player calculation   
    player = Player(100, screen_height - 130)
    blob_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    lava_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()

    #create dummy coin for showing the score
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)

    #load in level data and create world
    if path.exists(f'leveldata/level{level}_data'):
        pickle_in = open(f'leveldata/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    #create buttons
    restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
    start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
    exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

    run = True
    while run:
        clock.tick(fps)
        
        # Draw the current background
        screen.blit(current_bg, (0, 0))

        if main_menu == True:
            if exit_button.draw():
                run = False
            if start_button.draw():
                main_menu = False
                current_bg = bg_images[level]
        else:
            # Update camera position based on player position
            update_camera(player.rect)
            
            # Draw world with camera offset
            world.draw()

            if game_over == 0:
                blob_group.update()
                platform_group.update()
                #update score
                #check if a coin has been collected
                if pygame.sprite.spritecollide(player, coin_group, True):
                    score += 1
                    coin_fx.play()
                draw_text('Timers Collected: ' + str(score), font_score, white, tile_size - 10, 10)
            
            # Draw all game elements with camera offset
            for blob in blob_group:
                blob.draw(screen)
            for platform in platform_group:
                platform.draw(screen)
            for lava in lava_group:
                lava.draw(screen)
            for coin in coin_group:
                coin.draw(screen)
            for exit in exit_group:
                exit.draw(screen)

            game_over = player.update(game_over)

            #if player has died
            if game_over == -1:
                if restart_button.draw():
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0
            
            # If player has completed the level by reaching the time machine exit
            if game_over == 1:
                level += 1
                if level <= max_levels:
                    # Reset the game world and go to the next timeline level
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    current_bg = bg_images[level]
                else:
                    # Player has completed all timelines! Show the end screen.
                    if show_congratulations_screen():
                        run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
    
# Code Executions
dialogue()
platformer()



