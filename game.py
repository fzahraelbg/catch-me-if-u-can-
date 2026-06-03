from pygame import *
from random import randint
import os

# Setup
init() 
font.init() # Initialize the font module

# --- DYNAMIC SCREEN ADAPTATION ---
# This grabs the exact resolution of whatever laptop runs the game
screen_info = display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
Size = (SCREEN_WIDTH, SCREEN_HEIGHT)

# FULLSCREEN makes it fit perfectly, or use RESIZABLE if you want a normal window
window = display.set_mode(Size, FULLSCREEN) 
display.set_caption('Catch Me If You Can')

# --- HIGH SCORE SYSTEM ---
HIGH_SCORE_FILE = "highscore.txt"
high_score = 0

if os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, "r") as file:
        try:
            high_score = int(file.read())
        except ValueError:
            high_score = 0
else:
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write("0")

# --- COOL FONTS SETUP ---
game_over_font = font.SysFont("impact", 100)
score_font = font.SysFont("impact", 40)      
high_score_font = font.SysFont("impact", 30)
replay_font = font.SysFont("impact", 35)       

# Assets
background = transform.scale(image.load('Background.png'), Size)
GhostSize = (100, 60)
HunterSize = (120, 120)
zombieSize = (300, 150)

GhostImg = transform.scale(image.load('Ghost.png'), GhostSize)
HunterBase = transform.scale(image.load('Hunter.png'), HunterSize)
zombieImg = transform.scale(image.load('Zombie.png'), zombieSize)

# Properties

# Player Ghost (Starts in dead center)
GhostPosx, GhostPosy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
GhostSpeed = 20
angle = 0

# Zombie 1 (Moves Left & Right)
zombiePosx, zombiePosy = 300, SCREEN_HEIGHT // 2
zombieSpeed = 10

