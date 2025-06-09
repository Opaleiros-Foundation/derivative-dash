import pygame
import math
import sys
import random
import numpy as np

# Inicialização
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Derivative Dash - Cálculo 2 (1ª e 2ª derivadas)")

# Cores
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (200, 50, 50)
BLUE = (50, 100, 200)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Fontes
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 30)

# =============================================
# BIBLIOTECA DE FUNÇÕES PARA O JOGO
# =============================================
FUNCTIONS = [
    {
        "name": "Senoide",
        "formula": "f(x) = 50·sen(0.01x) + 0.001x² + 300",
        "f": lambda x: 50 * math.sin(0.01 * x) + 0.001 * x**2 + 300,
        "df": lambda x: 0.5 * math.cos(0.01 * x) + 0.002 * x,
        "d2f": lambda x: -0.005 * math.sin(0.01 * x) + 0.002,
        "range": (0, 1000),
        "checkpoints": 4
    },
    {
        "name": "Logística",
        "formula": "f(x) = 400 / (1 + e^(-0.01(x - 500)))",
        "f": lambda x: 400 / (1 + math.exp(-0.01*(x - 500))),
        "df": lambda x: (4 * math.exp(-0.01*(x - 500))) / (1 + math.exp(-0.01*(x - 500)))**2,
        "d2f": lambda x: (-0.04 * math.exp(-0.01*(x-500)) * (1 - math.exp(-0.01*(x-500)))) / (1 + math.exp(-0.01*(x-500)))**3,
        "range": (0, 1000),
        "checkpoints": 4
    },
    {
        "name": "Polinômio Cúbico",
        "formula": "f(x) = 0.00001x³ - 0.015x² + 5x + 300",
        "f": lambda x: 0.00001 * x**3 - 0.015 * x**2 + 5 * x + 300,
        "df": lambda x: 0.00003 * x**2 - 0.03 * x + 5,
        "d2f": lambda x: 0.00006 * x - 0.03,
        "range": (0, 1000),
        "checkpoints": 4
    }
]

# =============================================
# FUNÇÕES DE DESENHO E LÓGICA
# =============================================
def create_car_surface(color=BLUE):
    car = pygame.Surface((60, 30), pygame.SRCALPHA)
    pygame.draw.rect(car, color, (0, 5, 60, 20), border_radius=5)
    pygame.draw.rect(car, BLACK, (10, 0, 15, 5))
    pygame.draw.rect(car, BLACK, (35, 0, 15, 5))
    pygame.draw.rect(car, BLACK, (10, 25, 15, 5))
    pygame.draw.rect(car, BLACK, (35, 25, 15, 5))
    pygame.draw.rect(car, YELLOW, (50, 10, 10, 10))
    return car

