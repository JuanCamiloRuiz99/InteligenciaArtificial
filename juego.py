import pygame
import random
from collections import deque

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Serpiente Automática")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Tamaño de la celda (cada bloque de la serpiente y la comida)
cell_size = 20

# Dirección de la serpiente (comienza a moverse a la derecha)
directions = [(0, -cell_size), (0, cell_size), (-cell_size, 0), (cell_size, 0)]  # Arriba, Abajo, Izquierda, Derecha

# Clase para la serpiente
class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]  # La serpiente comienza con 3 segmentos
        self.direction = (cell_size, 0)  # Dirección inicial (hacia la derecha)
        self.alive = True

    def move(self):
        # La cabeza de la serpiente es el primer elemento de la lista
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # Agregar la nueva cabeza a la serpiente
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        # Hacer que la serpiente crezca agregando un nuevo segmento en la cola
        tail_x, tail_y = self.body[-1]
        dir_x, dir_y = self.direction
        new_tail = (tail_x - dir_x, tail_y - dir_y)  # Agregar segmento en la dirección opuesta
        self.body.append(new_tail)

    def check_collision(self):
        # Verificar si la serpiente colisiona con las paredes o consigo misma
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= width or head_y < 0 or head_y >= height:
            self.alive = False  # Colisión con las paredes
        if len(self.body) != len(set(self.body)):
            self.alive = False  # Colisión consigo misma

# Función para generar la comida
def generate_food(snake_body):
    while True:
        food_x = random.randint(0, (width - cell_size) // cell_size) * cell_size
        food_y = random.randint(0, (height - cell_size) // cell_size) * cell_size
        if (food_x, food_y) not in snake_body:
            return (food_x, food_y)

# Función para obtener los vecinos válidos (celdas accesibles)
def get_neighbors(x, y):
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            neighbors.append((nx, ny))
    return neighbors

# Algoritmo de Búsqueda en Anchura (BFS) para encontrar el camino más corto
def bfs(start, goal, snake_body):
    queue = deque([(start, [])])  # (posición actual, camino recorrido)
    visited = set()
    visited.add(start)
    
    while queue:
        (current_x, current_y), path = queue.popleft()

        # Verificar si llegamos a la meta (comida)
        if (current_x, current_y) == goal:
            return path

        for neighbor in get_neighbors(current_x, current_y):
            if neighbor not in visited and neighbor not in snake_body:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []  # Si no hay camino

# Función principal del juego
def game():
    clock = pygame.time.Clock()
    snake = Snake()
    food = generate_food(snake.body)
    path_to_food = []
    
    while snake.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake.alive = False  # Cerrar el juego
                
        # Calcular el camino más corto hacia la comida usando BFS
        head_x, head_y = snake.body[0]
        path_to_food = bfs((head_x, head_y), food, snake.body)
        
        # Si hay un camino, seguir el primer paso de ese camino
        if path_to_food:
            next_move = path_to_food[0]
            if next_move[0] < head_x:
                snake.direction = (-cell_size, 0)  # Mover hacia la izquierda
            elif next_move[0] > head_x:
                snake.direction = (cell_size, 0)  # Mover hacia la derecha
            elif next_move[1] < head_y:
                snake.direction = (0, -cell_size)  # Mover hacia arriba
            elif next_move[1] > head_y:
                snake.direction = (0, cell_size)  # Mover hacia abajo

        # Mover la serpiente
        snake.move()
        
        # Comprobar si la serpiente se comió la comida
        if snake.body[0] == food:
            snake.grow()
            food = generate_food(snake.body)  # Generar nueva comida
            path_to_food = []  # Limpiar el camino hacia la comida
        
        # Verificar colisiones
        snake.check_collision()

        # Rellenar el fondo de la pantalla
        screen.fill(BLACK)

        # Dibujar la serpiente
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], cell_size, cell_size))

        # Dibujar la comida
        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], cell_size, cell_size))

        # Comprobar si la serpiente ha muerto
        if not snake.alive:
            font = pygame.font.SysFont(None, 55)
            text = font.render("Game Over!", True, WHITE)
            screen.blit(text, (width // 3, height // 2))

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad del juego
        clock.tick(10)

    # Espera al cierre del juego
    pygame.quit()

# Iniciar el juego
if __name__ == "__main__":
    game()
