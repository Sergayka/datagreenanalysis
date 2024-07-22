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
def is_gray(r, g, b, threshold=23):  # Увеличим порог для более точного исключения серого
    return abs(r - g) < threshold and abs(b - r) < threshold


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
freeze = 0
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
    # Поиск зеленых и светло-голубых моделей
    for x in range(0, width, 20):
        for y in range(0, height, 20):
            r, g, b = scrn.getpixel((x, y))

            # Проверка на серые объекты (разница между r, g, b меньше определенного порога)
            if is_gray(r, g, b):
                continue

            # Проверка на зеленые объекты
            if (r in range(102, 220)) and (g in range(200, 255) and (b in range(10, 80))):
                screen_x = window_rect[0] + x
                screen_y = window_rect[1] + y
                click(screen_x + 4, screen_y)
                time.sleep(0.05)
                break

            if freeze <= 3:
                # Проверка на светло-голубые объекты
                if (r in range(125, 175)) and (g in range(200, 255)) and (b in range(200, 255)):
                    screen_x = window_rect[0] + x
                    screen_y = window_rect[1] + y
                    click(screen_x + 4, screen_y)
                    time.sleep(0.05)
                    last_found_time = time.time()
                    freeze += 1
                    break


    # Проверка, прошло ли n секунд после начала сессии
    if start_timer and (time.time() - timer_start_time >= 30):
        print("поиск")
        for x in range(0, width, 20):
            for y in range(8 * height // 10, height, 20):
                r, g, b = scrn.getpixel((x, y))
                # Проверка на белую кнопку
                if r > 240 and g > 240 and b > 240:  # Условия для белого цвета
                    screen_x = window_rect[0] + x
                    screen_y = window_rect[1] + y
                    click(screen_x - 6, screen_y - 7)
                    time.sleep(0.001)
                    timer_start_time = time.time()
                    pixel_found = True
                    print('[✅] | игра')
                    break


print('[✅] | Остановлено.')
