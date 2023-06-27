import pygame
import random

# Configuración
TILE_SIZE = 20
WIDTH = 40
HEIGHT = 30
SCREEN_WIDTH = TILE_SIZE * WIDTH
SCREEN_HEIGHT = TILE_SIZE * HEIGHT
NUM_ROOMS = 10
MIN_ROOM_SIZE = 3
MAX_ROOM_SIZE = 8

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Configuraciones para el boton
# Al principio del script (junto con otras configuraciones)
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 40
BUTTON_X = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = SCREEN_HEIGHT - 60
BUTTON_COLOR = (255, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)
# Inicializar Pygame
pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Generator")

# Clase de habitación
class Room:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        pygame.draw.rect(window, BLUE, (self.x * TILE_SIZE, self.y * TILE_SIZE, self.w * TILE_SIZE, self.h * TILE_SIZE), 0)

    def center(self):
        center_x = self.x + self.w // 2
        center_y = self.y + self.h // 2
        return center_x, center_y

    def intersects(self, other):
        return (self.x < other.x + other.w and self.x + self.w > other.x and
                self.y < other.y + other.h and self.y + self.h > other.y)

# Función para calcular la distancia entre dos puntos
def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

# Función para conectar dos habitaciones con corredores
def connect_rooms(room1, room2):
    x1, y1 = room1.center()
    x2, y2 = room2.center()
    # Horizontalmente primero
    for x in range(min(x1, x2), max(x1, x2) + 1):
        pygame.draw.rect(window, GREEN, (x * TILE_SIZE, y1 * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    # Luego verticalmente
    for y in range(min(y1, y2), max(y1, y2) + 1):
        pygame.draw.rect(window, GREEN, (x2 * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def generate_rooms():
    rooms = []
    for _ in range(NUM_ROOMS):
        w = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        h = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        x = random.randint(1, WIDTH - w - 1)
        y = random.randint(1, HEIGHT - h - 1)

        new_room = Room(x, y, w, h)
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        rooms.append(new_room)
    return rooms



# Conectar habitaciones usando algoritmo simplificado de Prim

# Mantener ventana abierta
while True:
    pygame.draw.rect(window, BUTTON_COLOR, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    font = pygame.font.Font(None, 36)
    text = font.render('Generate Dungeon', True, BUTTON_TEXT_COLOR)
    window.blit(text, (BUTTON_X + 10, BUTTON_Y + 5))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                # Borra la pantalla
                window.fill((0, 0, 0))
                # Genera y dibuja nuevas habitaciones
                rooms = generate_rooms()
                for room in rooms:
                    room.draw()
                # Reconecta las habitaciones usando algoritmo de Prim
                connected_rooms = [rooms[0]]
                remaining_rooms = set(rooms[1:])
                while remaining_rooms:
                    closest_room = None
                    room_to_connect = None
                    closest_distance = float('inf')
                    for room in connected_rooms:
                        for other_room in remaining_rooms:
                            dist = distance(room.center(), other_room.center())
                            if dist < closest_distance:
                                closest_distance = dist
                                closest_room = other_room
                                room_to_connect = room
                    if closest_room:
                        connect_rooms(room_to_connect, closest_room)
                        connected_rooms.append(closest_room)
                        remaining_rooms.remove(closest_room)

    pygame.display.update()
