import pygame
import math
from config import *

def create_game_icon():
    """
    Cria um ícone estilizado para a janela do jogo.
    
    Returns:
        pygame.Surface: Ícone do jogo
    """
    # Criar uma superfície 32x32 com canal alpha
    icon = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # Gradiente de fundo circular (simplificado)
    pygame.draw.circle(icon, BLUE, (16, 16), 16)
    
    # Simular uma curva/gráfico - similar ao arquivo SVG
    points = [(8, 16), (12, 12), (16, 16), (20, 20), (24, 16)]
    pygame.draw.lines(icon, GREEN, False, points, 2)
    
    # Simulação do carro
    pygame.draw.rect(icon, RED, (14, 13, 8, 4), border_radius=1)
    
    # Pequenas rodas
    pygame.draw.circle(icon, BLACK, (15, 18), 1)
    pygame.draw.circle(icon, BLACK, (21, 18), 1)
    
    return icon

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
    
    # Calcular a posição Y na tela
    screen_y = HEIGHT - (car_y - game.camera_y) - rotated_car.get_height()//2
    
    # Definir um limite mínimo para o topo (para não ficar atrás do header)
    min_y = 100  # Ajuste este valor conforme necessário para ficar abaixo do header
    screen_y = max(screen_y, min_y)
    
    screen.blit(rotated_car, (game.car_x - game.camera_x - rotated_car.get_width()//2, screen_y))

def create_icon_surface(icon_type, size=24):
    """Cria uma superfície com um ícone simples"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    if icon_type == "function":
        # Ícone de gráfico
        pygame.draw.line(surface, BLUE, (2, size//2), (size-2, size//2), 2)
        pygame.draw.line(surface, BLUE, (size//2, 2), (size//2, size-2), 2)
        # Curva simples
        points = [(2, size//2), (size//3, size//4), (2*size//3, 3*size//4), (size-2, size//2)]
        pygame.draw.lines(surface, GREEN, False, points, 2)
        
    elif icon_type == "speed":
        # Ícone de velocímetro
        pygame.draw.circle(surface, BLUE, (size//2, size//2), size//2-2, 2)
        pygame.draw.line(surface, RED, (size//2, size//2), (size//2 + size//3, size//2 - size//3), 2)
        
    elif icon_type == "checkpoint":
        # Ícone de checkpoint/bandeira
        pygame.draw.rect(surface, BLACK, (2, 2, 2, size-4), 2)
        flag_points = [(6, 4), (size-2, 4), (size-6, size//2-2), (6, size//2-2)]
        pygame.draw.polygon(surface, ORANGE, flag_points)
        
    elif icon_type == "score":
        # Ícone de troféu/pontuação
        # Base do troféu
        pygame.draw.rect(surface, ORANGE, (size//2-size//6, 3*size//4, size//3, size//4))
        # Corpo do troféu
        pygame.draw.rect(surface, YELLOW, (size//2-size//3, size//4, 2*size//3, size//2), 0, 3)
        # Alças
        pygame.draw.arc(surface, YELLOW, (size//2-size//2, size//4, size//3, size//3), 0, 3.14, 2)
        pygame.draw.arc(surface, YELLOW, (size//2+size//6, size//4, size//3, size//3), 0, 3.14, 2)
        
    elif icon_type == "equation":
        # Ícone de equação matemática
        pygame.draw.line(surface, BLACK, (4, 8), (size-4, 8), 2)
        pygame.draw.line(surface, BLACK, (4, size//2), (size-4, size//2), 2)
        pygame.draw.line(surface, BLACK, (4, size-8), (size-8, size-8), 2)
        # Símbolos matemáticos
        text_f = pygame.font.SysFont("Arial", size//2).render("f(x)", True, BLUE)
        surface.blit(text_f, (size//2 - text_f.get_width()//2, 2))
    
    return surface

def draw_hud(screen, game, current_func, TOTAL_CHECKPOINTS):
    # Fundo semitransparente para o HUD
    hud_height = 90
    hud_bg = pygame.Surface((WIDTH, hud_height), pygame.SRCALPHA)
    hud_bg.fill((240, 240, 240, 230))  # Cor de fundo com transparência
    screen.blit(hud_bg, (0, 0))
    
    # Linha separadora
    pygame.draw.line(screen, (200, 200, 200), (0, hud_height), (WIDTH, hud_height), 2)
    
    # Layout dividido em zonas
    icon_size = 24
    
    # ZONA 1: Informações da função (à esquerda)
    # Nome da função e equação - ocupam 60% da largura
    function_zone_width = WIDTH * 0.6
    
    # Nome da função
    func_icon = create_icon_surface("function", size=icon_size)
    screen.blit(func_icon, (20, 15))
    
    func_name = font.render(current_func['name'], True, BLACK)
    screen.blit(func_name, (20 + icon_size + 8, 15 + icon_size//2 - func_name.get_height()//2))
    
    # Equação - Com tratamento para equações longas
    eq_icon = create_icon_surface("equation", size=icon_size)
    screen.blit(eq_icon, (20, 50))
    
    eq_text = current_func['formula']
    # Limita o tamanho da equação para evitar sobreposição
    max_eq_width = function_zone_width - 60  # Espaço para o ícone e margem
    eq_rendered = font.render(eq_text, True, BLACK)
    
    if eq_rendered.get_width() > max_eq_width:
        # Tenta encurtar a equação
        eq_text = eq_text[:30] + "..."
        eq_rendered = font.render(eq_text, True, BLACK)
    
    screen.blit(eq_rendered, (20 + icon_size + 8, 50 + icon_size//2 - eq_rendered.get_height()//2))
    
    # ZONA 2: Status de progresso (à direita)
    # Checkpoints, velocidade e pontuação
    status_x = function_zone_width + 20
    
    # Velocidade
    speed_icon = create_icon_surface("speed", size=icon_size)
    screen.blit(speed_icon, (status_x, 15))
    
    speed_text = font.render(f"{game.speed:.1f} km/h", True, BLACK)
    screen.blit(speed_text, (status_x + icon_size + 8, 15 + icon_size//2 - speed_text.get_height()//2))
    
    # Checkpoints
    check_icon = create_icon_surface("checkpoint", size=icon_size)
    check_x = status_x + 160  # Posição após a velocidade
    screen.blit(check_icon, (check_x, 15))
    
    check_text = font.render(f"{game.checkpoints_passed}/{TOTAL_CHECKPOINTS}", True, BLACK)
    screen.blit(check_text, (check_x + icon_size + 8, 15 + icon_size//2 - check_text.get_height()//2))
    
    # Pontuação - destaque especial
    score_icon = create_icon_surface("score", size=icon_size)
    screen.blit(score_icon, (WIDTH - 120, 15))
    
    score_font = pygame.font.SysFont("Arial", 22, bold=True)
    score_text = score_font.render(f"{game.score}", True, (50, 50, 120))
    screen.blit(score_text, (WIDTH - 120 + icon_size + 8, 15 + icon_size//2 - score_text.get_height()//2))
    
    # Barra de progresso
    progress_width = WIDTH - 40
    progress_height = 8
    progress_x = 20
    progress_y = 75
    
    # Desenha o fundo da barra de progresso
    pygame.draw.rect(screen, (180, 180, 180), 
                    (progress_x, progress_y, progress_width, progress_height), 
                    border_radius=4)
    
    # Calcula o progresso atual (baseado nos checkpoints concluídos)
    if TOTAL_CHECKPOINTS > 0:
        progress_percent = game.checkpoints_passed / TOTAL_CHECKPOINTS
        fill_width = int(progress_width * progress_percent)
        
        # Desenha a barra de progresso preenchida
        if fill_width > 0:
            # Gradiente de cor na barra de progresso
            progress_color = (80, 180, 80)  # Verde mais vibrante
            pygame.draw.rect(screen, progress_color, 
                           (progress_x, progress_y, fill_width, progress_height), 
                           border_radius=4)
            
            # Pequenos marcadores para cada checkpoint
            for i in range(1, TOTAL_CHECKPOINTS):
                marker_x = progress_x + (i / TOTAL_CHECKPOINTS) * progress_width
                marker_height = progress_height + 4
                marker_y = progress_y - 2
                pygame.draw.line(screen, (120, 120, 120), 
                               (marker_x, marker_y), 
                               (marker_x, marker_y + marker_height), 
                               2)
    
    # Mensagem na tela (sem caixa de fundo, apenas o texto com brilho)
    if pygame.time.get_ticks() - game.message_time < 5000 or game.game_over:
        is_positive = "✓" in game.message or game.victory
        msg_color = GREEN if is_positive else RED
        
        # Mensagem principal com contorno para destaque
        msg_shadow_offset = 2
        msg_surface = large_font.render(game.message, True, msg_color)
        
        # Cria uma versão com sombra para dar destaque
        shadow_color = (0, 0, 0, 180)
        shadow_surf = pygame.Surface((msg_surface.get_width() + 8, msg_surface.get_height() + 8), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 0))  # Transparente
        
        # Posição centralizada abaixo do header
        msg_x = WIDTH//2 - msg_surface.get_width()//2
        msg_y = hud_height + 20
        
        # Adiciona o texto da mensagem com efeito de destaque
        # Primeiro desenha um contorno/sombra
        for offset_x in [-1, 0, 1]:
            for offset_y in [-1, 0, 1]:
                if offset_x == 0 and offset_y == 0:
                    continue  # Pula a posição central
                screen.blit(large_font.render(game.message, True, (0, 0, 0, 150)), 
                           (msg_x + offset_x, msg_y + offset_y))
        
        # Depois desenha o texto principal por cima
        screen.blit(msg_surface, (msg_x, msg_y))

    # Caixa de entrada de resposta com estilo minimalista
    if game.input_mode and not game.game_over:
        # Gradient overlay no fundo para destacar a área de input
        gradient_height = 180
        for y in range(gradient_height):
            alpha = int(180 * (y / gradient_height))  # Começa mais transparente e fica mais escuro
            pygame.draw.line(
                screen,
                (0, 0, 0, alpha),
                (0, HEIGHT - gradient_height + y),
                (WIDTH, HEIGHT - gradient_height + y)
            )
        
        # Caixa de entrada com design elegante
        input_width = 420
        input_height = 50
        input_bg = pygame.Rect(WIDTH//2 - input_width//2, HEIGHT - 80, input_width, input_height)
        
        # Fundo da caixa com sombra
        shadow_offset = 3
        shadow_rect = pygame.Rect(input_bg.left + shadow_offset, input_bg.top + shadow_offset,
                                 input_bg.width, input_bg.height)
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=12)
        
        # Caixa principal
        pygame.draw.rect(screen, (255, 255, 255), input_bg, border_radius=12)
        
        # Borda colorida baseada no tipo de derivada
        deriv_type = game.next_checkpoint["type"]
        border_color = GREEN if deriv_type == "first" else PURPLE
        pygame.draw.rect(screen, border_color, input_bg, 2, border_radius=12)
        
        # Ícone para o tipo de resposta
        icon_size = 36
        icon_color = GREEN if deriv_type == "first" else PURPLE
        deriv_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
        pygame.draw.circle(deriv_icon, icon_color, (icon_size//2, icon_size//2), icon_size//2 - 2, 0)
        
        # Símbolo da derivada
        symbol_text = "f'" if deriv_type == "first" else "f''"
        symbol_font = pygame.font.SysFont("Arial", 20, bold=True)
        text_f = symbol_font.render(symbol_text, True, WHITE)
        deriv_icon.blit(text_f, (icon_size//2 - text_f.get_width()//2, 
                                icon_size//2 - text_f.get_height()//2))
        
        # Posiciona o ícone no centro acima da caixa de entrada
        screen.blit(deriv_icon, (WIDTH//2 - icon_size//2, HEIGHT - 120))
        
        # Texto da pergunta com destaque
        if game.next_checkpoint["type"] == "first":
            prompt_text = f"Derivada f' em x ≈ {int(game.next_checkpoint['x'])}"
        else:
            prompt_text = f"Segunda derivada f'' em x ≈ {int(game.next_checkpoint['x'])}"
        
        prompt_font = pygame.font.SysFont("Arial", 22, bold=True)
        prompt = prompt_font.render(prompt_text, True, WHITE)
        
        # Adiciona um leve brilho ao texto para destaque
        glow_surf = pygame.Surface((prompt.get_width() + 10, prompt.get_height() + 10), pygame.SRCALPHA)
        glow_surf.fill((0, 0, 0, 0))  # Transparente
        
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT - 160))
        
        # Texto de entrada
        if game.input_text:
            input_text = font.render(game.input_text, True, BLACK)
        else:
            input_text = font.render("Digite sua resposta...", True, (150, 150, 150))
        
        # Centraliza o texto na caixa
        text_x = input_bg.left + (input_width - input_text.get_width()) // 2
        text_y = input_bg.top + (input_height - input_text.get_height()) // 2
        screen.blit(input_text, (text_x, text_y))
        
        # Botão de confirmação com estilo moderno
        button_width = 70
        button_height = 50
        confirm_button = pygame.Rect(
            input_bg.right + 20, 
            input_bg.top, 
            button_width, 
            button_height
        )
        
        # Botão com gradiente sutil
        button_color = GREEN
        for i in range(button_height):
            factor = 0.8 + (i / button_height) * 0.2  # Gradiente sutil
            color = (
                int(min(255, button_color[0] * factor)),
                int(min(255, button_color[1] * factor)),
                int(min(255, button_color[2] * factor))
            )
            pygame.draw.line(
                screen,
                color,
                (confirm_button.left, confirm_button.top + i),
                (confirm_button.right, confirm_button.top + i)
            )
        
        # Contorno do botão
        pygame.draw.rect(screen, (0, 100, 0), confirm_button, 2, border_radius=12)
        
        # Texto "OK" no botão
        confirm_text = pygame.font.SysFont("Arial", 22, bold=True).render("OK", True, WHITE)
        screen.blit(confirm_text, (
            confirm_button.centerx - confirm_text.get_width()//2, 
            confirm_button.centery - confirm_text.get_height()//2
        ))

    # Tela de game over com design moderno
    if game.game_over:
        # Overlay com gradiente radial
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Cria um gradiente radial do centro para as bordas
        center = (WIDTH//2, HEIGHT//2)
        max_radius = int(math.sqrt(WIDTH**2 + HEIGHT**2) / 2)
        
        for radius in range(max_radius, 0, -5):
            alpha = int(200 * (radius / max_radius))
            pygame.draw.circle(overlay, (0, 0, 0, alpha), center, radius)
            
        screen.blit(overlay, (0, 0))
        
        # Painel de resultado com tamanho ajustado
        panel_width = 750  # Largura um pouco maior para acomodar as barras
        panel_height = 550  # Altura um pouco maior para manter proporção
        panel_rect = pygame.Rect(WIDTH//2 - panel_width//2, HEIGHT//2 - panel_height//2, 
                                panel_width, panel_height)
        
        # Desenha o painel com cantos arredondados
        pygame.draw.rect(overlay, (30, 30, 30, 220), panel_rect, border_radius=20)
        screen.blit(overlay, (0, 0))
        
        # Definimos o texto e a cor baseados no resultado
        if game.crashed:
            result_text = "RESPOSTA INCORRETA!"
            border_color = RED
        elif game.victory:
            result_text = "VITÓRIA!"
            border_color = GREEN
            
        # Borda colorida baseada no resultado
        pygame.draw.rect(screen, border_color, panel_rect, 4, border_radius=20)
        
        # Texto do resultado com fonte menor
        result_font = pygame.font.SysFont("Arial", 40, bold=True)  # Fonte reduzida
        result_surf = result_font.render(result_text, True, border_color)
        result_y = panel_rect.top + 40  # Posicionado mais próximo ao topo do painel
        screen.blit(result_surf, (WIDTH//2 - result_surf.get_width()//2, result_y))
        
        # Instruções de teclas abaixo do título com espaçamento reduzido
        keys_font = pygame.font.SysFont("Arial", 18)  # Fonte menor
        keys_y = result_y + 60  # Espaço reduzido abaixo do título
        
        # Instruções para reiniciar e voltar ao menu em uma única linha
        keys_text = "Pressione R para jogar novamente | ESC para voltar ao menu"
        keys_surf = keys_font.render(keys_text, True, (200, 200, 200))
        screen.blit(keys_surf, (WIDTH//2 - keys_surf.get_width()//2, keys_y))
        
        # Pontuação com destaque - espaçamento reduzido
        score_font = pygame.font.SysFont("Arial", 24, bold=True)  # Fonte reduzida
        score_text = f"Pontuação final: {game.score}"
        score_surf = score_font.render(score_text, True, WHITE)
        score_y = keys_y + 50  # Espaço reduzido entre as instruções e a pontuação
        screen.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, score_y))
        
        # Adicionar visualização gráfica e dica para erros
        if game.crashed and game.error_info:
            # Título da comparação com espaçamento reduzido
            compare_title_y = score_y + 50  # Espaço reduzido após a pontuação
            compare_title_font = pygame.font.SysFont("Arial", 26, bold=True)  # Fonte reduzida
            compare_title = compare_title_font.render("COMPARAÇÃO DE VALORES", True, (220, 220, 220))
            screen.blit(compare_title, (WIDTH//2 - compare_title.get_width()//2, compare_title_y))
            
            # Informação sobre o erro - espaçamento reduzido
            error_info_y = compare_title_y + 40  # Espaçamento reduzido após o título
            error_font = pygame.font.SysFont("Arial", 22)  # Fonte reduzida
            
            # Mostrar valores
            deriv_type_text = "primeira derivada f'" if game.error_info["deriv_type"] == "first" else "segunda derivada f''"
            info_text = f"Em x = {int(game.error_info['x_value'])}, a {deriv_type_text} = {game.error_info['real_value']:.2f}"
            info_surf = error_font.render(info_text, True, WHITE)
            screen.blit(info_surf, (WIDTH//2 - info_surf.get_width()//2, error_info_y))
            
            # Comparação visual simplificada e mais clara
            compare_y = error_info_y + 40  # Espaçamento reduzido após a informação do erro
            
            # Em vez de um gráfico complexo, usamos uma representação de barras lado a lado
            bar_width = 550  # Aumentando a largura das barras
            bar_height = 100  # Aumentando a altura das barras
            bar_spacing = 12  # Reduzindo o espaçamento para maximizar o tamanho dos retângulos
            bar_rect = pygame.Rect(WIDTH//2 - bar_width//2, compare_y, bar_width, bar_height)
            
            # Fundo para a área de comparação
            pygame.draw.rect(screen, (40, 40, 40), bar_rect, border_radius=8)
            pygame.draw.rect(screen, (80, 80, 80), bar_rect, 2, border_radius=8)
            
            # Calculamos a largura para cada barra - maior espaçamento
            half_width = (bar_width - 3*bar_spacing) // 2
            
            # Barra para o valor correto - mais alta
            correct_bar_rect = pygame.Rect(bar_rect.left + bar_spacing, 
                                         bar_rect.top + bar_spacing, 
                                         half_width, 
                                         bar_height - 2*bar_spacing)
            pygame.draw.rect(screen, (30, 100, 30), correct_bar_rect, border_radius=6)  # Fundo verde escuro
            pygame.draw.rect(screen, GREEN, correct_bar_rect, 2, border_radius=6)  # Borda verde
            
            # Barra para a resposta do usuário - mais alta
            user_bar_rect = pygame.Rect(bar_rect.left + 2*bar_spacing + half_width, 
                                      bar_rect.top + bar_spacing, 
                                      half_width, 
                                      bar_height - 2*bar_spacing)
            pygame.draw.rect(screen, (100, 30, 30), user_bar_rect, border_radius=6)  # Fundo vermelho escuro
            pygame.draw.rect(screen, RED, user_bar_rect, 2, border_radius=6)  # Borda vermelha
            
            # Rótulos e valores para cada barra - fontes menores para garantir que caibam
            value_font = pygame.font.SysFont("Arial", 22, bold=True)
            label_font = pygame.font.SysFont("Arial", 18)
            
            # Valor correto
            correct_label = label_font.render("Valor correto", True, WHITE)
            correct_value = value_font.render(f"{game.error_info['real_value']:.2f}", True, WHITE)
            
            # Centraliza o texto nas barras com melhor espaçamento
            screen.blit(correct_label, 
                      (correct_bar_rect.centerx - correct_label.get_width()//2, 
                       correct_bar_rect.top + 10))  # Mais próximo ao topo
            screen.blit(correct_value, 
                      (correct_bar_rect.centerx - correct_value.get_width()//2, 
                       correct_bar_rect.centery + 10))  # Mais abaixo do centro
            
            # Valor do usuário
            user_label = label_font.render("Sua resposta", True, WHITE)
            user_value = value_font.render(f"{game.error_info['user_value']:.2f}", True, WHITE)
            
            # Adiciona o texto do usuário nas barras com mesmo espaçamento
            screen.blit(user_label, 
                      (user_bar_rect.centerx - user_label.get_width()//2, 
                       user_bar_rect.top + 10))  # Mais próximo ao topo
            screen.blit(user_value, 
                      (user_bar_rect.centerx - user_value.get_width()//2, 
                       user_bar_rect.centery + 10))  # Mais abaixo do centro
                       
            # Exibe a diferença no meio das barras em vez de usar setas
            diff = abs(game.error_info['user_value'] - game.error_info['real_value'])
            
            # Texto indicando a diferença - diretamente dentro do painel de barras
            diff_font = pygame.font.SysFont("Arial", 22, bold=True)
            diff_text = f"Diferença: {diff:.2f}"
            diff_surf = diff_font.render(diff_text, True, (255, 255, 100))  # Amarelo brilhante
            
            # Posiciona o texto da diferença mais abaixo (após as barras)
            diff_y = bar_rect.bottom + 15
            screen.blit(diff_surf, (WIDTH//2 - diff_surf.get_width()//2, diff_y))
            
            # Adiciona a dica no footer do painel com espaçamento adequado
            tip_font = pygame.font.SysFont("Arial", 18, italic=True)  # Fonte reduzida
            tip_y = panel_rect.bottom - 45  # 45 pixels acima da borda inferior do painel
            tip_surf = tip_font.render(game.error_tip, True, (255, 220, 100))
            screen.blit(tip_surf, (WIDTH//2 - tip_surf.get_width()//2, tip_y))
