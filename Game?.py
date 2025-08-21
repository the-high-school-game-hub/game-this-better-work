import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Scavenger")

# Clock
clock = pygame.time.Clock()

# Colors
BLACK = (10, 10, 30)
WHITE = (255, 255, 255)

# Load image helper
def load_image(name, scale=None):
    path = os.path.join("assets", name)
    if not os.path.exists(path):
        print(f"❌ ERROR: '{path}' does not exist.")
        sys.exit(1)

    try:
        img = pygame.image.load(path)
        try:
            img = img.convert_alpha()
        except pygame.error:
            img = img.convert()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except pygame.error as e:
        print(f"❌ ERROR loading image '{name}': {e}")
        sys.exit(1)

# Load sprites
spaceship_img = load_image("spaceship.png", (64, 64))
planet_img = load_image("planet.png", (100, 100))

# Font
font = pygame.font.SysFont("Arial", 24)

# Game variables
spaceship_rect = spaceship_img.get_rect()
spaceship_rect.center = (WIDTH // 2, HEIGHT - 100)
spaceship_speed = 5

planet_rect = planet_img.get_rect()
planet_rect.center = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT // 2))

inventory = []
health = 110
status_message = "Fly to the planet to explore!"

resources = ["alien metal", "crystals", "fuel", "ancient tech"]
hazards = ["space pirates", "asteroid storm", "toxic gas", "hostile lifeforms"]

# Landing and explore logic
def land_on_planet():
    global health, status_message
    event_roll = random.randint(1, 10)
    if event_roll <= 6:
        found = random.choice(resources)
        inventory.append(found)
        status_message = f"🪐 You found {found}!"
    else:
        hazard = random.choice(hazards)
        damage = random.randint(10, 30)
        health -= damage
        status_message = f"⚠️ You hit {hazard}, lost {damage} HP!"

    # Move planet to new location
    planet_rect.center = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT // 2))

# Draw text helper
def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        spaceship_rect.x -= spaceship_speed
    if keys[pygame.K_RIGHT]:
        spaceship_rect.x += spaceship_speed
    if keys[pygame.K_UP]:
        spaceship_rect.y -= spaceship_speed
    if keys[pygame.K_DOWN]:
        spaceship_rect.y += spaceship_speed

    # Keep ship in bounds
    spaceship_rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    # Collision check
    if spaceship_rect.colliderect(planet_rect):
        land_on_planet()

    # Draw sprites
    screen.blit(planet_img, planet_rect)
    screen.blit(spaceship_img, spaceship_rect)

    # UI
    draw_text(f"Health: {health}", 20, 20)
    draw_text(f"Inventory: {', '.join(inventory[-3:]) or 'None'}", 20, 50)
    draw_text(status_message, 20, 80)

    if health <= 0:
        draw_text("💀 GAME OVER - You died in space", 20, 140)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
