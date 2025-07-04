from random import choice
from game_settings import *  # Тут такой импорт оправдан.


# Тут описываем все классы игры.
class GameObject:
    def __init__(self):
        self.position = SCREEN_CENTER
        self.body_color = None

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR

    # Задает случайное положение яблока на игровом поле.
    def randomize_position(self):
        self.position = (choice(range(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)),
                         choice(range(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)))

    # Отрисовка яблока на экране.
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    # Отрисовка змейки на экране.
    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    # Определение позиции головы змейки.
    def get_head_position(self):
        return self.positions[0]

    # Описание движения змейки.
    def move(self):
        self.position = (self.position[0] + self.direction[0] * GRID_SIZE, self.position[1] +
                         self.direction[1] * GRID_SIZE)
        # Телепортация при пересечении границ игрового поля.
        if self.position[0] < 0:
            self.position = (SCREEN_WIDTH - GRID_SIZE, self.position[1])
        elif self.position[0] > SCREEN_WIDTH - GRID_SIZE:
            self.position = (0, self.position[1])
        elif self.position[1] < 0:
            self.position = (self.position[0], SCREEN_HEIGHT - GRID_SIZE)
        elif self.position[1] > SCREEN_HEIGHT - GRID_SIZE:
            self.position = (self.position[0], 0)

        self.positions.insert(0, self.position)
        # Определение последнего элемента для затирания и удаление его из списка.
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    # Обработка изменения направления движения.
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Обнуление змейки при столкновении с собой.
    def reset(self):
        for item in self.positions:
            last_rect = pygame.Rect(item, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.length = 1
        self.position = SCREEN_CENTER
        self.positions = [self.position]
        self.direction = RIGHT

    # Обработка столкновения змейки с собой.
    def handle_collisions(self):
        if self.get_head_position() in self.positions[1:]:
            self.reset()


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Проверка, что рандомно выбранная позиция яблока не попала на змейку.
# Выбор новой позиции, если попала.
def check_apple_position(apple, snake):
    while apple.position in snake.positions:
        apple.randomize_position()


# Обработка события поедания яблока.
def eat_an_apple(apple, snake):
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize_position()
        check_apple_position(apple, snake)


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут создаем экземпляры классов.
    apple = Apple()
    snake = Snake()
    # Выбираем случайную позицию яблока.
    apple.randomize_position()
    # Проверяем, что яблоко не попало на змейку.
    check_apple_position(apple, snake)

    # Запускаем основной цикл игры.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        eat_an_apple(apple, snake)
        snake.handle_collisions()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
