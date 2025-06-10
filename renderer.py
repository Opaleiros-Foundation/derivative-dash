import pygame
from config import *

def create_car_surface(color=BLUE):
    car = pygame.Surface((60, 30), pygame.SRCALPHA)
    pygame.draw.rect(car, color, (0, 5, 60, 20), border_radius=5)
    pygame.draw.rect(car, BLACK, (10, 0, 15, 5))
    pygame.draw.rect(car, BLACK, (35, 0, 15, 5))
    pygame.draw.rect(car, BLACK, (10, 25, 15, 5))
    pygame.draw.rect(car, BLACK, (35, 25, 15, 5))
    pygame.draw.rect(car, YELLOW, (50, 10, 10, 10))
    return car

def draw_track(screen, game, f, FUNC_RANGE, TRACK_LENGTH):
    points = []
    step = max(1, TRACK_LENGTH // 500)
    for x in range(FUNC_RANGE[0], FUNC_RANGE[1], step):
        y = f(x)
        screen_y = HEIGHT - (y - game.camera_y)
        points.append((x - game.camera_x, screen_y))
    if len(points) > 1:
        pygame.draw.lines(screen, GRAY, False, points, 12)
        pygame.draw.lines(screen, BLACK, False, points, 2)

def draw_checkpoints(screen, game, f):
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

def draw_car(screen, game, car_y, df):
    angle = pygame.math.Vector2(1, 0).angle_to(pygame.math.Vector2(1, df(game.car_x)))
    rotated_car = pygame.transform.rotate(game.car_surface, angle)
    screen.blit(rotated_car, (game.car_x - game.camera_x - rotated_car.get_width()//2,
                           HEIGHT - (car_y - game.camera_y) - rotated_car.get_height()//2))

def draw_hud(screen, game, current_func, TOTAL_CHECKPOINTS):
    # Informações do jogo
    info_text = [
        f"Função: {current_func['name']}",
        f"Equação: {current_func['formula']}",
        f"Velocidade: {game.speed:.1f}",
        f"Checkpoints: {game.checkpoints_passed}/{TOTAL_CHECKPOINTS}",
        f"Pontuação: {game.score}",
    ]

    for i, text in enumerate(info_text):
        screen.blit(font.render(text, True, BLACK), (10, 10 + i * 25))

    # Mensagem na tela
    if pygame.time.get_ticks() - game.message_time < 5000 or game.game_over:
        msg_color = GREEN if "✓" in game.message or game.victory else RED
        msg_surface = large_font.render(game.message, True, msg_color)
        screen.blit(msg_surface, (WIDTH//2 - msg_surface.get_width()//2, 50))

    # Caixa de entrada de resposta
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

    # Tela de game over
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