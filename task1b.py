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
                    result.append(char)
                else:
                    result.append(rules[char])
            else:
                result.append(char)
        current_string = "".join(result)

    return current_string


def clamp_color(value):
    return max(0.0, min(1.0, value))


def draw_fractal_tree(l_system, iterations=4, step_length=10.0,
                      initial_thickness=5.0, thickness_decay=0.7,
                      color_transition=0.7, angle_randomness=15.0):
    """
    Parameters:
    - initial_thickness: начальная толщина ствола
    - thickness_decay: коэффициент уменьшения толщины для каждой ветви
    - color_transition: точка перехода от коричневого к зеленому (0-1)
    - angle_randomness: случайное отклонение угла в градусах
    """

    axiom = l_system["atom"]
    base_angle = l_system["angle"]
    direction = l_system["start_direction"]
    rules = l_system["rules"]

    instructions = generate_l_system(axiom, rules, iterations, 0.0)

    fig, ax = plt.subplots(figsize=(10, 12))

    x, y = 0, 0
    stack = []
    current_angle = np.radians(direction)
    current_thickness = initial_thickness
    current_depth = 0
    max_depth = iterations

    for char in instructions:
        if char == "F":
            # Двигаемся вперед с рисованием
            x_new = x + np.sin(current_angle) * step_length
            y_new = y + np.cos(current_angle) * step_length

            # Определяем цвет в зависимости от глубины
            progress = current_depth / max_depth
            if progress < color_transition:
                # Интерполяция от коричневого к светло-коричневому
                brown_color = (0.4, 0.2, 0.0)
                light_brown = (0.6, 0.4, 0.2)
                t = progress / color_transition
                color = (
                    clamp_color(brown_color[0] + t * (light_brown[0] - brown_color[0])),
                    clamp_color(brown_color[1] + t * (light_brown[1] - brown_color[1])),
                    clamp_color(brown_color[2] + t * (light_brown[2] - brown_color[2]))
                )
            else:
                # Интерполяция от светло-коричневого к зеленому
                light_brown = (0.6, 0.4, 0.2)
                green = (0.0, 0.6, 0.0)
                t = (progress - color_transition) / (1 - color_transition)
                color = (
                    clamp_color(light_brown[0] + t * (green[0] - light_brown[0])),
                    clamp_color(light_brown[1] + t * (green[1] - light_brown[1])),
                    clamp_color(light_brown[2] + t * (green[2] - light_brown[2]))
                )

            ax.plot([x, x_new], [y, y_new],
                    color=color,
                    linewidth=current_thickness,
                    solid_capstyle='round')

            x, y = x_new, y_new

        elif char == "f":
            x_new = x + np.sin(current_angle) * step_length
            y_new = y + np.cos(current_angle) * step_length
            x, y = x_new, y_new

        elif char == "+":
            random_offset = np.radians(random.uniform(-angle_randomness, angle_randomness))
            current_angle -= np.radians(base_angle) + random_offset

        elif char == "-":
            random_offset = np.radians(random.uniform(-angle_randomness, angle_randomness))
            current_angle += np.radians(base_angle) + random_offset

        elif char == "[":
            stack.append((x, y, current_angle, current_thickness, current_depth))
            current_thickness *= thickness_decay
            current_depth += 1

        elif char == "]":
            if stack:
                x, y, current_angle, current_thickness, current_depth = stack.pop()

        elif char == "@":
            pass

    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    return fig, ax


def create_fractal_tree_file():
    tree_definition = """X 25 0
X → F[@[-X]+X]"""

    with open("Фрактальное дерево.txt", "w", encoding="utf-8") as f:
        f.write(tree_definition)

    print("Файл 'Фрактальное дерево.txt' создан")


if __name__ == "__main__":
    create_fractal_tree_file()

    l_system = read_l_system_from_file("Фрактальное дерево.txt")

    if l_system is not None:
        print(f"L-система дерева:")
        print(f"Атом: {l_system['atom']}")
        print(f"Угол: {l_system['angle']}")
        print(f"Начальное направление: {l_system['start_direction']}")
        print("Правила:")
        for key, value in l_system["rules"].items():
            print(f"  {key} → {value}")


        fig1, ax1 = draw_fractal_tree(l_system, iterations=7, step_length=15.0,
                                      initial_thickness=8.0, thickness_decay=0.6,
                                      color_transition=0.6, angle_randomness=10.0)
        ax1.set_title("Фрактальное дерево (стандартное)")
        plt.show()

        fig2, ax2 = draw_fractal_tree(l_system, iterations=7, step_length=12.0,
                                      initial_thickness=6.0, thickness_decay=0.65,
                                      color_transition=0.5, angle_randomness=20.0)
        ax2.set_title("Фрактальное дерево (более случайное)")
        plt.show()

        fig3, ax3 = draw_fractal_tree(l_system, iterations=7, step_length=14.0,
                                      initial_thickness=7.0, thickness_decay=0.7,
                                      color_transition=0.99, angle_randomness=15.0)
        ax3.set_title("Фрактальное дерево (плавный переход цвета)")
        plt.show()

    else:
        print("Не удалось загрузить L-систему дерева")