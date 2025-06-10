import pygame
import sys
import math
import os
from config import *
from game.game_state import GameState
from ui.renderer import draw_track, draw_checkpoints, draw_car, draw_hud, create_game_icon
from ui.menu import run_menu
from ui.game_screen import GameScreen
from utils.function_generator import get_functions

# Inicialização do pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Derivative Dash - Cálculo 2 (1ª e 2ª derivadas)")

# Definir o ícone da janela
pygame.display.set_icon(create_game_icon())

def run_game(difficulty=2):
    """Executa o loop principal do jogo"""
    # Cria um novo jogo com a dificuldade especificada
    game = GameState(difficulty)
    
    # Configurações adicionais baseadas na dificuldade
    # (as principais configurações são definidas na classe GameState)
    generated_count = 3  # Número de funções geradas
    if difficulty == 1:  # Fácil
        difficulty_range = (1, 1)  # Funções mais simples
    elif difficulty == 2:  # Normal
        difficulty_range = (1, 2)
    else:  # Difícil
        difficulty_range = (2, 3)  # Funções mais complexas
    
    # Carrega funções de acordo com a dificuldade
    from functions import FUNCTIONS
    
    # Cria e executa a tela do jogo
    game_screen = GameScreen(screen)
    game_screen.run(game)

def main():
    """Função principal que gerencia o fluxo entre menu e jogo"""
    in_menu = True
    
    while True:
        if in_menu:
            # Executa o menu e recebe as configurações escolhidas
            menu_result = run_menu(screen)
            
            if menu_result and menu_result["action"] == "start_game":
                # Inicia o jogo com a dificuldade selecionada
                difficulty = menu_result["difficulty"]
                in_menu = False
                run_game(difficulty)
                in_menu = True  # Volta para o menu quando o jogo terminar
        else:
            # Caso algo dê errado, volta para o menu
            in_menu = True

if __name__ == "__main__":
    main()