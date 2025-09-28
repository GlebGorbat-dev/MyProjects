import tkinter as tk
from tkinter import messagebox
import sys
import os
import time
import threading
import webbrowser

driver = None  # глобальный объект для контроля браузера

def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

def run_video_bot(query):
    """Запуск видео через системный браузер (легковесный вариант)"""
    try:
        query = query.strip()
        if not query:
            messagebox.showwarning("Пустой запрос", "Введите название видео")
            return
        
        # Используем системный браузер вместо Selenium
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        messagebox.showinfo("Видео запущено", "Видео открыто в браузере")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")

def run_video_bot_selenium(query):
    """Запуск видео через Selenium (для случаев когда нужен автоматический поиск)"""
    try:
        # Ленивая загрузка тяжелых библиотек
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import undetected_chromedriver as uc
        
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--log-level=3")
        # Убираем headless режим для стабильной работы
        # options.add_argument("--headless")
        
        driver = uc.Chrome(options=options)
        wait = WebDriverWait(driver, 15)  # Увеличиваем время ожидания
        
        driver.get("https://www.youtube.com")
        time.sleep(2)  # Увеличиваем время ожидания
        
        # Ждем загрузки страницы
        wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
        
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        # Ждем результатов поиска
        time.sleep(3)
        
        # Ищем первый видео элемент
        try:
            video = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a#video-title")))
            video_url = video.get_attribute("href")
        except:
            # Альтернативный селектор
            video = driver.find_element(By.CSS_SELECTOR, "a#video-title")
            video_url = video.get_attribute("href")
        
        driver.quit()
        
        # Открываем видео в системном браузере
        if video_url:
            webbrowser.open(video_url)
            messagebox.showinfo("Видео запущено", "Видео найдено и открыто в браузере")
        else:
            messagebox.showwarning("Предупреждение", "Видео не найдено")
            
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")

def prepare_background(path):
    """Упрощенная загрузка фона без OpenCV"""
    try:
        from PIL import Image, ImageTk
        img = Image.open(path)
        # Уменьшаем размер изображения для экономии памяти
        img = img.resize((710, 444), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки фона: {e}")
        return None

def launch_gui():
    """Оптимизированный GUI с минимальным потреблением ресурсов"""
    root = tk.Tk()
    root.title("YouTube Video Finder")
    root.geometry("400x200")
    root.resizable(False, False)
    
    # Устанавливаем минимальный стиль без фона
    root.configure(bg='#2c2c2c')
    
    # Главный фрейм
    main_frame = tk.Frame(root, bg='#2c2c2c')
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Заголовок
    title_label = tk.Label(main_frame, text="YouTube Video Finder", 
                          font=("Arial", 16, "bold"), 
                          bg='#2c2c2c', fg='white')
    title_label.pack(pady=(0, 10))
    
    # Поле ввода
    entry_label = tk.Label(main_frame, text="Введите название видео:", 
                          font=("Arial", 10), 
                          bg='#2c2c2c', fg='white')
    entry_label.pack(pady=(0, 5))
    
    entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
    entry.pack(pady=(0, 15))
    entry.focus()
    
    # Кнопки
    button_frame = tk.Frame(main_frame, bg='#2c2c2c')
    button_frame.pack()
    
    btn_browser = tk.Button(button_frame, text="Открыть в браузере", 
                           font=("Arial", 10), width=15,
                           bg='#4CAF50', fg='white', 
                           command=lambda: run_video_bot(entry.get()))
    btn_browser.pack(side=tk.LEFT, padx=(0, 10))
    
    btn_selenium = tk.Button(button_frame, text="Автопоиск", 
                            font=("Arial", 10), width=15,
                            bg='#2196F3', fg='white', 
                            command=lambda: threading.Thread(target=run_video_bot_selenium, 
                                                           args=(entry.get(),), daemon=True).start())
    btn_selenium.pack(side=tk.LEFT)
    
    # Обработка Enter в поле ввода
    entry.bind('<Return>', lambda e: run_video_bot(entry.get()))
    
    # Обработка закрытия окна
    def on_closing():
        root.destroy()
        sys.exit(0)
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    try:
        import multiprocessing
        multiprocessing.freeze_support()
        launch_gui()
    except KeyboardInterrupt:
        print("Приложение закрыто пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)
