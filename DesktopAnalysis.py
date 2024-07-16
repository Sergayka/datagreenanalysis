from pyautogui import *
import pygetwindow as gw
import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller

mouse = Controller()
time.sleep(0.5)


# Функция характеризующая и инициализирующая все серые (бомбы) модели
def is_gray(r, g, b, threshold=20):  # Увеличен порог до 20
    return abs(r - g) < threshold and abs(b - r) < threshold


def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)


window_name = input('\n[✅] | Введите название окна (1 - TelegramDesktop): ')

if window_name == '1':
    window_name = "TelegramDesktop"

check = gw.getWindowsWithTitle(window_name)
if not check:
    print(f"[❌] | Окно - {window_name} не найдено!")
else:
    print(f"[✅] | Окно найдено - {window_name}\n[✅] | Нажмите 'q' для паузы.")

telegram_window = check[0]
paused = False
start_timer = False
timer_start_time = None
timer_expired = False

while True:
    if keyboard.is_pressed('q'):
        paused = not paused
        start_timer = not paused
        if paused:
            print('[✅] | Пауза.')
        else:
            timer_start_time = time.time()
            timer_expired = False
            print('[✅] | Продолжение работы.')
        time.sleep(0.2)

    if paused:
        continue

    window_rect = (
        telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
    )

    if telegram_window != []:
        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

    scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

    width, height = scrn.size
    pixel_found = False

    if not timer_expired:
        # Поиск зеленых и светло-голубых моделей
        for x in range(0, width, 20):
            for y in range(0, height, 20):
                r, g, b = scrn.getpixel((x, y))

                # Проверка на серые объекты (разница между r, g, b меньше определенного порога)
                if is_gray(r, g, b):
                    continue

                # Проверка на зеленые объекты
                if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                    screen_x = window_rect[0] + x
                    screen_y = window_rect[1] + y
                    click(screen_x + 4, screen_y)
                    time.sleep(0.001)
                    pixel_found = True
                    last_found_time = time.time()
                    break

                # Проверка на светло-голубые объекты
                if (r in range(100, 175)) and (g in range(200, 255)) and (b in range(200, 255)):
                    screen_x = window_rect[0] + x
                    screen_y = window_rect[1] + y
                    click(screen_x + 4, screen_y)
                    time.sleep(0.001)
                    pixel_found = True
                    last_found_time = time.time()
                    break

    # Проверка, прошло ли 60 секунд после начала сессии
    if (time.time() - timer_start_time >= 60):
        timer_expired = True
        print('[✅] | 60sec прошло, начинаем поиск кнопки')

        for x in range(0, width, 20):
            for y in range(8 * height // 10, height, 20):  # Нижние 10% экрана
                r, g, b = scrn.getpixel((x, y))
                # Проверка на белую кнопку
                if r > 240 and g > 240 and b > 240:  # Условия для белого цвета
                    screen_x = window_rect[0] + x
                    screen_y = window_rect[1] + y
                    click(screen_x - 6, screen_y - 7)
                    time.sleep(0.001)
                    timer_start_time = time.time()
                    pixel_found = True
                    print('[✅] | Белая кнопка была найдена')
                    break
            if pixel_found:
                break

print('[✅] | Остановлено.')
