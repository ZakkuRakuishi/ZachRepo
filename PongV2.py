import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 400
BACKGROUND_COLOR = (0, 0, 0)
PADDLE_COLOR = (255, 255, 255)
BALL_COLOR = (255, 255, 255)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
BALL_WIDTH, BALL_HEIGHT = 10, 10
PADDLE_VELOCITY = 5
LEFT_PADDLE_POSITION = 30
RIGHT_PADDLE_POSITION = WIDTH - 30 - PADDLE_WIDTH

# Initialize Pygame
pygame.init()

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Fonts
font = pygame.font.Font(None, 36)

# Paddle and ball objects
left_paddle = pygame.Rect(LEFT_PADDLE_POSITION, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(RIGHT_PADDLE_POSITION, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_WIDTH // 2, HEIGHT // 2 - BALL_HEIGHT // 2, BALL_WIDTH, BALL_HEIGHT)

# Ball movement
ball_speed_x = 3
ball_speed_y = 3

# Score
left_score = 0
right_score = 0

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        new_line = current_line + " " + word
        if font.size(new_line)[0] <= max_width:
            current_line = new_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return lines

def update_paddle(paddle, dy):
    if paddle.top + dy < 0 or paddle.bottom + dy > HEIGHT:
        return
    paddle.move_ip(0, dy)

def update_right_paddle():
    if right_paddle.centery < ball.centery:
        update_paddle(right_paddle, 3)
    elif right_paddle.centery > ball.centery:
        update_paddle(right_paddle, -3)

def update_left_paddle():
    if left_paddle.centery < ball.centery:
        update_paddle(left_paddle, 3)
    elif left_paddle.centery > ball.centery:
        update_paddle(left_paddle, -3)

def update_ball():
    global ball_speed_x, ball_speed_y, left_score, right_score

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x = -ball_speed_x

    # Ball out of bounds
    if ball.left <= 0:
        right_score += 1
        ball.x, ball.y = WIDTH // 2 - BALL_WIDTH // 2, HEIGHT // 2 - BALL_HEIGHT // 2
        ball_speed_x = -ball_speed_x
    elif ball.right >= WIDTH:
        left_score += 1
        ball.x
        ball.x, ball.y = WIDTH // 2 - BALL_WIDTH // 2, HEIGHT // 2 - BALL_HEIGHT // 2
        ball_speed_x = -ball_speed_x

def draw_elements():
    screen.fill(BACKGROUND_COLOR)

    # Draw the paddles
    pygame.draw.rect(screen, PADDLE_COLOR, left_paddle)
    pygame.draw.rect(screen, PADDLE_COLOR, right_paddle)

    # Draw the ball
    pygame.draw.ellipse(screen, BALL_COLOR, ball)

    # Draw the middle line
    pygame.draw.line(screen, PADDLE_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

    # Draw the scores
    left_score_text = font.render(str(left_score), True, PADDLE_COLOR)
    right_score_text = font.render(str(right_score), True, PADDLE_COLOR)
    screen.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 10))
    screen.blit(right_score_text, (WIDTH * 3 // 4 - right_score_text.get_width() // 2, 10))

    pygame.display.flip()

def pre_game_screen():
    pre_game = True
    while pre_game:
        screen.fill(BACKGROUND_COLOR)
        welcome_text_lines = wrap_text("Press NumKey 1 to be left side or Press NumKey 2 to be right side", font, WIDTH - 20)
        for i, line in enumerate(welcome_text_lines):
            welcome_text = font.render(line, True, PADDLE_COLOR)
            screen.blit(welcome_text, (WIDTH // 2 - welcome_text.get_width() // 2, HEIGHT // 2 - welcome_text.get_height() // 2 + i * (font.get_height() + 5)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pre_game = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP1:
                    return True
                elif event.key == pygame.K_KP2:
                    return False

player_is_left = pre_game_screen()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if player_is_left:
        if keys[pygame.K_w]:
            update_paddle(left_paddle, -PADDLE_VELOCITY)
        if keys[pygame.K_s]:
            update_paddle(left_paddle, PADDLE_VELOCITY)
        update_right_paddle()
    else:
        if keys[pygame.K_w]:
            update_paddle(right_paddle, -PADDLE_VELOCITY)
        if keys[pygame.K_s]:
            update_paddle(right_paddle, PADDLE_VELOCITY)
        update_left_paddle()

    update_ball()
    draw_elements()
    pygame.time.delay(16)
