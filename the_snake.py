from random import choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут описываем все классы игры.
class GameObject:
    """
    Базовый класс для всех игровых объектов.
    Атрибуты:
        position (tuple): Текущие координаты объекта на экране.
        body_color (tuple): Цвет заполнения объекта.
    """

    def __init__(self, body_color=None):
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        """
        В случае отсутствия переопределения метода отрисовки возбуждается
        исключение. Метод обязательно должен быть переопределён в потомках.
        """
        raise NotImplementedError(f'Метод draw не определен в классе'
                                  f' {self.__class__.__name__}')


class Apple(GameObject):
    """
    Яблоко в игре «Змейка».
    Наследуется от GameObject и отвечает за
    случайное размещение и отрисовку яблока.
    """

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)

    # Задает случайное положение яблока на игровом поле.
    def randomize_position(self):
        """
        Устанавливает случайную позицию яблока
        так, чтобы его координаты были кратны сетке.
        """
        self.position = (
            choice(range(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)),
            choice(range(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE))
        )

    # Отрисовка яблока на экране.
    def draw(self):
        """
        Рисует яблоко: прямоугольник, заполненный указанным цветом
        и рамку вокруг него.
        """
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс Змейка. Наследуется от GameObject и отвечает за движение,
    отрисовку змейки, обработку столкновений с собой и сброс
    в первоначальное состояние в случае такого события.
    """

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    # Отрисовка змейки на экране.
    def draw(self):
        """
        Рисует все сегменты змейки на экране:
        тело, голову и затирает последний сегмент.
        """
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    # Определение позиции головы змейки.
    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    # Описание движения змейки.
    def move(self):
        """
        Перемещает голову в направлении self.direction,
        при выходе за границы экрана — телепортирует
        на противоположную сторону,
        обновляет список позиций и запоминает
        последний сегмент для затирания.
        """
        self.position = (
            self.position[0] + self.direction[0] * GRID_SIZE,
            self.position[1] + self.direction[1] * GRID_SIZE
        )
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

        # Определение последнего элемента для затирания и удаление
        # его из списка.
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    # Обработка изменения направления движения.
    def update_direction(self):
        """
        Применяет изменение направления движения
        (если оно было задано в handle_keys).
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Обнуление змейки при столкновении с собой.
    def reset(self):
        """
        Сбрасывает змейку в начальное состояние:
        очищает список координат сегментов, возвращает длину,
        позицию и направление движения к стартовым параметрам.
        """
        for item in self.positions:
            last_rect = pg.Rect(item, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.length = 1
        self.position = SCREEN_CENTER
        self.positions = [self.position]
        self.direction = RIGHT

    # Обработка столкновения змейки с собой.
    def handle_collisions(self):
        """
        Проверяет столкновение головы с телом.
        При обнаружении — сбрасывает змейку.
        """
        if self.get_head_position() in self.positions[1:]:
            self.reset()


def handle_keys(game_object):
    """
    Обрабатывает события клавиатуры и системные события PyGame.
    При нажатии стрелок меняет направление движения переданного объекта,
    проверяя, что нельзя сделать разворот на 180 градусов.
    При получении события QUIT завершает работу приложения.

    Параметры:
        game_object: объект с атрибутами direction и next_direction,
        в этом конкретном случае - экземпляр класса Snake.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Проверка, что рандомно выбранная позиция яблока не попала на змейку.
# Выбор новой позиции, если попала.
def check_apple_position(apple, snake):
    """
    Проверяет, что текущее положение яблока не совпадает с каким-либо
    сегментом змейки. Если совпадает, генерирует для яблока новую случайную
    позицию до тех пор, пока она не окажется свободной.
    Параметры:
        apple: экземпляр класса Apple с методом randomize_position().
        snake: экземпляр класса Snake с атрибутом positions
        (список координат сегментов змейки).
    """
    while apple.position in snake.positions:
        apple.randomize_position()


# Обработка события поедания яблока.
def eat_an_apple(apple, snake):
    """
    Проверяет, съела ли змея яблоко (совпадение головы змейки
    и позиции яблока). Если съела, увеличивает длину змейки, меняет
    позицию яблока и снова проверяет, что новое положение свободно.

    Параметры:
        apple: экземпляр класса Apple.
        snake: экземпляр класса Snake.
    """
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize_position()
        check_apple_position(apple, snake)


def main():
    """
    Точка входа в игру. Инициализирует PyGame, создает объекты яблока и змейки,
    устанавливает первую позицию яблока и запускает основной игровой цикл:
    чтение ввода с клавиатуры, обновление направления и положения змейки,
    проверка столкновений, поедания яблока, отрисовка объектов
    и обновление экрана.
    """
    # Инициализация PyGame:
    pg.init()
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
        pg.display.update()


if __name__ == '__main__':
    main()
