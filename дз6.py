import pygame
from queue import PriorityQueue
from pygame import Surface

pygame.init()

WIDTH = 600 # ширина окна 
GRID_SIZE = 10 # кол-во ячеек в одной строке/одном столбце
CELL_SIZE = WIDTH // GRID_SIZE # размер одной ячейки
WINDOW = pygame.display.set_mode((WIDTH, WIDTH)) # создание окна с заданой шириной
pygame.display.set_caption("A* поиск кратчайшего пути (нажмите ENTER для старта)") # заголовок окна

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)              # определение используемых цветов в формате RGB 
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GREY = (200, 200, 200)
VISITED_COLOR = (255, 200, 200)

# типы ячеек
EMPTY = 0 # пустая 
OBSTACLE = 1 # препятствие 
START = 2 # точка старта
END = 3 # финиш
PATH = 4 # сам путь
VISITED = 5 # посещаемая во время поиска пути

colors = {
    START: BLUE,
    END: BLACK,
    OBSTACLE: GREY,             # в этом блоке к каждому типу ячеек присваивается свой цвет
    PATH: PURPLE,
    VISITED: VISITED_COLOR,
    EMPTY: WHITE
}

class Cell:
    def __init__(self, x, y, type: int):  # инциализация ячеек
        # координаты ячеек в сетке 
        self.x = x   
        self.y = y
        self.type = type # тип ячейки
        self.color = colors.get(self.type, WHITE) # цвет ячейки в зависимости от типа
        self.neighbors = [] # список соседей
        self.g = float('inf') # стоимость пути от начальной точки до этой ячейки. изначальлно бесконечность
        self.h = 0 # эвристическая оценка стоимости пути от этой точки до конечной
        self.f = float('inf') # общая стоимость. основной показатель для А*. изначально бесконечность
        self.parent = None  # ссылка на ячейку из которой мы пришли 

    def draw(self, window: Surface): # отрисовка ячеек 
        pygame.draw.rect(window, self.color, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) # отрисовка ячейки с её текущим цветом

    def update_color(self): # обновление цвета ячейки в зависимости от его типа
        self.color = colors.get(self.type, WHITE) # получение цвета из списка соответсвий типа и цвета

    def update_neighbors(self, grid): # нахождение и сохранение всех соседий
        self.neighbors = [] # очищаем список прошлых соседей 
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # определяем куда можно идти для поиска соседей(направдения: вверх, вниз, влево, вправо)
        for dx, dy in directions: # проходимся по всем направлениям
            # координаты соседа
            x = self.x + dx 
            y = self.y + dy
            # проверка находится ли сосед в пределах сетки
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                cell = grid[x][y] # получаем соседа из сетки
                if cell.type != OBSTACLE: # если сосед не является препятствием 
                    self.neighbors.append(cell) # добавлем его в список

    def __lt__(self, other): #  не дает сравнивать ячейки с одинаковым f
        return False

def make_grid(): # создание пустой сетки
    grid = [] # список для хранения рядов
    for i in range(GRID_SIZE): # итерация по строкам
        grid.append([]) # добавление пустого ряда в сетку
        for j in range(GRID_SIZE): # итерация по столбцам
            cell = Cell(i, j, EMPTY) # создаем новую ячейку с координатам(i,j)
            grid[i].append(cell) # добавление ячейки в текущий ряд
    return grid # возвращаем собраную сетку

def draw(window, grid): # отрисовка окна
    window.fill(WHITE) # заливка окна белым цветом 
    for row in grid: # обходим каждый ряд в сетке
        for cell in row: # обходим каждую ячейку в ряду
            cell.draw(window) # отрисовка каждой ячейки
    for i in range(GRID_SIZE + 1): # отрисовка линий сетки
        pygame.draw.line(window, (128, 128, 128), (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE)) # отрисовка горизонтальных линий
        pygame.draw.line(window, (128, 128, 128), (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH)) # отрисовка вертикальных линий
    pygame.display.update() # обновление дисплея, чтобы показать, что было отрисовано 

def heuristic(loc_from, loc_to): # манхеттенское расстояние
    return abs(loc_from.x - loc_to.x) + abs(loc_from.y - loc_to.y) # расстояние по X и Y с учетом разрешенных направлений

def build_path(end, start): # восстановление найленного пути 
    current = end # начало в конечной точке
    while current and current.parent: # двигаемся в обратную сторону пока не вернемся в точку старта
        current.type = PATH # меняем тип ячейки 
        current.update_color() # обновляем цвет
        current = current.parent # переходим к предыдущей ячейке

