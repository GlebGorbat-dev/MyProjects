// Определение класса MinesweeperGame для управления игрой в сапер на фронтенде
class MinesweeperGame {
    // Конструктор класса - инициализация всех элементов интерфейса и переменных
    constructor() {
        // Получение ссылки на DOM элемент игрового поля
        this.gameBoard = document.getElementById('game-board');
        // Получение ссылки на DOM элемент счетчика мин
        this.minesCount = document.getElementById('mines-count');
        // Получение ссылки на DOM элемент таймера
        this.timer = document.getElementById('timer');
        // Получение ссылки на DOM элемент статуса игры
        this.gameStatus = document.getElementById('game-status');
        // Получение ссылки на DOM элемент сообщений игры
        this.gameMessage = document.getElementById('game-message');
        // Получение ссылки на DOM элемент кнопки новой игры
        this.newGameBtn = document.getElementById('new-game-btn');
        // Получение ссылки на DOM элемент выбора сложности
        this.difficultySelect = document.getElementById('difficulty');
        // Получение ссылки на DOM элемент пользовательских настроек
        this.customSettings = document.getElementById('custom-settings');
        
        // Переменная для хранения текущего состояния игры с сервера
        this.gameState = null;
        // Флаг начала игры (True когда игрок сделал первый клик)
        this.gameStarted = false;
        // Время игры в секундах
        this.gameTime = 0;
        // ID интервала таймера для его остановки
        this.timerInterval = null;
        
        // Объект с настройками сложности игры
        this.difficultySettings = {
            // Легкая сложность: поле 9x9 с 10 минами
            easy: { rows: 9, cols: 9, mines: 10 },
            // Средняя сложность: поле 16x16 с 40 минами
            medium: { rows: 16, cols: 16, mines: 40 },
            // Сложная сложность: поле 16x30 с 99 минами
            hard: { rows: 16, cols: 30, mines: 99 },
            // Пользовательская сложность: поле 9x9 с 10 минами (по умолчанию)
            custom: { rows: 9, cols: 9, mines: 10 }
        };
        
        // Вызов метода инициализации игры
        this.init();
    }
    
    // Метод инициализации игры - настройка обработчиков событий и создание первой игры
    init() {
        // Настройка всех обработчиков событий для элементов интерфейса
        this.setupEventListeners();
        // Создание новой игры при запуске
        this.createNewGame();
    }
    
    // Метод настройки обработчиков событий для всех интерактивных элементов
    setupEventListeners() {
        // Обработчик клика по кнопке новой игры
        this.newGameBtn.addEventListener('click', () => {
            // Создание новой игры при клике на кнопку
            this.createNewGame();
        });
        
        // Обработчик изменения выбора сложности
        this.difficultySelect.addEventListener('change', (e) => {
            // Проверка: если выбрана пользовательская сложность
            if (e.target.value === 'custom') {
                // Показ блока пользовательских настроек
                this.customSettings.style.display = 'flex';
            } else {
                // Скрытие блока пользовательских настроек
                this.customSettings.style.display = 'none';
            }
        });
        
        // Обработчик левых кликов по клеткам игрового поля
        this.gameBoard.addEventListener('click', (e) => {
            // Проверка: клик по клетке и клетка не помечена флагом
            if (e.target.classList.contains('cell') && !e.target.classList.contains('flagged')) {
                // Обработка клика для открытия клетки
                this.handleCellClick(e.target, 'reveal');
            }
        });
        
        // Обработчик правых кликов (контекстное меню) по клеткам
        this.gameBoard.addEventListener('contextmenu', (e) => {
            // Отмена стандартного контекстного меню
            e.preventDefault();
            // Проверка: клик по клетке и клетка не открыта
            if (e.target.classList.contains('cell') && !e.target.classList.contains('revealed')) {
                // Обработка клика для установки/снятия флага
                this.handleCellClick(e.target, 'flag');
            }
        });
    }
    
