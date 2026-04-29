from pygame import *

# Setup
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 700
Size = (SCREEN_WIDTH, SCREEN_HEIGHT)
window = display.set_mode(Size)
display.set_caption('Catch Me If You Can')
clock = time.Clock() # Added to keep speed consistent

# Assets
background = transform.scale(image.load('Background.png'), Size)
GhostSize = (100, 60)
HunterSize = (200, 100)
zombieSize = (300, 150)

GhostImg = transform.scale(image.load('Ghost.png'), GhostSize)
Hunter = transform.rotate(transform.scale(image.load('Hunter.png'), HunterSize), 190)
zombie = transform.scale(image.load('Zombie.png'), zombieSize)

# Properties
GhostPosx, GhostPosy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
GhostSpeed = 9

zombiePosx, zombiePosy = 300, 300
zombieSpeed = 10

HunterPosx, HunterPosy = 200, 100
HunterSpeed = 4 # Slow searching speed
angle = 0

game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    keys = key.get_pressed()
    moving = False # Track if player is pressing keys

    # --- PLAYER MOVEMENT ---
    if keys[K_LEFT] and keys[K_UP]:
        GhostPosx -= GhostSpeed
        GhostPosy -= GhostSpeed
        angle, moving = 45, True
    elif keys[K_RIGHT] and keys[K_UP]:
        GhostPosx += GhostSpeed
        GhostPosy -= GhostSpeed
        angle, moving = -45, True
    elif keys[K_LEFT] and keys[K_DOWN]:
        GhostPosx -= GhostSpeed
        GhostPosy += GhostSpeed
        angle, moving = 135, True
    elif keys[K_RIGHT] and keys[K_DOWN]:
        GhostPosx += GhostSpeed
        GhostPosy += GhostSpeed
        angle, moving = 225, True
    elif keys[K_UP]:
        GhostPosy -= GhostSpeed
        angle, moving = 0, True
    elif keys[K_DOWN]:
        GhostPosy += GhostSpeed
        angle, moving = 180, True
    elif keys[K_LEFT]:
        GhostPosx -= GhostSpeed
        angle, moving = 90, True
    elif keys[K_RIGHT]:
        GhostPosx += GhostSpeed
        angle, moving = -90, True

    # --- Hunter SEARCHING LOGIC ---
    dx = GhostPosx - HunterPosx
    dy = GhostPosy - HunterPosy

    if abs(dx) > 0:
        HunterPosx += HunterSpeed if dx > 0 else -HunterSpeed
    if abs(dy) > 0:
        HunterPosy += HunterSpeed if dy > 0 else -HunterSpeed

    # --- COLLISION / THE CATCH ---
    ghost_rect = Rect(GhostPosx, GhostPosy, GhostSize[0], GhostSize[1])
    Hunter_rect = Rect(HunterPosx, HunterPosy, HunterSize[0], HunterSize[1])



    # --- ZOMBIE LOGIC ---
    zombiePosx += zombieSpeed
    if zombiePosx <= 0 or zombiePosx >= SCREEN_WIDTH - 150:
        zombieSpeed *= -1

    # --- DRAWING ---
    window.blit(background, (0, 0))
    # Using the angle to rotate the top-view hunter
    rotated_ghost = transform.rotate(GhostImg, angle)
    window.blit(rotated_ghost, (GhostPosx, GhostPosy))
    
    window.blit(Hunter, (HunterPosx, HunterPosy))
    window.blit(zombie, (zombiePosx, zombiePosy))

    display.update()
    clock.tick(60) # Limits the game to 60 FPS