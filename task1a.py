import matplotlib.pyplot as plt
import numpy as np
import random
import os


def read_l_system_from_file(filename):
    """
    Чтение L-системы из текстового файла
    Формат файла:
    <атом> <угол поворота> <начальное направление>
    <правило №1>
    <правило №2>
    ...
    """
    l_system = {
        "atom": "",
        "rules": {},
        "angle": 0,
        "start_direction": 0
    }

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        if len(lines) < 2:
            raise ValueError("Файл должен содержать как минимум 2 строки")

        first_line = lines[0].split()
        l_system["atom"] = first_line[0]
        l_system["angle"] = float(first_line[1])
        l_system["start_direction"] = float(first_line[2]) if len(first_line) > 2 else 0

        for line in lines[1:]:
            if '→' in line:
                key, value = line.split('→', 1)
            elif '=' in line:
                key, value = line.split('=', 1)
            else:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key, value = parts
                else:
                    continue

            l_system["rules"][key.strip()] = value.strip()

    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
        return None

    return l_system


def generate_l_system(axiom, rules, iterations, randomness=0.0):
    current_string = axiom

    for _ in range(iterations):
        result = []
        for char in current_string:
            if char in rules:
                # Добавление случайности
                if randomness > 0 and random.random() < randomness:
                    result.append(char) #Сохраняется исходный символ
                else:
                    result.append(rules[char]) #Применяется правило
            else:
                result.append(char)
        current_string = "".join(result)

    return current_string


def points_l_system(l_system, iterations=4, randomness=0.0, step_length=1.0):
    axiom = l_system["atom"]
    angle = l_system["angle"]
    direction = l_system["start_direction"]
    rules = l_system["rules"]

    instructions = generate_l_system(axiom, rules, iterations, randomness)

    x, y = 0, 0
    stack = []
    points = [(x, y)]
    current_angle = np.radians(direction)

    for char in instructions:
        if char == "F" or char == "G":
            # Двигаемся вперед
            x_new = x + np.sin(current_angle) * step_length
            y_new = y + np.cos(current_angle) * step_length
            points.append((x_new, y_new))
            x, y = x_new, y_new
        elif char == "f" or char == "g":
            # Перемещаемся без рисования
            x_new = x + np.sin(current_angle) * step_length
            y_new = y + np.cos(current_angle) * step_length
            x, y = x_new, y_new
        elif char == "+":
            # Поворачиваем вправо
            current_angle -= np.radians(angle)
        elif char == "-":
            # Поворачиваем влево
            current_angle += np.radians(angle)
        elif char == "[":
            # Сохраняем текущую позицию и угол (начало ветвления)
            stack.append((x, y, current_angle))
        elif char == "]":
            # Восстанавливаем сохраненную позицию и угол (конец ветвления)
            if stack:
                x, y, current_angle = stack.pop()
                points.append((x, y))

    return points


def normalize_points(points):
    if not points:
        return points

    points = np.array(points)

    points -= points.min(axis=0)

    max_val = points.max()
    if max_val > 0:
        points /= max_val

    return points


def draw_l_system_from_file(filename, iterations=4, randomness=0.0, step_length=1.0):
    l_system = read_l_system_from_file(filename)
    if l_system is None:
        print(f"Не удалось загрузить L-систему из файла {filename}")
        return

    print(f"L-система из файла {filename}:")
    print(f"Атом: {l_system['atom']}")
    print(f"Угол: {l_system['angle']}")
    print(f"Начальное направление: {l_system['start_direction']}")
    print("Правила:")
    for key, value in l_system["rules"].items():
        print(f"  {key} → {value}")

    points = points_l_system(l_system, iterations, randomness, step_length)

    points = normalize_points(points)

    plt.figure(figsize=(10, 10))
    plt.plot(points[:, 0], points[:, 1], color="darkgreen", linewidth=1)
    plt.title(f"Фрактал: {os.path.basename(filename)} (итераций: {iterations})")
    plt.axis("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_l_system_from_file("Кривая Коха.txt", iterations=5, randomness=0)
    draw_l_system_from_file("Квадратный остров Коха.txt", iterations=5, randomness=0)
    draw_l_system_from_file("Ковёр Серпинского.txt", iterations=5, randomness=0)
    #draw_l_system_from_file("Кривая Гильберта.txt", iterations=5, randomness=0)
    draw_l_system_from_file("Кривая дракона Хартера-Хейтуэя.txt", iterations=15, randomness=0)
    draw_l_system_from_file("Наконечник Серпинского.txt", iterations=7, randomness=0)
    #draw_l_system_from_file("Шестиугольная кривая Госпера.txt", iterations=5, randomness=0)
    #draw_l_system_from_file("Куст 1.txt", iterations=2, randomness=0)
    #draw_l_system_from_file("Куст 2.txt", iterations=5, randomness=0)
    #draw_l_system_from_file("Куст 3.txt", iterations=5, randomness=0)


