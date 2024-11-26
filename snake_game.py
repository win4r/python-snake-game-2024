import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_SIZE = (400, 400)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Snake Game')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Snake properties
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# Initialize font
font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.x = WINDOW_SIZE[0] // 2
        self.y = WINDOW_SIZE[1] // 2
        self.dx = SNAKE_BLOCK
        self.dy = 0
        self.body = [(self.x, self.y)]
        self.score = 0

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.body.insert(0, (self.x, self.y))
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])
        self.score += 10

    def check_collision(self):
        # Check wall collision
        if (self.x < 0 or self.x >= WINDOW_SIZE[0] or
            self.y < 0 or self.y >= WINDOW_SIZE[1]):
            return True
        # Check self collision
        if (self.x, self.y) in self.body[1:]:
            return True
        return False

def show_score(score):
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def show_game_over(final_score):
    game_over_text = font.render('Game Over!', True, RED)
    score_text = font.render(f'Final Score: {final_score}', True, WHITE)
    screen.blit(game_over_text, (WINDOW_SIZE[0]//2 - 100, WINDOW_SIZE[1]//2 - 50))
    screen.blit(score_text, (WINDOW_SIZE[0]//2 - 100, WINDOW_SIZE[1]//2 + 10))
    pygame.display.flip()
    pygame.time.wait(2000)

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = (random.randrange(0, WINDOW_SIZE[0], SNAKE_BLOCK),
            random.randrange(0, WINDOW_SIZE[1], SNAKE_BLOCK))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.dy == 0:
                    snake.dx = 0
                    snake.dy = -SNAKE_BLOCK
                elif event.key == pygame.K_DOWN and snake.dy == 0:
                    snake.dx = 0
                    snake.dy = SNAKE_BLOCK
                elif event.key == pygame.K_LEFT and snake.dx == 0:
                    snake.dx = -SNAKE_BLOCK
                    snake.dy = 0
                elif event.key == pygame.K_RIGHT and snake.dx == 0:
                    snake.dx = SNAKE_BLOCK
                    snake.dy = 0

        snake.move()

        # Check for food collision
        if snake.x == food[0] and snake.y == food[1]:
            snake.grow()
            food = (random.randrange(0, WINDOW_SIZE[0], SNAKE_BLOCK),
                   random.randrange(0, WINDOW_SIZE[1], SNAKE_BLOCK))

        # Check for game over
        if snake.check_collision():
            show_game_over(snake.score)
            running = False

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, (food[0], food[1], SNAKE_BLOCK, SNAKE_BLOCK))
        
        # Draw snake with gradient color
        for i, segment in enumerate(snake.body):
            color_value = 255 - (i * (255 // (len(snake.body) + 1)))
            color = (0, color_value, 0)
            pygame.draw.rect(screen, color, (segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK))
        
        show_score(snake.score)
        pygame.display.flip()

        clock.tick(SNAKE_SPEED)

    pygame.quit()

if __name__ == '__main__':
    main()