    // Асинхронный метод создания новой игры с отправкой запроса на сервер
    async createNewGame() {
        // Получение выбранной сложности из селекта
        const difficulty = this.difficultySelect.value;
        // Переменная для хранения настроек игры
        let settings;
        
        // Проверка: если выбрана пользовательская сложность
        if (difficulty === 'custom') {
            // Получение пользовательских настроек из полей ввода
            settings = {
                // Количество строк из поля ввода
                rows: parseInt(document.getElementById('custom-rows').value),
                // Количество столбцов из поля ввода
                cols: parseInt(document.getElementById('custom-cols').value),
                // Количество мин из поля ввода
                mines: parseInt(document.getElementById('custom-mines').value)
            };
        } else {
            // Получение настроек из предустановленных вариантов
            settings = this.difficultySettings[difficulty];
        }
        
        // Попытка создания новой игры на сервере
        try {
            // Отправка POST запроса на сервер для создания новой игры
            const response = await fetch('/new_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // Отправка настроек игры в формате JSON
                body: JSON.stringify(settings)
            });
            
            // Получение ответа от сервера в формате JSON
            const result = await response.json();
            
            // Проверка успешности создания игры
            if (result.success) {
                // Сброс состояния игры на фронтенде
                this.resetGame();
                // Создание визуального игрового поля
                this.createBoard(settings.rows, settings.cols);
                // Обновление счетчика мин
                this.updateMinesCount(settings.mines);
                // Показ сообщения об успешном создании игры
                this.showMessage('Новая игра началась! Удачи!', 'info');
            } else {
                // Показ сообщения об ошибке создания игры
                this.showMessage('Ошибка создания игры: ' + result.message, 'error');
            }
        } catch (error) {
            // Обработка ошибки соединения с сервером
            this.showMessage('Ошибка соединения с сервером', 'error');
            // Вывод ошибки в консоль для отладки
            console.error('Error:', error);
        }
    }
    
    // Метод сброса состояния игры к начальному состоянию
    resetGame() {
        // Сброс флага начала игры
        this.gameStarted = false;
        // Сброс времени игры
        this.gameTime = 0;
        // Обновление отображения таймера
        this.updateTimer();
        // Обновление статуса игры
        this.updateStatus('Готов к игре');
        
        // Проверка: если таймер запущен
        if (this.timerInterval) {
            // Остановка таймера
            clearInterval(this.timerInterval);
            // Сброс ссылки на интервал
            this.timerInterval = null;
        }
        
        // Очистка игрового поля от всех клеток
        this.gameBoard.innerHTML = '';
    }
    
    // Метод создания визуального игрового поля из DOM элементов
    createBoard(rows, cols) {
        // Установка CSS Grid для игрового поля с заданным количеством столбцов
        this.gameBoard.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
        // Установка CSS Grid для игрового поля с заданным количеством строк
        this.gameBoard.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
        
        // Создание клеток игрового поля
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                // Создание нового DOM элемента для клетки
                const cell = document.createElement('div');
                // Добавление CSS класса 'cell' для стилизации
                cell.className = 'cell';
                // Сохранение координат клетки в data-атрибутах
                cell.dataset.row = row;
                cell.dataset.col = col;
                // Добавление клетки в игровое поле
                this.gameBoard.appendChild(cell);
            }
        }
    }
    
    // Асинхронный метод обработки клика по клетке
    async handleCellClick(cell, action) {
        // Получение координат клетки из data-атрибутов
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        
        // Проверка: если игра не началась и действие - открытие клетки
        if (!this.gameStarted && action === 'reveal') {
            // Запуск таймера игры
            this.startTimer();
        }
        
        // Попытка отправки клика на сервер
        try {
            // Отправка POST запроса на сервер с данными клика
            const response = await fetch('/click', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // Отправка координат и типа действия в формате JSON
                body: JSON.stringify({
                    row: row,
                    col: col,
                    action: action
                })
            });
            
            // Получение ответа от сервера в формате JSON
            const result = await response.json();
            
            // Проверка успешности действия
            if (result.success) {
                // Обновление состояния игры данными с сервера
                this.updateGameState(result.game_state);
            } else {
                // Показ сообщения об ошибке
                this.showMessage('Неверное действие', 'error');
            }
        } catch (error) {
            // Обработка ошибки соединения с сервером
            this.showMessage('Ошибка соединения с сервером', 'error');
            // Вывод ошибки в консоль для отладки
            console.error('Error:', error);
        }
    }
    
    // Метод обновления состояния игры данными с сервера
    updateGameState(gameState) {
        // Сохранение состояния игры в переменной класса
        this.gameState = gameState;
        
        // Обновление визуального отображения всех клеток
        this.updateCells(gameState);
        
        // Обновление счетчика оставшихся мин
        this.updateMinesCount(gameState.mines_left);
        
        // Проверка состояния игры
        if (gameState.game_over) {
            // Завершение игры с поражением
            this.endGame(false);
        } else if (gameState.win) {
            // Завершение игры с победой
            this.endGame(true);
        }
    }
    
    // Метод обновления визуального отображения всех клеток игрового поля
    updateCells(gameState) {
        // Получение всех DOM элементов клеток
        const cells = this.gameBoard.querySelectorAll('.cell');
        
        // Проход по всем клеткам для обновления их состояния
        cells.forEach(cell => {
            // Получение координат клетки из data-атрибутов
            const row = parseInt(cell.dataset.row);
            const col = parseInt(cell.dataset.col);
            // Создание ключа для поиска в массивах состояния игры
            const cellKey = `${row},${col}`;
            
            // Сброс всех CSS классов клетки
            cell.className = 'cell';
            // Очистка текстового содержимого клетки
            cell.textContent = '';
            // Очистка data-атрибута с номером
            cell.dataset.number = '';
            
            // Проверка: если клетка открыта
            if (gameState.revealed.includes(cellKey)) {
                // Добавление CSS класса для открытой клетки
                cell.classList.add('revealed');
                
                // Получение значения клетки из игрового поля
                const value = gameState.board[row][col];
                
                // Проверка: если клетка содержит мину
                if (value === -1) {
                    // Добавление CSS класса для мины
                    cell.classList.add('mine');
                    // Установка эмодзи мины как содержимого
                    cell.textContent = '💣';
                } else if (value > 0) {
                    // Если клетка содержит число (количество соседних мин)
                    // Установка числа как текстового содержимого
                    cell.textContent = value;
                    // Сохранение числа в data-атрибуте
                    cell.dataset.number = value;
                }
            }
            
            // Проверка: если клетка помечена флагом
            if (gameState.flagged.includes(cellKey)) {
                // Добавление CSS класса для помеченной клетки
                cell.classList.add('flagged');
                // Установка эмодзи флага как содержимого
                cell.textContent = '🚩';
            }
        });
    }
    
    // Метод запуска таймера игры
    startTimer() {
        // Установка флага начала игры
        this.gameStarted = true;
        // Обновление статуса игры
        this.updateStatus('Игра идет...');
        
        // Запуск интервала для обновления таймера каждую секунду
        this.timerInterval = setInterval(() => {
            // Увеличение времени игры на 1 секунду
            this.gameTime++;
            // Обновление отображения таймера
            this.updateTimer();
        }, 1000);
    }
    
    // Метод завершения игры (победа или поражение)
    endGame(won) {
        // Сброс флага начала игры
        this.gameStarted = false;
        
        // Проверка: если таймер запущен
        if (this.timerInterval) {
            // Остановка таймера
            clearInterval(this.timerInterval);
            // Сброс ссылки на интервал
            this.timerInterval = null;
        }
        
        // Проверка результата игры
        if (won) {
            // Обновление статуса при победе
            this.updateStatus('Победа! 🎉');
            // Показ сообщения о победе с временем
            this.showMessage(`Поздравляем! Вы выиграли за ${this.formatTime(this.gameTime)}!`, 'success');
        } else {
            // Обновление статуса при поражении
            this.updateStatus('Поражение 💥');
            // Показ сообщения о поражении
            this.showMessage('Вы попали на мину! Попробуйте еще раз.', 'error');
            
            // Показ всех мин на поле
            this.revealAllMines();
        }
    }
    
    // Метод показа всех мин на поле при поражении
    revealAllMines() {
        // Проверка: если состояние игры не загружено
        if (!this.gameState) return;
        
        // Получение всех DOM элементов клеток
        const cells = this.gameBoard.querySelectorAll('.cell');
        
        // Проход по всем клеткам
        cells.forEach(cell => {
            // Получение координат клетки из data-атрибутов
            const row = parseInt(cell.dataset.row);
            const col = parseInt(cell.dataset.col);
            
            // Проверка: если клетка содержит мину и не помечена флагом
            if (this.gameState.board[row][col] === -1 && !cell.classList.contains('flagged')) {
                // Добавление CSS классов для мины и взрыва
                cell.classList.add('mine', 'exploded');
                // Установка эмодзи мины как содержимого
                cell.textContent = '💣';
            }
        });
    }
    
    // Метод обновления отображения таймера
    updateTimer() {
        // Установка отформатированного времени в элемент таймера
        this.timer.textContent = this.formatTime(this.gameTime);
    }
    
    // Метод форматирования времени из секунд в формат MM:SS
    formatTime(seconds) {
        // Вычисление количества минут (целая часть от деления на 60)
        const mins = Math.floor(seconds / 60);
        // Вычисление количества секунд (остаток от деления на 60)
        const secs = seconds % 60;
        // Возврат отформатированной строки с ведущими нулями
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    
    // Метод обновления счетчика оставшихся мин
    updateMinesCount(count) {
        // Установка количества мин в элемент счетчика
        this.minesCount.textContent = count;
    }
    
    // Метод обновления статуса игры
    updateStatus(status) {
        // Установка текста статуса в элемент статуса
        this.gameStatus.textContent = status;
    }
    
    // Метод показа сообщений пользователю
    showMessage(message, type) {
        // Установка текста сообщения в элемент сообщений
        this.gameMessage.textContent = message;
        // Установка CSS класса для стилизации сообщения по типу
        this.gameMessage.className = `game-message ${type}`;
        
        // Автоматическое скрытие сообщения через 3 секунды
        setTimeout(() => {
            // Очистка текста сообщения
            this.gameMessage.textContent = '';
            // Сброс CSS класса сообщения
            this.gameMessage.className = 'game-message';
        }, 3000);
    }
}

// Инициализация игры при полной загрузке DOM документа
document.addEventListener('DOMContentLoaded', () => {
    // Создание нового экземпляра игры MinesweeperGame
    new MinesweeperGame();
});
