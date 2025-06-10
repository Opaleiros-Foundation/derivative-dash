import pygame
import sys
import math
import os
from config import *
from game import GameState
from renderer import draw_track, draw_checkpoints, draw_car, draw_hud

# Inicialização do pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Derivative Dash - Cálculo 2 (1ª e 2ª derivadas)")

# Criando um ícone estilizado similar ao SVG, mas gerado pelo Pygame
def create_game_icon():
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

# Definir o ícone da janela
pygame.display.set_icon(create_game_icon())

def main():
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
        
        # Atualiza estado do jogo
        game.update()
        
        # Desenha elementos do jogo
        draw_track(screen, game, game.f, game.FUNC_RANGE, game.TRACK_LENGTH)
        draw_checkpoints(screen, game, game.f)
        
        car_y = game.f(game.car_x)
        draw_car(screen, game, car_y, game.df)
        
        # Interface do usuário
        draw_hud(screen, game, game.current_func, game.TOTAL_CHECKPOINTS)
        
        # Verifica tecla R para reiniciar após game over
        if game.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game.reset()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()