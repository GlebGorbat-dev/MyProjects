import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

EMAIL_SENDER = "glebgorbat17@gmail.com"
EMAIL_PASSWORD = "***************"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_registration_email(recipient_email):
    try:
        msg = MIMEText("Вы успешно зарегистрированы в Telegram-боте Справочник путешественника!", 'plain', 'utf-8')
        msg['Subject'] = "Успешная регистрация в Справочнике путешественника"
        msg['From'] = EMAIL_SENDER
        msg['To'] = recipient_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Включение TLS
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())
        logging.info(f"Письмо успешно отправлено на {recipient_email}")
        return True
    except smtplib.SMTPAuthenticationError:
        logging.error(f"Ошибка аутентификации SMTP. Проверьте EMAIL_SENDER и EMAIL_PASSWORD.")
        return False
    except smtplib.SMTPException as e:
        logging.error(f"Ошибка отправки письма на {recipient_email}: {e}")
        return False
    except Exception as e:
        logging.error(f"Неизвестная ошибка при отправке письма: {e}")
        return False

def init_db():
    try:
        conn = sqlite3.connect('sights.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL UNIQUE,
                sight1 TEXT NOT NULL,
                sight2 TEXT NOT NULL,
                hotel TEXT NOT NULL,
                sight1_coords TEXT,
                sight2_coords TEXT,
                hotel_coords TEXT,
                sight1_photo TEXT,
                sight2_photo TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()
        logging.info("Таблицы sights и users успешно созданы или уже существуют.")
    except sqlite3.Error as e:
        logging.error(f"Ошибка при инициализации базы данных: {e}")
    finally:
        conn.close()

def register_user(telegram_id, email, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn = sqlite3.connect('sights.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (telegram_id, email, password_hash) VALUES (?, ?, ?)',
                       (telegram_id, email, password_hash))
        conn.commit()
        logging.info(f"Пользователь {telegram_id} успешно зарегистрирован с email {email}")

        send_registration_email(email)
        return True
    except sqlite3.IntegrityError:
        logging.warning(f"Попытка регистрации с уже существующим telegram_id {telegram_id} или email {email}")
        return False
    except sqlite3.Error as e:
        logging.error(f"Ошибка при регистрации пользователя: {e}")
        return False
    finally:
        conn.close()

def authenticate_user(telegram_id, email, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn = sqlite3.connect('sights.db')
        cursor = conn.cursor()
        cursor.execute('SELECT telegram_id FROM users WHERE email = ? AND password_hash = ?',
                       (email, password_hash))
        result = cursor.fetchone()
        conn.close()
        if result and result[0] == telegram_id:
            logging.info(f"Пользователь {telegram_id} успешно вошел с email {email}")
            return True
        logging.warning(f"Неудачная попытка входа для {telegram_id} с email {email}")
        return False
    except sqlite3.Error as e:
        logging.error(f"Ошибка при аутентификации пользователя: {e}")
        return False

def is_user_registered(telegram_id):
    try:
        conn = sqlite3.connect('sights.db')
        cursor = conn.cursor()
        cursor.execute('SELECT telegram_id FROM users WHERE telegram_id = ?', (telegram_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except sqlite3.Error as e:
        logging.error(f"Ошибка при проверке регистрации пользователя: {e}")
        return False

def get_sights(city):
    try:
        conn = sqlite3.connect('sights.db')
        cursor = conn.cursor()
        cursor.execute('SELECT sight1, sight2, hotel, sight1_coords, sight2_coords, hotel_coords, sight1_photo, sight2_photo FROM sights WHERE city = ?', (city,))
        result = cursor.fetchone()
        conn.close()
        return result
    except sqlite3.Error as e:
        logging.error(f"Ошибка при получении данных о городе {city}: {e}")
        return None
