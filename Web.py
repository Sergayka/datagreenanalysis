from pyautogui import *
import pygetwindow as gw
import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller

mouse = Controller()
time.sleep(0.5)


# Функция, характеризующая и инициализирующая все серые (бомбы) модели
def is_gray(r, g, b, threshold=15):  # Увеличим порог для более точного исключения серого
    return abs(r - g) < threshold and abs(b - r) < threshold

#
def check_surrounding_for_gray(scrn, x, y, width, height, distance=70):
    for dx in [-distance, distance + 1, 5]:
        for dy in [-distance, distance + 1, 5]:
            if 0 <= x + dx < width and 0 <= y + dy < height:
                r, g, b = scrn.getpixel((x + dx, y + dy))
                if is_gray(r, g, b):
                    return True
    return False


def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

#
# Вывод всех доступных окон
# print("[✅] | Доступные окна:")
# for window in gw.getAllWindows():
#     print(f" - {window.title}")

windows_list = gw.getAllWindows()
# Ищем нужное окно
window_name = None
for window in windows_list:
    if "Blum - SunBrowser" in window.title or "Telegram Web" in window.title:
        window_name = window.title
        break

if not window_name:
    print(f"[❌] | Нужное окно не найдено!")
    exit()

# window_name = input('\n[✅] | Введите название окна (1 - Blum-SunBrowser): ')

# if window_name == '1':
#     window_name = "Blum - SunBrowser"

# check = gw.getWindowsWithTitle(window_name)
# if not check:
#     print(f"[❌] | Окно - {window_name} не найдено!")
# else:

print(f"[✅] | Окно найдено - {window_name}")
# Ожидание ввода пользователя для старта
start_input = input('[✅] | Введите 1 для начала: ')
if start_input != '1':
    print("[❌] | Неверное значение, программа завершена.")
    exit()

print("Нажмите 'q' для паузы.")
browser_window = gw.getWindowsWithTitle(window_name)[0]
paused = False
start_timer = False
timer_start_time = None
random_time = random.randint(50, 51)

while True:
    if keyboard.is_pressed('q'):
        paused = not paused
        start_timer = not paused
        if paused:
            print('[✅] | Пауза.')
        else:
            timer_start_time = time.time()
            print('[✅] | Продолжение работы.')
        time.sleep(0.2)

    if paused:
        continue

    window_rect = (
        browser_window.left, browser_window.top, browser_window.width, browser_window.height
    )

    if browser_window != []:
        try:
            browser_window.activate()
        except:
            browser_window.minimize()
            browser_window.restore()

    scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

    width, height = scrn.size
    pixel_found = False
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
                time.sleep(0.01)
                pixel_found = True
                last_found_time = time.time()
                break

            # Проверка на светло-голубые объекты
            if (r in range(100, 175)) and (g in range(200, 255)) and (b in range(200, 255)):
                screen_x = window_rect[0] + x
                screen_y = window_rect[1] + y
                click(screen_x + 4, screen_y)
                time.sleep(0.01)
                pixel_found = True
                last_found_time = time.time()
                break

    # Проверка, прошло ли 50 секунд после начала сессии
    if start_timer and (time.time() - timer_start_time >= random_time):
        print(f'[✅] | {random_time}sec прошло, начинаем поиск кнопки Play')
        # Проверка, прошло ли 7 секунд с последнего нахождения объекта

        for x in range(0, width, 20):
            for y in range(3 * height // 4, height, 20):
                r, g, b = scrn.getpixel((x, y))
                # Проверка на кнопку "Play" (белый фон, черный шрифт)
                if r > 200 and g > 200 and b > 200:
                    # Поиск черного текста внутри белого фона
                    black_text_found = False
                    for dx in range(-10, 11):
                        for dy in range(-10, 11):
                            nr, ng, nb = scrn.getpixel((x + dx, y + dy))
                            if nr < 50 and ng < 50 and nb < 50:
                                black_text_found = True
                                break
                        if black_text_found:
                            break
                    if not black_text_found:
                        screen_x = window_rect[0] + x
                        screen_y = window_rect[1] + y
                        click(screen_x - 6, screen_y - 7)  # Сдвиг клика вверх и влево
                        time.sleep(0.001)
                        timer_start_time = time.time()
                        pixel_found = True
                        random_time = random.randint(60, 63)  # Обновляем случайное время
                        print('[✅] | Кнопка Play была найдена')
                        break
            if pixel_found:
                break

print('[✅] | Остановлено.')
