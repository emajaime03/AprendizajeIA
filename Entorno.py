import pygame
import sys
import numpy as np
import random

# Inicializar Pygame
pygame.init()

# Configuraciones de la pantalla
WIDTH, HEIGHT = 320, 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laberinto Q-Learning")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Configuración del Cuadrado y el laberinto
square_size = 10
start_pos = [10, 10]
goal_pos = [WIDTH - square_size, HEIGHT - square_size]
goal_rect = pygame.Rect(goal_pos[0], goal_pos[1], square_size, square_size)
line_width = 3

# Definir las líneas del laberinto
maze_lines = [
    (40, 120, 40, 200),
    (80, 40, 160, 40),
    (160, 0, 160, 40),
    (200, 40, 200, 80),
    (240, 0, 240, 40),
    (280, 40, 280, 80),
    (120, 80, 200, 80),
    (160, 120, 320, 120),
    (0, 200, 40, 200),
    (240, 80, 280, 80),
    (240, 80, 240, 120),
    (120, 80, 120, 120),
    (0, 40, 40, 40),
    (40, 40, 40, 80),
    (40, 80, 80, 80),
    (40, 120, 120, 120),
    (160, 120, 160, 160),
    (80, 160, 240, 160),
    (80, 160, 80, 200),
    (80, 200, 160, 200),
    (160, 200, 160, 280),
    (80, 280, 160, 280),
    (40, 240, 120, 240),
    (40, 240, 40, 320),
    (200, 200, 200, 320),
    (200, 200, 240, 200),
    (280, 160, 280, 240),
    (240, 240, 280, 240),
    (240, 240, 240, 280),
    (240, 280, 320, 280),
]

# Parámetros de Q-Learning
actions = ["left", "right", "up", "down"]
q_table = np.zeros((WIDTH // square_size, HEIGHT // square_size, len(actions)))
learning_rate = 0.1
discount_factor = 0.9
epsilon = 1.0
epsilon_decay = 0.995
min_epsilon = 0.01
episodes = 5000

# Variables para rastrear el mejor intento
best_reward = -float('inf')
best_episode_steps = []

# Función para verificar colisión
def check_collision(pos):
    square_rect = pygame.Rect(pos[0], pos[1], square_size, square_size)
    for x1, y1, x2, y2 in maze_lines:
        line_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1) + line_width, abs(y2 - y1) + line_width)
        if square_rect.colliderect(line_rect):
            return True
    return False

# Función para seleccionar acción usando la política epsilon-greedy
def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.choice(range(len(actions)))  # Exploración
    else:
        return np.argmax(q_table[state])  # Explotación

# Función para ejecutar un paso
def take_step(state, action):
    x, y = state
    if action == 0:  # Left
        x -= 1
    elif action == 1:  # Right
        x += 1
    elif action == 2:  # Up
        y -= 1
    elif action == 3:  # Down
        y += 1

    new_pos = [x * square_size, y * square_size]
    if 0 <= x < WIDTH // square_size and 0 <= y < HEIGHT // square_size and not check_collision(new_pos):
        return (x, y), -1  # Movimiento válido, pequeña penalización
    return state, -10  # Colisión, penalización fuerte

# Entrenamiento del agente con visualización en tiempo real
for episode in range(episodes):
    state = (start_pos[0] // square_size, start_pos[1] // square_size)
    done = False
    total_reward = 0
    episode_steps = []

    while not done:
        # Dibuja el laberinto y el agente en la pantalla
        screen.fill(WHITE)
        for x1, y1, x2, y2 in maze_lines:
            pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), line_width)
        pygame.draw.rect(screen, BLUE, (start_pos[0], start_pos[1], square_size, square_size))
        pygame.draw.rect(screen, GREEN, (goal_pos[0], goal_pos[1], square_size, square_size))
        pygame.draw.rect(screen, RED, (state[0] * square_size, state[1] * square_size, square_size, square_size))

        # Actualizar pantalla y verificar eventos de salida
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Seleccionar y ejecutar acción
        action = choose_action(state)
        next_state, reward = take_step(state, action)
        total_reward += reward
        episode_steps.append(state)

        # Verificar condición de victoria (dentro del cuadrado verde)
        if goal_rect.contains(pygame.Rect(next_state[0] * square_size, next_state[1] * square_size, square_size, square_size)):
            reward = 100
            done = True

        # Actualizar la Q-table
        q_table[state][action] = q_table[state][action] + learning_rate * (reward + discount_factor * np.max(q_table[next_state]) - q_table[state][action])
        state = next_state

    # Reducir epsilon para disminuir exploración
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

    # Guardar el mejor intento
    if total_reward > best_reward:
        best_reward = total_reward
        best_episode_steps = episode_steps

    # Mostrar progreso cada 100 episodios
    if (episode + 1) % 100 == 0:
        print(f"Episodio {episode + 1}, Recompensa del mejor episodio: {best_reward}")

# Visualización del mejor intento en bucle
def visualize_best_attempt():
    clock = pygame.time.Clock()
    while True:  # Bucle para repetir visualización
        for step in best_episode_steps:
            screen.fill(WHITE)
            for x1, y1, x2, y2 in maze_lines:
                pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), line_width)
            pygame.draw.rect(screen, BLUE, (start_pos[0], start_pos[1], square_size, square_size))
            pygame.draw.rect(screen, GREEN, (goal_pos[0], goal_pos[1], square_size, square_size))
            pygame.draw.rect(screen, RED, (step[0] * square_size, step[1] * square_size, square_size, square_size))

            pygame.display.flip()
            clock.tick(5)  # Velocidad de visualización ajustable

# Ejecutar visualización del mejor intento
visualize_best_attempt()