def draw_track():
    points = []
    step = max(1, TRACK_LENGTH // 500)
    for x in range(FUNC_RANGE[0], FUNC_RANGE[1], step):
        y = f(x)
        screen_y = HEIGHT - (y - game.camera_y)
        points.append((x - game.camera_x, screen_y))
    if len(points) > 1:
        pygame.draw.lines(screen, GRAY, False, points, 12)
        pygame.draw.lines(screen, BLACK, False, points, 2)

def draw_checkpoints():
    for i, checkpoint in enumerate(game.checkpoints):
        checkpoint_x = checkpoint["x"]
        y = f(checkpoint_x)
        pos = (checkpoint_x - game.camera_x, HEIGHT - (y - game.camera_y))
        if -50 < pos[0] < WIDTH + 50:
            # Cor baseada no tipo de derivada e status
            if checkpoint["type"] == "first":
                base_color = GREEN
            else:
                base_color = PURPLE
            
            if i < game.checkpoints_passed:
                color = base_color
            elif i == game.checkpoints_passed:
                color = ORANGE
            else:
                color = RED
            
            pygame.draw.circle(screen, color, pos, 12, 2 if i > game.checkpoints_passed else 0)
            
            # Adiciona indicador do tipo de derivada
            symbol = font.render("f'" if checkpoint["type"] == "first" else "f''", True, BLACK)
            screen.blit(symbol, (pos[0] - symbol.get_width()//2, pos[1] - symbol.get_height()//2))

# =============================================
# LÓGICA DO JOGO
# =============================================
class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        global current_func, f, df, d2f, FUNC_RANGE, TOTAL_CHECKPOINTS, TRACK_LENGTH
        current_func = random.choice(FUNCTIONS)
        f = current_func["f"]
        df = current_func["df"]
        d2f = current_func["d2f"]
        FUNC_RANGE = current_func["range"]
        TOTAL_CHECKPOINTS = current_func["checkpoints"]
        TRACK_LENGTH = FUNC_RANGE[1] - FUNC_RANGE[0]

        self.car_x = FUNC_RANGE[0] + 50
        self.camera_x = 0
        self.camera_y = f(self.car_x) - HEIGHT // 2
        self.speed = 2.0
        self.max_speed = 8.0
        self.input_mode = False
        self.input_text = ''
        self.message = ''
        self.message_time = 0
        self.score = 0
        self.game_over = False
        self.crashed = False
        self.victory = False
        self.car_surface = create_car_surface()
        self.skid_marks = []
        self.checkpoints_passed = 0

        # Cria checkpoints alternando entre primeira e segunda derivadas
        spacing = TRACK_LENGTH / (TOTAL_CHECKPOINTS + 1)
        self.checkpoints = []
        for i in range(TOTAL_CHECKPOINTS):
            checkpoint_x = FUNC_RANGE[0] + (i+1) * spacing
            # Alterna entre primeira e segunda derivada
            deriv_type = "first" if i % 2 == 0 else "second"
            self.checkpoints.append({"x": checkpoint_x, "type": deriv_type})
        
        self.next_checkpoint = self.checkpoints[0]
        self.waiting_at_checkpoint = False

    def check_answer(self):
        try:
            user_value = float(self.input_text)
            
            if self.next_checkpoint["type"] == "first":
                real_value = df(self.next_checkpoint["x"])
                error = abs(user_value - real_value)
                threshold = 0.5  # Tolerância para primeira derivada
            else:
                real_value = d2f(self.next_checkpoint["x"])
                error = abs(user_value - real_value)
                threshold = 0.1  # Tolerância mais estrita para segunda derivada

            if error < threshold:
                self.message = "✓ Correto! Continue!"
                self.speed = 2.0
                self.score += 100 if self.next_checkpoint["type"] == "first" else 150  # Bônus para segunda derivada
                self.waiting_at_checkpoint = False
                self.input_mode = False
                self.checkpoints_passed += 1

                if self.checkpoints_passed < TOTAL_CHECKPOINTS:
                    self.next_checkpoint = self.checkpoints[self.checkpoints_passed]
                else:
                    self.next_checkpoint = {"x": FUNC_RANGE[1], "type": "none"}
            else:
                self.message = f"✗ Errado! Valor correto: {real_value:.2f}"
                self.speed = 0
                self.game_over = True
                self.crashed = True
                self.car_surface = create_car_surface(RED)
            self.input_text = ''
            self.message_time = pygame.time.get_ticks()
        except ValueError:
            self.message = "Digite um número válido!"
            self.message_time = pygame.time.get_ticks()

# =============================================
# LOOP PRINCIPAL
# =============================================
game = GameState()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game.game_over and game.input_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game.check_answer()
                elif event.key == pygame.K_BACKSPACE:
                    game.input_text = game.input_text[:-1]
                else:
                    game.input_text += event.unicode

    screen.fill(WHITE)

    if not game.game_over and not game.waiting_at_checkpoint:
        game.car_x += game.speed
        car_y = f(game.car_x)
        game.camera_x = max(0, game.car_x - WIDTH//3)
        game.camera_y = car_y - HEIGHT // 2

        if game.car_x >= game.next_checkpoint["x"] - 10 and not game.input_mode:
            game.car_x = game.next_checkpoint["x"]
            game.speed = 0
            game.waiting_at_checkpoint = True
            game.input_mode = True
            if game.next_checkpoint["type"] == "first":
                game.message = f"Qual a derivada f' em x ≈ {int(game.next_checkpoint['x'])}?"
            else:
                game.message = f"Qual a segunda derivada f'' em x ≈ {int(game.next_checkpoint['x'])}?"
            game.message_time = pygame.time.get_ticks()

        if game.car_x >= FUNC_RANGE[1] - 50:
            game.car_x = FUNC_RANGE[1] - 50
            game.speed = 0
            if game.checkpoints_passed == TOTAL_CHECKPOINTS:
                game.victory = True
                game.message = f"🏁 VITÓRIA! Pontuação: {game.score}"
            else:
                game.message = "Fim da pista! Você não completou todos os checkpoints!"
            game.game_over = True

    draw_track()
    draw_checkpoints()

    car_y = f(game.car_x)
    angle = math.degrees(math.atan(-df(game.car_x)))
    rotated_car = pygame.transform.rotate(game.car_surface, angle)
    screen.blit(rotated_car, (game.car_x - game.camera_x - rotated_car.get_width()//2,
                              HEIGHT - (car_y - game.camera_y) - rotated_car.get_height()//2))

    info_text = [
        f"Função: {current_func['name']}",
        f"Equação: {current_func['formula']}",
        f"Velocidade: {game.speed:.1f}",
        f"Checkpoints: {game.checkpoints_passed}/{TOTAL_CHECKPOINTS}",
        f"Pontuação: {game.score}",
    ]

    for i, text in enumerate(info_text):
        screen.blit(font.render(text, True, BLACK), (10, 10 + i * 25))

    if pygame.time.get_ticks() - game.message_time < 5000 or game.game_over:
        msg_color = GREEN if "✓" in game.message or game.victory else RED
        msg_surface = large_font.render(game.message, True, msg_color)
        screen.blit(msg_surface, (WIDTH//2 - msg_surface.get_width()//2, 50))

    if game.input_mode and not game.game_over:
        input_bg = pygame.Rect(WIDTH//2 - 160, HEIGHT - 70, 320, 40)
        pygame.draw.rect(screen, (240, 240, 240), input_bg, border_radius=5)
        pygame.draw.rect(screen, BLUE, input_bg, 2, border_radius=5)
        
        if game.next_checkpoint["type"] == "first":
            prompt_text = f"Derivada f' em x ≈ {int(game.next_checkpoint['x'])}:"
        else:
            prompt_text = f"Segunda derivada f'' em x ≈ {int(game.next_checkpoint['x'])}:"
            
        prompt = font.render(prompt_text, True, (100, 100, 100))
        screen.blit(prompt, (WIDTH//2 - 150, HEIGHT - 120))
        input_text = font.render(game.input_text, True, BLACK)
        screen.blit(input_text, (WIDTH//2 - 50, HEIGHT - 60))

    if game.game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        if game.crashed:
            result_text = large_font.render("VOCÊ BATEU!", True, RED)
            screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2 - 50))
        elif game.victory:
            result_text = large_font.render("VITÓRIA!", True, GREEN)
            screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2 - 50))
        score_text = large_font.render(f"Pontuação final: {game.score}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        restart_text = font.render("Pressione R para jogar novamente", True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game.reset()

    pygame.display.flip()
    clock.tick(60)