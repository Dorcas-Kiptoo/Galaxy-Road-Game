
import pygame
import sys
import random

# Initialize Pygame and the mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Road Game")

# Colors
ROAD_COLOR = (60, 60, 70)
TEXT_COLOR = (255, 255, 255)

# Sphere properties
sphere_radius = 20
sphere_x, sphere_y = WIDTH // 2, HEIGHT - 100
sphere_speed = 5

# Obstacle properties
obstacle_width, obstacle_height = 60, 40
obstacles = []
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
highest_score = 0  # Initialize highest score
frames_since_last_obstacle = 0

# Background Star positions for galaxy effect
star_positions = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

# Load skull image for obstacles
skull_image = pygame.image.load("skull.png")
skull_image = pygame.transform.scale(skull_image, (obstacle_width, obstacle_height))

# Define lanes for balanced obstacle positioning
lane_width = WIDTH // 3  # Width of each lane
road_start_x = WIDTH // 3  # Start of the road section
lane_positions = [
    road_start_x + lane_width // 6 - obstacle_width // 2,  # Left lane
    road_start_x + lane_width // 2 - obstacle_width // 2,  # Center lane
    road_start_x + 5 * lane_width // 6 - obstacle_width // 2  # Right lane
]

# Load sounds
background_music = r"C:\Users\Admin\Downloads\music.mp3"
explosion_sound = pygame.mixer.Sound(r"C:\Users\Admin\Downloads\explosion.wav")
game_over_sound = pygame.mixer.Sound(r"C:\Users\Admin\Downloads\game_over.mp3")

# Play background music (looping)
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # Loop indefinitely


# Function to reset the game state
def reset_game():
    global sphere_x, sphere_y, obstacles, score, game_over, explosion_radius, explosion_growing, collision_detected, game_over_sound_played
    sphere_x, sphere_y = WIDTH // 2, HEIGHT - 100
    obstacles = []
    score = 0
    game_over = False
    explosion_radius = 0
    explosion_growing = False
    collision_detected = False
    game_over_sound_played = False
    pygame.mixer.music.play(-1)  # Restart background music


# Function to update the highest score if needed
def update_highest_score():
    global highest_score
    if score > highest_score:
        highest_score = score


# Function to display Game Over screen with score, highest score, and Play Again button
def show_game_over_screen():
    global game_over_sound_played
    update_highest_score()  # Update highest score on game over

    # Game Over text
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    score_text = font_small.render(f"Your Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

    # highest score
    highest_score_text = font_small.render(f"Highest Score: {highest_score}", True, TEXT_COLOR)
    screen.blit(highest_score_text, (WIDTH // 2 - highest_score_text.get_width() // 2, HEIGHT // 2 + 40))

    #Play Again button
    play_again_text = font_small.render("Play Again", True, TEXT_COLOR)
    play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    pygame.draw.rect(screen, (0, 150, 0), play_again_rect.inflate(20, 10))
    screen.blit(play_again_text, play_again_rect)

    # Check for mouse click on Play Again button
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if play_again_rect.collidepoint(mouse_pos) and mouse_click[0]:
        reset_game()


def draw_background():
    for i in range(HEIGHT):
        gradient_color = (
            max(10, 30 + i // 10),
            max(10, 20 + i // 20),
            max(20, 50 + i // 15)
        )
        pygame.draw.line(screen, gradient_color, (0, i), (WIDTH, i))
    for pos in star_positions:
        pygame.draw.circle(screen, (255, 255, 255), pos, random.choice([1, 2]))


def draw_sphere(x, y, radius):
    for i in range(radius, 0, -2):
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
        color = (255 - int(i * 2.5), 255 - int(i * 2.5), 255 - int(i * 2.5))
        pygame.draw.circle(screen, color, (x + offset_x, y + offset_y), i)


def draw_road():
    pygame.draw.rect(screen, ROAD_COLOR, (WIDTH // 3 - 10, 0, WIDTH // 3 + 20, HEIGHT))
    pygame.draw.line(screen, (255, 255, 255), (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(screen, (255, 255, 255), (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), 5)


def spawn_obstacle():
    lane_x = random.choice(lane_positions)
    obstacles.append([lane_x, -obstacle_height])


def move_obstacles():
    global score, obstacles
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed
    obstacles = [obs for obs in obstacles if obs[1] < HEIGHT]
    for obstacle in obstacles:
        if obstacle[1] > sphere_y + sphere_radius and not game_over:
            score += 1


def draw_obstacles():
    for obstacle in obstacles:
        screen.blit(skull_image, (obstacle[0], obstacle[1]))


collision_detected = False


def detect_collision():
    global game_over, explosion_growing, collision_detected
    sphere_rect = pygame.Rect(sphere_x - sphere_radius, sphere_y - sphere_radius, sphere_radius * 2, sphere_radius * 2)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if sphere_rect.colliderect(obstacle_rect):
            game_over = True
            explosion_growing = True
            if not collision_detected:
                explosion_sound.play()
                collision_detected = True
            return


def explode():
    global explosion_radius, explosion_growing
    if explosion_growing:
        explosion_radius += 5
        if explosion_radius > 100:
            explosion_growing = False
        pygame.draw.circle(screen, (255, 100, 100), (sphere_x, sphere_y), explosion_radius)



font_score = pygame.font.Font(None, 28)  # Smaller font size for compact score display

def draw_score():

    score_text = font_score.render("Score: " + str(score).zfill(6), True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

    highest_score_text = font_score.render("Highest: " + str(highest_score).zfill(6), True, TEXT_COLOR)
    screen.blit(highest_score_text, (10, 50)) 



# Main game loop
game_over_sound_played = False
clock = pygame.time.Clock()
while True:
    draw_background()
    draw_road()

    if game_over:
        pygame.mixer.music.stop()
        if not game_over_sound_played:
            game_over_sound.play()
            game_over_sound_played = True
        explode()
        show_game_over_screen()  # Show Game Over screen with Play Again button
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
