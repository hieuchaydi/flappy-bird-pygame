import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
PIPE_GAP = 100
PIPE_VELOCITY = -4
GRAVITY = 1
JUMP_VELOCITY = -10

# Load assets
bg = pygame.image.load('assets/bg.png')
birdup = pygame.image.load('assets/birdup.png')
birddown = pygame.image.load('assets/birddown.png')
font = pygame.font.Font('assets/font.ttf', 24)
ground = pygame.image.load('assets/ground.png')
pipedown = pygame.image.load('assets/pipedown.png')
pipeup = pygame.image.load('assets/pipeup.png')

# Initialize sound
pygame.mixer.init()
try:
    sound = pygame.mixer.Sound('assets/source.ogg')
except pygame.error as e:
    print(f"Error loading sound: {e}")

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
pipes = []
score = 0
game_active = False
mute_sound = False

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Functions
def draw_background():
    screen.blit(bg, (0, 0))

def draw_ground():
    screen.blit(ground, (0, SCREEN_HEIGHT - ground.get_height()))

def draw_bird():
    if bird_velocity < 0:
        screen.blit(birdup, (50, bird_y))
    else:
        screen.blit(birddown, (50, bird_y))

def draw_pipes():
    for pipe in pipes:
        screen.blit(pipeup, (pipe['x'], pipe['y']))
        screen.blit(pipedown, (pipe['x'], pipe['y'] + pipeup.get_height() + PIPE_GAP))

def generate_pipe():
    pipe_height = random.randint(50, SCREEN_HEIGHT - ground.get_height() - PIPE_GAP - 50)
    return {'x': SCREEN_WIDTH, 'y': pipe_height - pipeup.get_height(), 'scored': False}

def check_collision():
    bird_rect = pygame.Rect(50, bird_y, birdup.get_width(), birdup.get_height())
    for pipe in pipes:
        upper_pipe_rect = pygame.Rect(pipe['x'], pipe['y'], pipeup.get_width(), pipeup.get_height())
        lower_pipe_rect = pygame.Rect(pipe['x'], pipe['y'] + pipeup.get_height() + PIPE_GAP, pipeup.get_width(), pipedown.get_height())
        if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect):
            return True
    if bird_y + birdup.get_height() >= SCREEN_HEIGHT - ground.get_height():
        return True
    return False

def draw_score():
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

def draw_menu():
    menu_surface = pygame.Surface((150, 100))
    menu_surface.set_alpha(200)
    menu_surface.fill((50, 50, 50))
    screen.blit(menu_surface, (SCREEN_WIDTH - 160, 10))

    play_again_text = font.render("Play Again", True, white)
    mute_sound_text = font.render("Mute Sound" if not mute_sound else "Unmute Sound", True, white)
    quit_text = font.render("Quit", True, white)

    screen.blit(play_again_text, (SCREEN_WIDTH - 150, 20))
    screen.blit(mute_sound_text, (SCREEN_WIDTH - 150, 50))
    screen.blit(quit_text, (SCREEN_WIDTH - 150, 80))

def draw_button(text, color, rect):
    pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, black)
    text_rect = text_surf.get_rect(center=(rect[0] + rect[2] / 2, rect[1] + rect[3] / 2))
    screen.blit(text_surf, text_rect)

def is_button_clicked(rect, pos):
    return pygame.Rect(rect).collidepoint(pos)

def message(text, color, pos):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=pos)
    screen.blit(text_surf, text_rect)

def main_menu():
    menu = True
    while menu:
        draw_background()
        draw_button("Start Game", white, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100, 200, 50])
        draw_button("View Score", white, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 30, 200, 50])
        draw_button("Quit", white, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 40, 200, 50])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if is_button_clicked([SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100, 200, 50], pos):
                    gameLoop()
                elif is_button_clicked([SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 30, 200, 50], pos):
                    draw_background()
                    message("Score: Not Implemented", white, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2])
                    pygame.display.update()
                    time.sleep(2)
                elif is_button_clicked([SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 40, 200, 50], pos):
                    pygame.quit()
                    quit()

def gameLoop():
    global bird_y, bird_velocity, pipes, score, game_active, mute_sound
    game_over = False
    game_close = False

    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_active = True

    while not game_over:
        while game_close:
            draw_background()
            draw_button("Restart", white, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 50, 200, 50])
            draw_button("Quit", white, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 20, 200, 50])
            message("Game Over!", red, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if is_button_clicked([SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 50, 200, 50], pos):
                        gameLoop()  # Restart the game
                    elif is_button_clicked([SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 20, 200, 50], pos):
                        pygame.quit()
                        quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_velocity = JUMP_VELOCITY

        if bird_y >= SCREEN_HEIGHT or bird_y < 0:
            game_close = True

        bird_velocity += GRAVITY
        bird_y += bird_velocity

        if check_collision():
            game_active = False
            game_close = True

        if len(pipes) == 0 or pipes[-1]['x'] < SCREEN_WIDTH - 150:
            pipes.append(generate_pipe())

        for pipe in pipes:
            pipe['x'] += PIPE_VELOCITY

        pipes = [pipe for pipe in pipes if pipe['x'] > -pipeup.get_width()]

        for pipe in pipes:
            # Chỉ tăng điểm khi bird vượt qua mép phải của ống
            if pipe['x'] + pipeup.get_width() < 50 and not pipe['scored']:
                score += 1
                pipe['scored'] = True
                if not mute_sound:
                    try:
                        sound.play()
                    except pygame.error as e:
                        print(f"Error playing sound: {e}")

        draw_background()
        draw_pipes()
        draw_bird()
        draw_ground()
        draw_score()

        pygame.display.update()
        pygame.time.Clock().tick(30)

    pygame.quit()
    quit()

main_menu()
