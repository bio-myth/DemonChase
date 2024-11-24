import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions and setup
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Demon Chase")

# Fonts and clock
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (50, 205, 50)

# Game variables
gravity = 1
player_speed = 5
player_jump = -15
score = 0

# Player variables
player_x = 50
player_y = SCREEN_HEIGHT - 100
player_size = 50
velocity_y = 0
is_jumping = False
player_img = pygame.image.load(r"C:\Users\devan\Desktop\new_folder\player.png")
player_img = pygame.transform.scale(player_img, (40, 40))

# Demon variables
demon_x = SCREEN_WIDTH - 100
demon_speed = 3
demon_img = pygame.image.load(r"C:\Users\devan\Desktop\new_folder\demon.png")
demon_img = pygame.transform.scale(demon_img, (50, 50))  # Scale to 50x50

# Obstacles
obstacle_img = pygame.image.load(r"C:\Users\devan\Desktop\new_folder\obstacle.png")
obstacle_img = pygame.transform.scale(obstacle_img, (40, 40))  # Scale to 40x40
obstacles = []

# Coins
coin_img = pygame.image.load(r"C:\Users\devan\Desktop\new_folder\coin.png")
coin_img = pygame.transform.scale(coin_img, (20, 20))  # Scale to 20x20
coins = []

# Ground
ground = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)


def update_player():
    """Update player position and handle jumping."""
    global player_y, velocity_y, is_jumping

    # Gravity effect
    velocity_y += gravity
    player_y += velocity_y

    # Jump logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        velocity_y = player_jump
        is_jumping = True

    # Ensure player stays on the ground
    if player_y >= SCREEN_HEIGHT - 100:
        player_y = SCREEN_HEIGHT - 100
        is_jumping = False

    # Draw player
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    screen.blit(player_img, (player_x, player_y))
    return player_rect


def update_demon():
    """Update demon position to chase the player."""
    global demon_x

    demon_x -= demon_speed
    if demon_x <= player_x:
        game_over_display()

    # Draw demon
    screen.blit(demon_img, (demon_x, SCREEN_HEIGHT - 120))


def generate_obstacles():
    """Generate obstacles randomly."""
    if len(obstacles) < 3:
        obstacle_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 500)
        obstacle_y = SCREEN_HEIGHT - 100
        obstacles.append(pygame.Rect(obstacle_x, obstacle_y, 50, 50))


def update_obstacles(player_rect):
    """Update obstacles and check for collisions."""
    global obstacles

    for obstacle in obstacles:
        obstacle.x -= player_speed
        if obstacle.x < 0:
            obstacles.remove(obstacle)

        # Draw obstacle
        screen.blit(obstacle_img, (obstacle.x, obstacle.y))

        # Check collision
        if player_rect.colliderect(obstacle):
            game_over_display()


def generate_coins():
    """Generate coins randomly."""
    if len(coins) < 3:
        coin_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
        coin_y = SCREEN_HEIGHT - 150
        coins.append(pygame.Rect(coin_x, coin_y, 30, 30))


def update_coins(player_rect):
    """Update coins and check for collection."""
    global score, coins

    for coin in coins:
        coin.x -= player_speed
        if coin.x < 0:
            coins.remove(coin)

        # Draw coin
        screen.blit(coin_img, (coin.x, coin.y))

        # Check collection
        if player_rect.colliderect(coin):
            coins.remove(coin)
            score += 1


def draw_score():
    """Display the current score."""
    score_txt = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_txt, (10, 10))


def game_over_display():
    """Display game over screen."""
    global running
    screen.fill((0, 0, 0))
    game_over_txt = font.render("Game Over! Press R to Restart", True, WHITE)
    screen.blit(game_over_txt, (SCREEN_WIDTH // 2 - game_over_txt.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    reset_game()


def reset_game():
    """Reset game variables to restart."""
    global player_y, velocity_y, demon_x, score, obstacles, coins

    player_y = SCREEN_HEIGHT - 100
    velocity_y = 0
    demon_x = SCREEN_WIDTH - 100
    score = 0
    obstacles = []
    coins = []
    game_loop()


def game_loop():
    """Main game loop."""
    global running

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, GROUND_COLOR, ground)

        # Update game elements
        player_rect = update_player()
        update_demon()
        generate_obstacles()
        update_obstacles(player_rect)
        generate_coins()
        update_coins(player_rect)
        draw_score()

        pygame.display.update()
        clock.tick(30)


game_loop()
pygame.quit()