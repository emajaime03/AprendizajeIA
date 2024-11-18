import pygame
import sys

# Inicializar Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Crear pantalla
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')

# Fuente
font = pygame.font.SysFont(None, 60)
message_font = pygame.font.SysFont(None, 50)  # Fuente para el mensaje de ganador o empate
button_font = pygame.font.SysFont(None, 40)  # Fuente para el botón de reinicio

# Tablero vacío
board = ['_' for _ in range(9)]
winner = None  # Almacena al ganador, si lo hay
draw = False  # Variable para detectar empate

# Dibujar el tablero de Tic-Tac-Toe
def draw_board():
    screen.fill(WHITE)
    # Dibujar líneas verticales
    pygame.draw.line(screen, BLACK, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), LINE_WIDTH)
    # Dibujar líneas horizontales
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), LINE_WIDTH)

# Dibujar X y O
def draw_x_o():
    for i in range(9):
        if board[i] == 'X':
            draw_x(i)
        elif board[i] == 'O':
            draw_o(i)

# Dibujar X en una celda
def draw_x(index):
    x = index % 3 * WIDTH // 3 + WIDTH // 6
    y = index // 3 * HEIGHT // 3 + HEIGHT // 6
    pygame.draw.line(screen, RED, (x - 50, y - 50), (x + 50, y + 50), LINE_WIDTH)
    pygame.draw.line(screen, RED, (x + 50, y - 50), (x - 50, y + 50), LINE_WIDTH)

# Dibujar O en una celda
def draw_o(index):
    x = index % 3 * WIDTH // 3 + WIDTH // 6
    y = index // 3 * HEIGHT // 3 + HEIGHT // 6
    pygame.draw.circle(screen, BLUE, (x, y), 50, LINE_WIDTH)

# Verificar si hay un ganador
def check_winner(board):
    winning_combinations = [
        [board[0], board[1], board[2]],
        [board[3], board[4], board[5]],
        [board[6], board[7], board[8]],
        [board[0], board[3], board[6]],
        [board[1], board[4], board[7]],
        [board[2], board[5], board[8]],
        [board[0], board[4], board[8]],
        [board[2], board[4], board[6]]
    ]
    for combo in winning_combinations:
        if combo[0] == combo[1] == combo[2] and combo[0] != '_':
            return combo[0]
    return None

# MiniMax para IA
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif '_' not in board:
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == '_':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = '_'
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == '_':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = '_'
                best_score = min(score, best_score)
        return best_score

# IA elige la mejor jugada
def best_move():
    best_score = -float('inf')
    move = None
    for i in range(9):
        if board[i] == '_':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = '_'
            if score > best_score:
                best_score = score
                move = i
    print(f"Best score: {best_score}")
    print(f"Best move: {move}")
    return move

# Manejador del clic del jugador
def handle_click(x, y):
    global winner, draw
    row = y // (HEIGHT // 3)
    col = x // (WIDTH // 3)
    index = row * 3 + col
    if board[index] == '_' and winner is None:  # Solo permite movimiento si no hay ganador
        board[index] = 'X'
        winner = check_winner(board)  # Verifica si el jugador ganó
        if winner is None and '_' in board:
            move = best_move()
            if move is not None:
                board[move] = 'O'
                winner = check_winner(board)  # Verifica si la IA ganó
            elif '_' not in board:
                draw = True  # Si no hay movimientos posibles, es empate
        elif '_' not in board:
            draw = True

# Reiniciar el juego
def reset_game():
    global board, winner, draw
    board = ['_' for _ in range(9)]
    winner = None
    draw = False

# Mostrar mensaje de ganador o empate
def display_message():
    screen.fill(WHITE)  # Limpia la pantalla
    if winner:
        message = f'Ganador "{winner}"'
    elif draw:
        message = 'Empate'
    else:
        return
    text = message_font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    screen.blit(text, text_rect)

    # Dibujar el botón de "Volver a Jugar"
    button_text = button_font.render("Reiniciar", True, WHITE)
    button_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 30, 140, 50)
    pygame.draw.rect(screen, GRAY, button_rect)
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))
    return button_rect  # Devuelve el rectángulo del botón para detección de clics

# Loop principal del juego
running = True
while running:
    if winner or draw:  # Si hay un ganador o empate, muestra el mensaje
        button_rect = display_message()  # Obtener rectángulo del botón
    else:
        draw_board()
        draw_x_o()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if winner or draw:
                # Verificar si el clic está en el botón de "Volver a Jugar"
                if button_rect.collidepoint(x, y):
                    reset_game()
            else:
                handle_click(x, y)
    
    pygame.display.update()

pygame.quit()
sys.exit()