# Zombie 2 (Centered horizontally, moves Up & Down)
zombie2Posx = (SCREEN_WIDTH // 2) - (zombieSize[0] // 2)
zombie2Posy = 100
zombie2SpeedY = 8

# Hunter
HunterPosx, HunterPosy = 200, 100
HunterSpeed = 4
Hunter_angle = 0

game = True
game_over = False  
clock = time.Clock()

# Score tracking variables
score = 0
start_ticks = time.get_ticks() 
last_speed_update = 0  

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        # Allow pressing the Escape key to close the game since it is Fullscreen
        if e.type == KEYDOWN and e.key == K_ESCAPE:
            game = False
        
        # --- REPLAY MECHANIC ---
        if game_over and e.type == KEYDOWN:
            if e.key == K_r:
                game_over = False
                score = 0
                last_speed_update = 0
                start_ticks = time.get_ticks() 
                
                GhostPosx, GhostPosy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                angle = 0
                
                zombiePosx, zombiePosy = 300, SCREEN_HEIGHT // 2
                zombieSpeed = 10
                
                zombie2Posy = 100
                zombie2SpeedY = 8
                
                HunterPosx, HunterPosy = 200, 100
                Hunter_angle = 0

    # Only allow movement and physics updates if the game isn't over
    if not game_over:
        keys = key.get_pressed()
        
        # --- SCORE & DIFFICULTY LOGIC ---
        score = (time.get_ticks() - start_ticks) // 1000 
        
        if score > 0 and score // 10 > last_speed_update:
            last_speed_update = score // 10
            
            if zombieSpeed > 0: zombieSpeed += 2
            else: zombieSpeed -= 2
                
            if zombie2SpeedY > 0: zombie2SpeedY += 2
            else: zombie2SpeedY -= 2

        # --- PLAYER MOVEMENT (Ghost with Adaptive Boundaries) ---
        if keys[K_LEFT] and keys[K_UP]:
            GhostPosx -= GhostSpeed; GhostPosy -= GhostSpeed; angle = 45
        elif keys[K_RIGHT] and keys[K_UP]:
            GhostPosx += GhostSpeed; GhostPosy -= GhostSpeed; angle = -45
        elif keys[K_LEFT] and keys[K_DOWN]:
            GhostPosx -= GhostSpeed; GhostPosy += GhostSpeed; angle = 135
        elif keys[K_RIGHT] and keys[K_DOWN]:
            GhostPosx += GhostSpeed; GhostPosy += GhostSpeed; angle = 225
        elif keys[K_UP] and GhostPosy > 0: 
            GhostPosy -= GhostSpeed; angle = 0
        elif keys[K_DOWN] and GhostPosy < SCREEN_HEIGHT - GhostSize[1]:
            GhostPosy += GhostSpeed; angle = 180
        elif keys[K_LEFT] and GhostPosx > 0:
            GhostPosx -= GhostSpeed; angle = 90
        elif keys[K_RIGHT] and GhostPosx < SCREEN_WIDTH - GhostSize[0]:
            GhostPosx += GhostSpeed; angle = -90

        # --- HUNTER SEARCHING LOGIC ---
        if HunterPosx < GhostPosx: HunterPosx += HunterSpeed; Hunter_angle = 0
        if HunterPosx > GhostPosx: HunterPosx -= HunterSpeed; Hunter_angle = 180
        if HunterPosy < GhostPosy: HunterPosy += HunterSpeed; Hunter_angle = -90
        if HunterPosy > GhostPosy: HunterPosy -= HunterSpeed; Hunter_angle = 90
        
        # Diagonals
        if HunterPosx < GhostPosx and HunterPosy < GhostPosy: Hunter_angle = -45
        if HunterPosx < GhostPosx and HunterPosy > GhostPosy: Hunter_angle = 45
        if HunterPosx > GhostPosx and HunterPosy < GhostPosy: Hunter_angle = -135
        if HunterPosx > GhostPosx and HunterPosy > GhostPosy: Hunter_angle = 135
        
        # --- ZOMBIE 1 LOGIC (Adapts to Screen Width) ---
        zombiePosx += zombieSpeed
        if zombiePosx <= 0 or zombiePosx >= SCREEN_WIDTH - zombieSize[0]:
            zombieSpeed *= -1

        # --- ZOMBIE 2 LOGIC (Adapts to Screen Height) ---
        zombie2Posy += zombie2SpeedY
        if zombie2Posy <= 0 or zombie2Posy >= SCREEN_HEIGHT - zombieSize[1]:
            zombie2SpeedY *= -1

    # --- COLLISION DETECTORS ---
    ghost_rect   = GhostImg.get_rect(topleft=(GhostPosx, GhostPosy))
    hunter_rect  = HunterBase.get_rect(topleft=(HunterPosx, HunterPosy))
    zombie_rect  = zombieImg.get_rect(topleft=(zombiePosx, zombiePosy))
    zombie2_rect = zombieImg.get_rect(topleft=(zombie2Posx, zombie2Posy))

    hit_zombie = ghost_rect.colliderect(zombie_rect) or ghost_rect.colliderect(zombie2_rect)

    # --- DRAWING ---
    if (hit_zombie and not game_over) or game_over:
        window.blit(background, (randint(-5, 5), randint(-5, 5)))
    else:
        window.blit(background, (0, 0))
    
    # Rotate textures
    rotated_ghost  = transform.rotate(GhostImg, angle)
    rotated_hunter = transform.rotate(HunterBase, Hunter_angle)

    # Draw all characters to the window
    window.blit(rotated_ghost, (GhostPosx, GhostPosy))
    window.blit(rotated_hunter, (HunterPosx, HunterPosy))
    window.blit(zombieImg, (zombiePosx, zombiePosy))
    window.blit(zombieImg, (zombie2Posx, zombie2Posy)) 

    # --- ZOMBIE HIT EFFECT ---
    if hit_zombie and not game_over:
        green = Surface(Size, SRCALPHA)
        green.fill((0, 255, 0, 60)) 
        window.blit(green, (0, 0))

    # --- HUNTER HIT LOGIC (Triggers Game Over) ---
    if ghost_rect.colliderect(hunter_rect) and not game_over: 
        game_over = True
        if score > high_score:
            high_score = score
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write(str(high_score))

    # --- DISPLAY SCORE & HIGH SCORE LIVE ---
    score_surface = score_font.render(f"SCORE: {score}", True, (255, 255, 255))
    window.blit(score_surface, (20, 20)) 
    
    hi_score_surface = high_score_font.render(f"BEST: {high_score}", True, (243, 156, 18)) 
    window.blit(hi_score_surface, (20, 70))

    # --- PERMANENT GAME OVER OVERLAY ---
    if game_over:
        red = Surface(Size, SRCALPHA)
        red.fill((255, 0, 0, 100)) 
        window.blit(red, (0, 0))
        
        # Central text assets dynamically adapt to center point of whatever screen scale is active
        text_surface = game_over_font.render("GAME OVER", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        window.blit(text_surface, text_rect)
        
        final_score_surface = score_font.render(f"YOUR SCORE: {score}", True, (255, 255, 255))
        final_score_rect = final_score_surface.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 80))
        window.blit(final_score_surface, final_score_rect)
        
        replay_surface = replay_font.render("Press 'R' to Play Again", True, (255, 255, 255))
        replay_rect = replay_surface.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 140))
        window.blit(replay_surface, replay_rect)

    display.update()
    clock.tick(60)