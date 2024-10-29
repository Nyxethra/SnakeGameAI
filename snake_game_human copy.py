import pygame
import random
from enum import Enum
from collections import namedtuple
import time
 
pygame.init()
font = pygame.font.Font('arial.ttf', 25)
# font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE2 = (0, 100, 255)

BLOCK_SIZE = 20
SPEED = 8

class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('g.png')

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

        # Thêm bộ đếm thời gian thay đổi màu
        self.last_color_change_time = time.time()
        self.snake_colors = [self._get_random_color() for _ in self.snake]

    def _get_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. thu thập đầu vào từ người dùng
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. di chuyển
        self._move(self.direction)  # cập nhật vị trí đầu rắn
        self.snake.insert(0, self.head)
        self.snake_colors.insert(0, self._get_random_color())  # Thêm màu cho đốt mới

        # 3. kiểm tra nếu game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. đặt thức ăn mới hoặc chỉ di chuyển
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
            self.snake_colors.pop()

        # 5. cập nhật giao diện người dùng và đồng hồ
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. trả về game over và điểm số
        return game_over, self.score

    def _is_collision(self):
        # chạm biên
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # chạm chính nó
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.blit(self.background, (0, 0))

        # Kiểm tra nếu đến thời điểm thay đổi màu sắc
        current_time = time.time()
        if current_time - self.last_color_change_time > 1.5:
            self.snake_colors = [self._get_random_color() for _ in self.snake]
            self.last_color_change_time = current_time

        for idx, pt in enumerate(self.snake):
            color = self.snake_colors[idx]
            pygame.draw.rect(self.display, color, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    # vòng lặp game
    while True:
        game_over, score = game.play_step()

        if game_over:
            break

    print('Final Score', score)

    pygame.quit()
