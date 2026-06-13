import pygame
import sys
import random
import json
import os
from enum import Enum

pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 7

# Colors
WHITE = (255, 255, 255)   
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
DARK_GREEN = (0, 128, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
GOLD = (255, 215, 0)

# Fonts
SMALL_FONT = pygame.font.SysFont('Arial', 20)
MEDIUM_FONT = pygame.font.SysFont('Arial', 30, bold=True)
LARGE_FONT = pygame.font.SysFont('Arial', 50, bold=True)
TITLE_FONT = pygame.font.SysFont('Arial', 60, bold=True)

# Game states
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('🐍 SNAKE GAME 🐍')
clock = pygame.time.Clock()

# High score file
HIGH_SCORE_FILE = 'highscore.json'

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except:
            return 0
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        json.dump({'high_score': score}, f)
class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, -CELL_SIZE)
        self.next_direction = (0, -CELL_SIZE)
    
    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body = [new_head] + self.body[:-1]
    
    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)
    
    def change_direction(self, new_direction):
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.next_direction = new_direction
    
    def check_collision(self):
        head = self.body[0]
        if head in self.body[1:]:
            return True
        if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
            return True
        return False
    
    def reset(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, -CELL_SIZE)
        self.next_direction = (0, -CELL_SIZE)
class Food:
    def __init__(self):
        self.position = self.random_position()
    
    def random_position(self):
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        return (x, y)
    def respawn(self):
        self.position = self.random_position()
def draw_snake(snake):
    for i, segment in enumerate(snake.body):
        if i == 0:  # Head
            pygame.draw.rect(screen, DARK_GREEN, (*segment, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE), 2)
        else:  # Body
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, DARK_GREEN, (*segment, CELL_SIZE, CELL_SIZE), 1)

def draw_food(food):
    pygame.draw.rect(screen, RED, (*food.position, CELL_SIZE, CELL_SIZE))
    pygame.draw.circle(screen, GOLD, (food.position[0] + CELL_SIZE // 2, food.position[1] + CELL_SIZE // 2), CELL_SIZE // 3)

def draw_menu(high_score):
    screen.fill(BLACK)
    title = TITLE_FONT.render('🐍 SNAKE GAME 🐍', True, GREEN)
    title_rect = title.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title, title_rect)
    
    start_text = LARGE_FONT.render('PRESS SPACE TO START', True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, 250))
    screen.blit(start_text, start_rect)
    
    instructions = [
        'CONTROLS:',
        '↑ UP / ↓ DOWN / ← LEFT / → RIGHT - Move Snake',
        'P - Pause/Resume',
        'R - Restart (During Game Over)',
    ]
    
    y = 350
    for instruction in instructions:
        text = SMALL_FONT.render(instruction, True, LIGHT_GRAY)
        screen.blit(text, (50, y))
        y += 30
    
    high_score_text = MEDIUM_FONT.render(f'High Score: {high_score}', True, GOLD)
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, 550))
    screen.blit(high_score_text, high_score_rect)

def draw_pause_screen(score, high_score):
    pause_text = LARGE_FONT.render('PAUSED', True, WHITE)
    pause_rect = pause_text.get_rect(center=(WIDTH // 2, 250))
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(100)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    screen.blit(pause_text, pause_rect)
    
    resume_text = MEDIUM_FONT.render('Press P to Resume', True, GREEN)
    resume_rect = resume_text.get_rect(center=(WIDTH // 2, 350))
    screen.blit(resume_text, resume_rect)

def draw_game_over_screen(score, high_score):
    screen.fill(BLACK)
    
    game_over_text = TITLE_FONT.render('GAME OVER', True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(game_over_text, game_over_rect)
    
    score_text = LARGE_FONT.render(f'Score: {score}', True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 200))
    screen.blit(score_text, score_rect)
    
    if score == high_score and score > 0:
        new_high_text = MEDIUM_FONT.render('🎉 NEW HIGH SCORE! 🎉', True, GOLD)
        new_high_rect = new_high_text.get_rect(center=(WIDTH // 2, 270))
        screen.blit(new_high_text, new_high_rect)
    
    high_score_text = MEDIUM_FONT.render(f'High Score: {high_score}', True, GOLD)
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, 320))
    screen.blit(high_score_text, high_score_rect)
    
    restart_text = MEDIUM_FONT.render('Press R to Restart or Q to Quit', True, GREEN)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, 420))
    screen.blit(restart_text, restart_rect)

def draw_game_screen(snake, food, score, high_score):
    screen.fill(BLACK)
    draw_snake(snake)
    draw_food(food)
    
    score_text = MEDIUM_FONT.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    
    high_score_text = MEDIUM_FONT.render(f'High Score: {high_score}', True, GOLD)
    high_score_rect = high_score_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(high_score_text, high_score_rect)

def main():
    game_state = GameState.MENU
    snake = Snake()
    food = Food()
    score = 0
    high_score = load_high_score()
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        game_state = GameState.PLAYING
                        snake.reset()
                        food.respawn()
                        score = 0
                
                elif game_state == GameState.PLAYING:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -CELL_SIZE))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, CELL_SIZE))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-CELL_SIZE, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((CELL_SIZE, 0))
                    elif event.key == pygame.K_p:
                        game_state = GameState.PAUSED
                
                elif game_state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        game_state = GameState.PLAYING
                
                elif game_state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        game_state = GameState.MENU
                    elif event.key == pygame.K_q:
                        running = False
        
        # Game logic
        if game_state == GameState.PLAYING:
            snake.move()
            
            if snake.check_collision():
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                game_state = GameState.GAME_OVER
            
            if snake.body[0] == food.position:
                snake.grow()
                food.respawn()
                score += 1
        
        # Drawing
        if game_state == GameState.MENU:
            draw_menu(high_score)
        elif game_state == GameState.PLAYING:
            draw_game_screen(snake, food, score, high_score)
        elif game_state == GameState.PAUSED:
            draw_game_screen(snake, food, score, high_score)
            draw_pause_screen(score, high_score)
        elif game_state == GameState.GAME_OVER:
            draw_game_over_screen(score, high_score)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
    