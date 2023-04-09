import pygame
import pygame.surfarray as surfarray
from pygame.locals import *
import numpy as np
import io
import base64
import html
import os



pygame.init()

# Set up the game window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
# Set up the game window
WINDOW_FLAGS = pygame.NOFRAME
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)


# Set up the paddles and ball
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
PADDLE_SPEED = 5
BALL_RADIUS = 5
BALL_SPEED = 5

PLAYER1_SCORE = 0
PLAYER2_SCORE = 0

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the fonts
FONT = pygame.font.Font(None, 36)

# Function to draw the ball
def draw_ball(ball_x, ball_y):
    pygame.draw.circle(WINDOW, WHITE, (ball_x, ball_y), BALL_RADIUS)

# Function to draw the paddles
def draw_paddle(paddle_x, paddle_y):
    pygame.draw.rect(WINDOW, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Function to update the ball position
def update_ball(ball_x, ball_y, ball_dx, ball_dy):
    ball_x += ball_dx
    ball_y += ball_dy

    # Check for collision with the top or bottom of the window
    if ball_y - BALL_RADIUS < 0 or ball_y + BALL_RADIUS > WINDOW_HEIGHT:
        ball_dy *= -1

    return ball_x, ball_y, ball_dx, ball_dy

# Function to check for collision with a paddle
def check_collision(ball_x, ball_y, ball_dx, ball_dy, paddle_x, paddle_y):
    # Check for collision with the left or right of the paddle
    if (ball_x - BALL_RADIUS <= paddle_x + PADDLE_WIDTH and
            ball_x + BALL_RADIUS >= paddle_x and
            ball_y + BALL_RADIUS >= paddle_y and
            ball_y - BALL_RADIUS <= paddle_y + PADDLE_HEIGHT):
        ball_dx *= -1
        return ball_dx, ball_dy

    return ball_dx, ball_dy

# Function to update the player scores
def update_scores(ball_x):
    global PLAYER1_SCORE, PLAYER2_SCORE

    # Check if the ball went out of bounds on the left or right
    if ball_x - BALL_RADIUS < 0:
        PLAYER2_SCORE += 1
        return True
    elif ball_x + BALL_RADIUS > WINDOW_WIDTH:
        PLAYER1_SCORE += 1
        return True

    return False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Get the current state of the keyboard
    keys = pygame.key.get_pressed()

    # Update the player paddles
    if keys[K_w] and paddle1_y > 0:
        paddle1_y -= PADDLE_SPEED
    elif keys[K_s] and paddle1_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
        paddle1_y += PADDLE_SPEED

    if keys[K_UP] and paddle2_y > 0:
        paddle2_y -= PADDLE_SPEED
    elif keys[K_DOWN] and paddle2_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
        paddle2_y += PADDLE_SPEED

    # Update the ball position
    ball_x, ball_y, ball_dx, ball_dy = update_ball(ball_x, ball_y, ball_dx, ball_dy)

    # Check for collision with the paddles
    ball_dx, ball_dy = check_collision(ball_x, ball_y, ball_dx, ball_dy, paddle1_x, paddle1_y)
    ball_dx, ball_dy = check_collision(ball_x, ball_y, ball_dx, ball_dy, paddle2_x, paddle2_y)

    # Update the player scores if the ball goes out of bounds
    if update_scores(ball_x):
        ball_x, ball_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        ball_dx, ball_dy = -ball_dx, -ball_dy

    # Draw the game objects
    WINDOW.fill(BLACK)
    draw_paddle(paddle1_x, paddle1_y)
    draw_paddle(paddle2_x, paddle2_y)
    draw_ball(ball_x, ball_y)
    draw_scores()

    # Update the display
    pygame.display.update()

    # Wait for a short time
    CLOCK.tick(60)
