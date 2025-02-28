import pygame
import random
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman et la rivière quantique")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
LIGHT_RED = (255, 102, 102)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
DARK_GRAY = (64, 64, 64)
LIGHT_BLUE = (173, 216, 230)

# Police
font = pygame.font.Font(None, 24)

# Position du stickman
stickman_x, stickman_y = WIDTH // 2, HEIGHT - 150
stickman_speed = 5

# Position et animation de la rivière
river_color = BLUE
wave_phase = 0
wave_lines = [[random.randint(5, 15) for _ in range(WIDTH // 10)] for _ in range(20)]
wave_color = LIGHT_BLUE
particles = []  # Liste des particules
particle_elements = []  # Liste des éléments affichés dans les particules

# Taille des particules
particle_size = 20

def draw_stickman(x, y):
    pygame.draw.circle(screen, BLACK, (x, y - 30), 15)
    pygame.draw.line(screen, BLACK, (x, y - 15), (x, y + 30), 5)
    pygame.draw.line(screen, BLACK, (x - 20, y), (x + 20, y), 5)
    pygame.draw.line(screen, BLACK, (x, y + 30), (x - 15, y + 60), 5)
    pygame.draw.line(screen, BLACK, (x, y + 30), (x + 15, y + 60), 5)

def draw_river():
    global wave_phase
    wave_phase += 0.1
    pygame.draw.rect(screen, river_color, (0, HEIGHT // 2, WIDTH, HEIGHT // 3))
    for j, line in enumerate(wave_lines):
        for i in range(len(line)):
            offset = 10 * math.sin(i * 0.5 + wave_phase + j * 0.3)
            pygame.draw.ellipse(screen, wave_color, (i * 10, HEIGHT // 2 + j * 10 + offset, 20, 10))

def draw_particles():
    for p in particles:
        pygame.draw.circle(screen, WHITE, (int(p[0]), int(p[1])), particle_size)
        text_surface = font.render(p[2], True, BLACK)
        text_rect = text_surface.get_rect(center=(p[0], p[1]))
        screen.blit(text_surface, text_rect)

def check_water():
    global river_color, wave_color, message, particle_elements, particles
    rand = random.random()
    if rand < 0.2:
        river_color = GREEN
        wave_color = (0, 100, 0)
        message = "L'eau est polluée (algues)."
        particle_elements = ["N", "P", "O"]
    elif rand < 0.4:
        river_color = LIGHT_RED
        wave_color = (200, 50, 50)
        message = "L'eau est radioactive !"
        particle_elements = ["U", "Ra", "Po"]
    elif rand < 0.6:
        river_color = PURPLE
        wave_color = (100, 0, 100)
        message = "L'eau est contaminée par un virus !"
        particle_elements = ["COVID-19", "EBOLA", "RNA", "DNA"]
    elif rand < 0.75:
        river_color = BROWN
        wave_color = (80, 40, 20)
        message = "L'eau est boueuse."
        particle_elements = ["Fe", "Mg", "Ca"]
    elif rand < 0.9:
        river_color = YELLOW
        wave_color = (200, 200, 0)
        message = "L'eau contient des produits chimiques !"
        particle_elements = ["Hg", "Pb", "Cl"]
    else:
        river_color = BLUE
        wave_color = LIGHT_BLUE
        message = "L'eau est potable."
        particle_elements = ["H", "O"]
    
    particles = [[WIDTH - random.randint(0, WIDTH // 4), HEIGHT // 2 + j * 10 + random.randint(-5, 5), random.choice(particle_elements)] for j in range(len(wave_lines))]
    
    # Éviter que les particules se chevauchent
    seen_positions = set()
    for p in particles:
        while (int(p[0]), int(p[1])) in seen_positions:
            p[0] -= random.randint(5, 15)  # Décaler légèrement vers la gauche
            p[1] += random.randint(-5, 5)  # Décaler légèrement en hauteur
        seen_positions.add((int(p[0]), int(p[1])))

# Texte d'information
message = "Cliquez sur la rivière pour analyser l'eau."
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0, HEIGHT // 2 + 100, WIDTH, HEIGHT // 2))  # Sol
    draw_river()
    draw_particles()
    draw_stickman(stickman_x, stickman_y)
    text_surface = font.render(message, True, BLACK)
    screen.blit(text_surface, (20, 20))
    
    pygame.display.flip()
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if HEIGHT // 2 < event.pos[1] < HEIGHT // 2 + 100:
                check_water()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and stickman_x > 20:
        stickman_x -= stickman_speed
    if keys[pygame.K_RIGHT] and stickman_x < WIDTH - 20:
        stickman_x += stickman_speed
    if keys[pygame.K_UP] and stickman_y > 100:
        stickman_y -= stickman_speed
    if keys[pygame.K_DOWN] and stickman_y < HEIGHT - 50:
        stickman_y += stickman_speed
    
    for p in particles:
        p[0] -= random.randint(1, 3)
        p[1] += random.choice([-1, 1]) + random.uniform(-0.5, 0.5)
    
    particles = [p for p in particles if p[0] > 0]

pygame.quit()