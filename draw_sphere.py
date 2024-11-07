import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Road Game")

# Colors
BACKGROUND_COLOR = (50, 50, 50)
ROAD_COLOR = (80, 80, 80)
SPHERE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (200, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Sphere properties
sphere_radius = 20
sphere_x, sphere_y = WIDTH // 2, HEIGHT - 100  # Start at bottom center
sphere_speed = 5

# Obstacle properties
obstacle_width, obstacle_height = 60, 40
obstacles = []  # List to store active obstacles
obstacle_speed = 5
obstacle_spawn_rate = 25  # Frames between new obstacles

# Explosion effect
explosion_radius = 0
explosion_growing = False

# Font for "Game Over" and score
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)
game_over_text = font_large.render("Game Over", True, TEXT_COLOR)

# Game state
game_over = False
score = 0
frames_since_last_obstacle = 0


def draw_sphere(x, y, radius):
    # Draw a simple sphere with a gradient effect
    for i in range(radius, 0, -1):
        color = (int(255 * (1 - i / radius)), int(255 * (1 - i / radius)), int(255 * (1 - i / radius)))
        pygame.draw.circle(screen, color, (int(x), int(y)), i)


def draw_road():
    # Draw the road with lanes
    pygame.draw.rect(screen, ROAD_COLOR, (WIDTH // 3, 0, WIDTH // 3, HEIGHT))
    pygame.draw.line(screen, (255, 255, 255), (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(screen, (255, 255, 255), (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), 5)


def spawn_obstacle():
    # Spawn an obstacle at a random position in the road lane
    lane_x = random.choice([WIDTH // 3 + obstacle_width, 2 * WIDTH // 3 - obstacle_width])
    obstacles.append([lane_x, -obstacle_height])  # Position off-screen at top


def move_obstacles():
    global score, obstacles
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed  # Move down by obstacle_speed

    # Remove obstacles that have left the screen
    obstacles = [obs for obs in obstacles if obs[1] < HEIGHT]

    # Increment score for each obstacle passed
    for obstacle in obstacles:
        if obstacle[1] > sphere_y + sphere_radius and not game_over:
            score += 1


def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, (*obstacle, obstacle_width, obstacle_height))


def detect_collision():
    global game_over, explosion_growing
    sphere_rect = pygame.Rect(sphere_x - sphere_radius, sphere_y - sphere_radius, sphere_radius * 2, sphere_radius * 2)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if sphere_rect.colliderect(obstacle_rect):
            game_over = True
            explosion_growing = True  # Start explosion animation
            return


def explode():
    global explosion_radius, explosion_growing
    if explosion_growing:
        explosion_radius += 5
        if explosion_radius > 100:  # End explosion after reaching a certain radius
            explosion_growing = False
        pygame.draw.circle(screen, (255, 100, 100), (sphere_x, sphere_y), explosion_radius)


def draw_score():
    score_text = font_small.render("Score: " + str(score), True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))


# Main game loop
clock = pygame.time.Clock()
while True:
    screen.fill(BACKGROUND_COLOR)
    draw_road()

    if game_over:
        explode()
        screen.blit(game_over_text,
                    (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and sphere_x > WIDTH // 3 + sphere_radius:
            sphere_x -= sphere_speed
        if keys[pygame.K_RIGHT] and sphere_x < 2 * WIDTH // 3 - sphere_radius:
            sphere_x += sphere_speed
        if keys[pygame.K_UP] and sphere_y > sphere_radius:
            sphere_y -= sphere_speed
        if keys[pygame.K_DOWN] and sphere_y < HEIGHT - sphere_radius:
            sphere_y += sphere_speed

        draw_sphere(sphere_x, sphere_y, sphere_radius)

        # Spawn new obstacles periodically
        frames_since_last_obstacle += 1
        if frames_since_last_obstacle >= obstacle_spawn_rate:
            spawn_obstacle()
            frames_since_last_obstacle = 0

        move_obstacles()
        draw_obstacles()
        detect_collision()
        draw_score()

    pygame.display.flip()
    clock.tick(30)

    # Handle quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()