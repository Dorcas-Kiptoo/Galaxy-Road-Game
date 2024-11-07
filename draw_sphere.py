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
ROAD_COLOR = (80, 80, 80)
SPHERE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (200, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Sphere properties
sphere_radius = 20
sphere_x, sphere_y = WIDTH // 2, HEIGHT - 100
sphere_speed = 5

# Obstacle properties
obstacle_width, obstacle_height = 60, 40
obstacles = []
obstacle_speed = 5
obstacle_spawn_rate = 25

# Explosion effect
explosion_radius = 0
explosion_growing = False

# Fonts
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)
game_over_text = font_large.render("Game Over", True, TEXT_COLOR)

# Game state
game_over = False
score = 0
frames_since_last_obstacle = 0

# Day-Night Cycle
time_of_day = 0
day_night_speed = 0.0005
sun_position = [WIDTH // 2, HEIGHT // 4]
moon_position = [WIDTH // 2, HEIGHT // 4]
star_positions = [(random.randint(0, WIDTH), random.randint(0, HEIGHT // 2)) for _ in range(50)]

def draw_background():
    global time_of_day
    day_color = (255, 153, 51)
    night_color = (10, 10, 50)
    blended_color = [int(day_color[i] * (1 - time_of_day) + night_color[i] * time_of_day) for i in range(3)]
    screen.fill(blended_color)
    time_of_day += day_night_speed
    if time_of_day > 1:
        time_of_day = 0

def draw_sun_and_moon():
    sun_y = int((1 - time_of_day) * HEIGHT // 4) + 50
    moon_y = int(time_of_day * HEIGHT // 4) + 50
    if time_of_day < 0.5:
        pygame.draw.circle(screen, (255, 204, 0), (sun_position[0], sun_y), 30)
    if time_of_day > 0.5:
        pygame.draw.circle(screen, (200, 200, 255), (moon_position[0], moon_y), 25)

def draw_stars():
    if time_of_day > 0.5:
        for pos in star_positions:
            pygame.draw.circle(screen, (255, 255, 255), pos, 2)

def draw_sphere(x, y, radius):
    for i in range(radius, 0, -1):
        color = (int(255 * (1 - i / radius)),) * 3
        pygame.draw.circle(screen, color, (int(x), int(y)), i)

def draw_road():
    pygame.draw.rect(screen, ROAD_COLOR, (WIDTH // 3, 0, WIDTH // 3, HEIGHT))
    pygame.draw.line(screen, (255, 255, 255), (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(screen, (255, 255, 255), (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), 5)

def spawn_obstacle():
    lane_x = random.choice([WIDTH // 3 + obstacle_width, 2 * WIDTH // 3 - obstacle_width])
    obstacles.append([lane_x, -obstacle_height])

def move_obstacles():
    global score
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed
    obstacles[:] = [obs for obs in obstacles if obs[1] < HEIGHT]
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
            explosion_growing = True
            return

def explode():
    global explosion_radius, explosion_growing
    if explosion_growing:
        explosion_radius += 5
        if explosion_radius > 100:
            explosion_growing = False
        pygame.draw.circle(screen, (255, 100, 100), (sphere_x, sphere_y), explosion_radius)

def draw_score():
    score_text = font_small.render("Score: " + str(score), True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

# Main game loop
clock = pygame.time.Clock()
while True:
    draw_background()
    draw_sun_and_moon()
    draw_stars()
    draw_road()
    
    if game_over:
        explode()
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
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
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