def a_star(draw_callback, grid, start, end): # алгорим A* 
    count = 0 # счетчик для одинаковых f
    open_set = PriorityQueue() # очередь с проритетом для хранения узлов к рассмотрению
    open_set.put((0, count, start)) # добавление начального узла в очередь
    start.g = 0 # стоимость пути до его начала
    start.f = heuristic(start, end) # f для начального узла
    open_set_hash = {start} # множество для быстрой проверки наличия узла в open_set

    while not open_set.empty(): # пока есть узлы для рассмотрения
        for event in pygame.event.get(): # обработка чтобы окно не висло и его можно было закрыть
            if event.type == pygame.QUIT:
                pygame.quit()
                return None # выход если позьзователь закрыл окно

        current = open_set.get()[2] # извлекаем из очереди узел с самым маленьким f. возвращаем саму ячейку
        open_set_hash.remove(current) # удаление его из списка из-за того что мы его обрабатыеваем

        if current == end: # если текущий узел финиш, то мы нашли путь
            build_path(end, start) # восстанавление и отрисовка пути
            end.type = END 
            end.update_color()        # задаем тип чтобы окрасить старт и финиш
            start.type = START
            start.update_color()
            draw_callback() # финальная отрисовка
            return True # сигнал об успехе

        for neighbor in current.neighbors: # обход всех соседей
            temp_g = current.g + 1 # считаем g соседа 
            if temp_g < neighbor.g: # если нашли более короткий путь до этого  соседа
                neighbor.parent = current # запоминаем откуда пришли 
                neighbor.g = temp_g # обновляем g
                neighbor.f = temp_g + heuristic(neighbor, end) # пересчитываем f
                if neighbor not in open_set_hash: # если этого соседа нет в очереди
                    count += 1 # увеличиваем счетчик для одинаковых f
                    open_set.put((neighbor.f, count, neighbor)) # добавление соседа в очередь
                    open_set_hash.add(neighbor) # добавление в множество
                    if neighbor != end: 
                        neighbor.type = VISITED     # помечаем узел как посещенный
                        neighbor.update_color()
        draw_callback() # перерисовка сетки 
        pygame.time.wait(50) # задерка для наглядности визуализауии
    return False # если цикл закончился а путь не найден 

def run_task_from_image(mode, grid=None, start=None, end=None): # настройка поля
    task_map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],              # карта где числа соответствуют типу ячейки
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [2, 0, 1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 1, 3],
    ]

    if mode == 'setup': # настройка
        grid = make_grid()                    # создаем
        start_node, end_node = None, None       # пустую ячейку
        for y, row_data in enumerate(task_map): # обход карты (y - номер строки, сама строка)
            for x, cell_type in enumerate(row_data): # x - номер столбца, тип ячейки
                cell = grid[x][y] # получаем соответсвующую ячейку
                cell.type = cell_type # устанавливаем её тип
                cell.update_color() # обновляем цвет
                if cell.type == START: start_node = cell # если это старт то запоминаем её
                elif cell.type == END: end_node = cell # если это финш то запоминаем её
        
        draw(WINDOW, grid) # отрисовка полученного поля
        return grid, start_node, end_node # созвращаем сетку начало и конец

    elif mode == 'run': # запуск
        if grid and start and end: # проверка сетки
            for row in grid: # находим соседей каждой ячейки
                for cell in row:
                    cell.update_neighbors(grid)
            a_star(lambda: draw(WINDOW, grid), grid, start, end) # запуск А*. передаем ему отрисовку

def main():
    running = True # запуск главного цикла
    started = False # проверка был ли запущен алгоритм

    grid, start, end = run_task_from_image(mode='setup') # получение готовой сетки начала и конца
    
    while running: # главный цикл
        for event in pygame.event.get(): # обработка нажатия клавишь/закрытие окна
            if event.type == pygame.QUIT: # если пользователь нажал на закрытие окна то закрываем его
                running = False # завершаем главный цикл
            
            if event.type == pygame.KEYDOWN: # если нажали ENTER 
                if event.key == pygame.K_RETURN and not started: # если нажали и алгоритм ещё не запущен
                    print("Запуск алгоритма A*...")     
                    started = True        #помечаем что алгоритм запущен
                    run_task_from_image(mode='run', grid=grid, start=start, end=end) # запускаем саму прогу
                    print("Поиск завершен.")

    pygame.quit() # выход

main() # запуск напрямую 