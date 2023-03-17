import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60

# Create the paddles and ball
left_paddle = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 10, 10)

# Ball speed
ball_speed = [3, 3]

def draw_elements():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.rect(screen, WHITE, ball)

def update_ball():
    global ball_speed
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]
    
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] = -ball_speed[0]
    
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2

def update_paddle(paddle, dy):
    paddle.y += dy
    paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, paddle.y))

def update_right_paddle():
    if right_paddle.centery < ball.centery:
        update_paddle(right_paddle, 3)
    elif right_paddle.centery > ball.centery:
        update_paddle(right_paddle, -3)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        update_paddle(left_paddle, -5)
    if keys[pygame.K_s]:
        update_paddle(left_paddle, 5)

    update_ball()
    update_right_paddle()
    draw_elements()
    pygame.display.flip()
    clock.tick(60)