# Импорт необходимых модулей Flask для создания веб-приложения
from flask import Flask, render_template, request, jsonify
# Импорт модуля random для генерации случайных чисел (размещение мин)
import random
# Импорт модуля json для работы с JSON данными
import json

# Создание экземпляра Flask приложения с именем текущего модуля
app = Flask(__name__)

# Определение класса MinesweeperGame для логики игры в сапер
class MinesweeperGame:
    # Конструктор класса - инициализация игры с параметрами по умолчанию
    def __init__(self, rows=9, cols=9, mines=10):
        # Количество строк на игровом поле (по умолчанию 9)
        self.rows = rows
        # Количество столбцов на игровом поле (по умолчанию 9)
        self.cols = cols
        # Количество мин на поле (по умолчанию 10)
        self.mines = mines
        # Двумерный массив для хранения игрового поля
        self.board = []
        # Флаг окончания игры (True если игрок попал на мину)
        self.game_over = False
        # Флаг победы (True если игрок открыл все клетки кроме мин)
        self.win = False
        # Флаг первого клика (True до первого клика игрока)
        self.first_click = True
        # Множество координат клеток, помеченных флагами
        self.flagged_cells = set()
        # Множество координат открытых клеток
        self.revealed_cells = set()
        
    # Метод инициализации пустого игрового поля
    def initialize_board(self):
        """Инициализация пустого игрового поля"""
        # Создание двумерного массива заполненного нулями (пустые клетки)
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
    # Метод размещения мин на игровом поле
    def place_mines(self, first_row, first_col):
        """Размещение мин на поле, избегая первого клика"""
        # Счетчик размещенных мин
        mines_placed = 0
        # Цикл продолжается пока не разместим все мины
        while mines_placed < self.mines:
            # Генерация случайной строки от 0 до rows-1
            row = random.randint(0, self.rows - 1)
            # Генерация случайного столбца от 0 до cols-1
            col = random.randint(0, self.cols - 1)
            
            # Проверка: не размещаем мину в первом клике и его окрестности
            if (row != first_row or col != first_col) and self.board[row][col] != -1:
                # Размещение мины (значение -1)
                self.board[row][col] = -1
                # Увеличение счетчика размещенных мин
                mines_placed += 1
                
    # Метод подсчета чисел для каждой клетки (количество соседних мин)
    def calculate_numbers(self):
        """Подсчет чисел для каждой клетки"""
        # Проход по всем строкам игрового поля
        for row in range(self.rows):
            # Проход по всем столбцам игрового поля
            for col in range(self.cols):
                # Проверка: если клетка не содержит мину
                if self.board[row][col] != -1:
                    # Счетчик мин в соседних клетках
                    count = 0
                    # Проверка всех 8 соседних клеток (3x3 область вокруг текущей клетки)
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            # Проверка границ поля и наличие мины в соседней клетке
                            if (0 <= row + i < self.rows and 
                                0 <= col + j < self.cols and 
                                self.board[row + i][col + j] == -1):
                                # Увеличение счетчика если найдена мина
                                count += 1
                    # Запись количества соседних мин в клетку
                    self.board[row][col] = count
                    
    # Метод получения списка соседних клеток для заданной позиции
    def get_neighbors(self, row, col):
        """Получение соседних клеток"""
        # Список для хранения координат соседних клеток
        neighbors = []
        # Проход по всем 8 соседним клеткам (3x3 область)
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Проверка границ поля и исключение самой клетки (i=0, j=0)
                if (0 <= row + i < self.rows and 
                    0 <= col + j < self.cols and 
                    (i != 0 or j != 0)):
                    # Добавление координат соседней клетки в список
                    neighbors.append((row + i, col + j))
        # Возврат списка соседних клеток
        return neighbors
        
    # Метод открытия клетки игроком
    def reveal_cell(self, row, col):
        """Открытие клетки"""
        # Проверка: клетка уже открыта или помечена флагом
        if (row, col) in self.revealed_cells or (row, col) in self.flagged_cells:
            # Возврат False если действие невозможно
            return False
            
        # Добавление клетки в множество открытых клеток
        self.revealed_cells.add((row, col))
        
        # Проверка: если клетка содержит мину
        if self.board[row][col] == -1:
            # Установка флага окончания игры
            self.game_over = True
            # Возврат True для успешного открытия (но игра окончена)
            return True
            
        # Проверка: если клетка пустая (число 0)
        if self.board[row][col] == 0:
            # Рекурсивное открытие всех соседних пустых клеток
            for neighbor_row, neighbor_col in self.get_neighbors(row, col):
                # Проверка что соседняя клетка еще не открыта
                if (neighbor_row, neighbor_col) not in self.revealed_cells:
                    # Рекурсивный вызов для открытия соседней клетки
                    self.reveal_cell(neighbor_row, neighbor_col)
                    
        # Проверка условия победы: все клетки кроме мин открыты
        if len(self.revealed_cells) == self.rows * self.cols - self.mines:
            # Установка флага победы
            self.win = True
            
        # Возврат True для успешного открытия
        return True
        
    # Метод установки/снятия флага на клетке
    def toggle_flag(self, row, col):
        """Установка/снятие флага"""
        # Проверка: нельзя ставить флаг на открытую клетку
        if (row, col) in self.revealed_cells:
            # Возврат False если действие невозможно
            return False
            
        # Проверка: если клетка уже помечена флагом
        if (row, col) in self.flagged_cells:
            # Удаление флага из множества помеченных клеток
            self.flagged_cells.remove((row, col))
        else:
            # Добавление флага в множество помеченных клеток
            self.flagged_cells.add((row, col))
        # Возврат True для успешного действия
        return True
        
    # Метод получения текущего состояния игры для отправки на фронтенд
    def get_game_state(self):
        """Получение состояния игры для фронтенда"""
        # Возврат словаря с полным состоянием игры
        return {
            # Игровое поле с минами и числами
            'board': self.board,
            # Список открытых клеток в формате строк "row,col"
            'revealed': [f"{row},{col}" for row, col in self.revealed_cells],
            # Список помеченных флагами клеток в формате строк "row,col"
            'flagged': [f"{row},{col}" for row, col in self.flagged_cells],
            # Флаг окончания игры (True если игрок попал на мину)
            'game_over': self.game_over,
            # Флаг победы (True если игрок выиграл)
            'win': self.win,
            # Количество оставшихся мин (общее количество - количество флагов)
            'mines_left': self.mines - len(self.flagged_cells)
        }

