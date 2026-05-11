from pygame import *

# Setup
init() # Good practice to initialize
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 700
Size = (SCREEN_WIDTH, SCREEN_HEIGHT)
window = display.set_mode(Size)
display.set_caption('Catch Me If You Can')
clock = time.Clock()

# Assets
background = transform.scale(image.load('Background.png'), Size)
GhostSize = (100, 60)
HunterSize = (120, 120)
zombieSize = (300, 150)

GhostImg = transform.scale(image.load('Ghost.png'), GhostSize)
# Note: Rotating the base image here is fine
HunterBase = transform.rotate(transform.scale(image.load('Hunter.png'), HunterSize), 190)
zombieImg = transform.scale(image.load('Zombie.png'), zombieSize)

# Properties
GhostPosx, GhostPosy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
GhostSpeed = 9
angle = 0

zombiePosx, zombiePosy = 300, 300
zombieSpeed = 10

HunterPosx, HunterPosy = 200, 100
HunterSpeed = 4
Hunter_angle = 0

game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    keys = key.get_pressed()
    
    # --- PLAYER MOVEMENT (Ghost) ---
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
    elif keys[K_DOWN] and GhostPosy < SCREEN_HEIGHT - GhostSize[1]: # Changed to SCREEN_HEIGHT
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

    # --- ZOMBIE LOGIC ---
    zombiePosx += zombieSpeed
    if zombiePosx <= 0 or zombiePosx >= SCREEN_WIDTH - 300:
        zombieSpeed *= -1

    # --- DRAWING ---
    window.blit(background, (0, 0))
    
    # Ghost - Stays exactly as you had it
    rotated_ghost = transform.rotate(GhostImg, angle)
    window.blit(rotated_ghost, (GhostPosx, GhostPosy))

    # Hunter - FIXED ROTATION AND CENTERING
    # We subtract 90 because your image faces UP, but Pygame's 0-degrees is RIGHT
    rotated_hunter = transform.rotate(HunterBase, Hunter_angle - 90)
    
    # This keeps the Hunter from "teleporting" when he rotates
    hunter_rect = rotated_hunter.get_rect(center=(HunterPosx + HunterSize[0]//2, HunterPosy + HunterSize[1]//2))
    window.blit(rotated_hunter, hunter_rect)
    
    # Zombie
    window.blit(zombieImg, (zombiePosx, zombiePosy))

    display.update() # Don't forget to update the screen!
    
    display.update()
    clock.tick(60) # Limits the game to 60 Frames Per Second