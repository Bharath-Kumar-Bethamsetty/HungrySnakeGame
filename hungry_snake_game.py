import pygame
import sys
import random
import time

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()  # Initialize pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.SysFont('arial', 24)  # Initialize font after pygame.init()
        self.reset_game()

    def reset_game(self):
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.food = self.generate_food()
        self.direction = 'RIGHT'
        self.score = 0
        self.game_over = False  # Track game state

    def generate_food(self):
        while True:
            food = (random.randint(0, SCREEN_WIDTH - 20) // 20 * 20,
                    random.randint(0, SCREEN_HEIGHT - 20) // 20 * 20)
            if food not in self.snake:
                return food

    def draw_score(self):
        score_text = self.score_font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        game_over_text = self.score_font.render('Game Over! Press Space to Restart', True, (255, 255, 255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:  # Only allow restarting if game is over
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                    else:  # Allow direction changes only when the game is active
                        if event.key == pygame.K_UP and self.direction != 'DOWN':
                            self.direction = 'UP'
                        elif event.key == pygame.K_DOWN and self.direction != 'UP':
                            self.direction = 'DOWN'
                        elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                            self.direction = 'LEFT'
                        elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                            self.direction = 'RIGHT'

            if not self.game_over:  # Only move the snake if the game is not over
                # Move Snake
                head = self.snake[-1]
                if self.direction == 'UP':
                    new_head = (head[0], head[1] - 20)
                elif self.direction == 'DOWN':
                    new_head = (head[0], head[1] + 20)
                elif self.direction == 'LEFT':
                    new_head = (head[0] - 20, head[1])
                elif self.direction == 'RIGHT':
                    new_head = (head[0] + 20, head[1])
                self.snake.append(new_head)

                # Check Collision with Food
                if self.snake[-1] == self.food:
                    self.score += 1
                    self.food = self.generate_food()
                else:
                    self.snake.pop(0)

                # Check Collision with Boundary or Self
                if (self.snake[-1][0] < 0 or self.snake[-1][0] >= SCREEN_WIDTH or
                        self.snake[-1][1] < 0 or self.snake[-1][1] >= SCREEN_HEIGHT or
                        self.snake[-1] in self.snake[:-1]):
                    self.game_over = True  # Set game over state

            # Draw Game
            self.screen.fill(BG_COLOR)
            for pos in self.snake:
                pygame.draw.rect(self.screen, SNAKE_COLOR, (pos[0], pos[1], 20, 20))
            pygame.draw.rect(self.screen, FOOD_COLOR, (self.food[0], self.food[1], 20, 20))
            self.draw_score()

            if self.game_over:
                self.draw_game_over()  # Show game over message

            pygame.display.flip()
            self.clock.tick(10)

if __name__ == '__main__':
    game = SnakeGame()
    game.play()