# Глобальная переменная для хранения текущей игры (один экземпляр на сессию)
current_game = None

# Декоратор маршрута для главной страницы игры
@app.route('/')
def index():
    """Главная страница игры"""
    # Возврат HTML шаблона главной страницы
    return render_template('index.html')

# Декоратор маршрута для создания новой игры (POST запрос)
@app.route('/new_game', methods=['POST'])
def new_game():
    """Создание новой игры"""
    # Объявление глобальной переменной для доступа к ней
    global current_game
    # Получение JSON данных из запроса
    data = request.get_json()
    # Извлечение количества строк (по умолчанию 9)
    rows = data.get('rows', 9)
    # Извлечение количества столбцов (по умолчанию 9)
    cols = data.get('cols', 9)
    # Извлечение количества мин (по умолчанию 10)
    mines = data.get('mines', 10)
    
    # Создание нового экземпляра игры с заданными параметрами
    current_game = MinesweeperGame(rows, cols, mines)
    # Инициализация пустого игрового поля
    current_game.initialize_board()
    
    # Возврат JSON ответа об успешном создании игры
    return jsonify({
        'success': True,
        'message': 'Новая игра создана'
    })

# Декоратор маршрута для обработки кликов по клеткам (POST запрос)
@app.route('/click', methods=['POST'])
def click_cell():
    """Обработка клика по клетке"""
    # Объявление глобальной переменной для доступа к ней
    global current_game
    # Проверка: игра должна быть инициализирована
    if not current_game:
        # Возврат ошибки если игра не создана
        return jsonify({'success': False, 'message': 'Игра не инициализирована'})
    
    # Получение JSON данных из запроса
    data = request.get_json()
    # Извлечение номера строки кликнутой клетки
    row = data.get('row')
    # Извлечение номера столбца кликнутой клетки
    col = data.get('col')
    # Извлечение типа действия ('reveal' для открытия или 'flag' для флага)
    action = data.get('action', 'reveal')
    
    # Проверка типа действия
    if action == 'flag':
        # Установка/снятие флага на клетке
        success = current_game.toggle_flag(row, col)
    else:
        # Проверка: если это первый клик в игре
        if current_game.first_click:
            # Размещение мин на поле (избегая первого клика)
            current_game.place_mines(row, col)
            # Подсчет чисел для всех клеток
            current_game.calculate_numbers()
            # Сброс флага первого клика
            current_game.first_click = False
        # Открытие клетки игроком
        success = current_game.reveal_cell(row, col)
    
    # Проверка успешности действия
    if success:
        # Возврат успешного ответа с текущим состоянием игры
        return jsonify({
            'success': True,
            'game_state': current_game.get_game_state()
        })
    else:
        # Возврат ошибки при неуспешном действии
        return jsonify({'success': False, 'message': 'Неверное действие'})

# Декоратор маршрута для получения текущего состояния игры (GET запрос)
@app.route('/game_state')
def get_game_state():
    """Получение текущего состояния игры"""
    # Объявление глобальной переменной для доступа к ней
    global current_game
    # Проверка: игра должна быть инициализирована
    if not current_game:
        # Возврат ошибки если игра не создана
        return jsonify({'success': False, 'message': 'Игра не инициализирована'})
    
    # Возврат успешного ответа с текущим состоянием игры
    return jsonify({
        'success': True,
        'game_state': current_game.get_game_state()
    })

# Проверка: если файл запускается напрямую (не импортируется)
if __name__ == '__main__':
    # Запуск Flask приложения в режиме отладки
    # debug=True - автоматическая перезагрузка при изменении кода
    # host='0.0.0.0' - приложение доступно на всех сетевых интерфейсах
    # port=52670 - приложение работает на порту 52670
    app.run(debug=True, host='0.0.0.0', port=52670)
