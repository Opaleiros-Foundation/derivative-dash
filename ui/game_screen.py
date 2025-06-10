import pygame
import sys
from config import *
from ui.renderer import draw_track, draw_checkpoints, draw_car, draw_hud, create_icon_surface

class GameScreen:
    """
    Classe responsável por gerenciar a tela do jogo em execução,
    lidando com renderização e entradas do usuário.
    """
    def __init__(self, screen):
        """
        Inicializa a tela do jogo.
        
        Args:
            screen: Superfície do pygame onde o jogo será renderizado
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
    def handle_events(self, game):
        """
        Processa eventos do pygame.
        
        Args:
            game: Instância de GameState
            
        Returns:
            bool: True se o jogo deve continuar, False para voltar ao menu
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Tecla Escape volta para o menu
                if event.key == pygame.K_ESCAPE:
                    return False
                # Processamento de entrada para o jogo
                if not game.game_over and game.input_mode:
                    if event.key == pygame.K_RETURN:
                        game.check_answer()
                    elif event.key == pygame.K_BACKSPACE:
                        game.input_text = game.input_text[:-1]
                    else:
                        game.input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Detecta clique no botão OK da caixa de entrada
                if game.input_mode and not game.game_over:
                    input_width = 420
                    input_height = 50
                    input_bg = pygame.Rect(WIDTH//2 - input_width//2, HEIGHT - 80, input_width, input_height)
                    button_width = 70
                    button_height = 50
                    confirm_button = pygame.Rect(
                        input_bg.right + 20, 
                        input_bg.top, 
                        button_width, 
                        button_height
                    )
                    if confirm_button.collidepoint(event.pos):
                        game.check_answer()
                
                # Detecta cliques nos botões da tela de game over
                if game.game_over:
                    # Dimensões do painel
                    panel_width = 500
                    panel_height = 300
                    panel_rect = pygame.Rect(WIDTH//2 - panel_width//2, HEIGHT//2 - panel_height//2, 
                                           panel_width, panel_height)
                    
                    # Botões de ação
                    button_width = 200
                    button_height = 50
                    button_y = panel_rect.bottom - 70
                    
                    # Botão de reiniciar
                    restart_button = pygame.Rect(WIDTH//2 - button_width - 10, button_y, button_width, button_height)
                    if restart_button.collidepoint(event.pos):
                        game.reset()
                    
                    # Botão de menu
                    menu_button = pygame.Rect(WIDTH//2 + 10, button_y, button_width, button_height)
                    if menu_button.collidepoint(event.pos):
                        return False  # Volta para o menu
        
        # Verifica tecla R para reiniciar após game over
        if game.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game.reset()
                
        return True
        
    def update(self, game):
        """
        Atualiza o estado do jogo e desenha todos os elementos.
        
        Args:
            game: Instância de GameState
        """
        # Limpa a tela
        self.screen.fill(WHITE)
        
        # Atualiza estado do jogo
        game.update()
        
        # Desenha elementos do jogo
        self._draw_game_elements(game)
        
        # Atualiza a tela
        pygame.display.flip()
        self.clock.tick(60)
    
    def _draw_game_elements(self, game):
        """
        Desenha todos os elementos visuais do jogo.
        
        Args:
            game: Instância de GameState
        """
        # Desenha a pista
        draw_track(self.screen, game, game.f, game.FUNC_RANGE, game.TRACK_LENGTH)
        
        # Desenha os checkpoints
        draw_checkpoints(self.screen, game, game.f)
        
        # Calcula posição do carro e desenha
        car_y = game.f(game.car_x)
        draw_car(self.screen, game, car_y, game.df)
        
        # Interface do usuário
        draw_hud(self.screen, game, game.current_func, game.TOTAL_CHECKPOINTS)
        
        # Removida a mensagem redundante de voltar ao menu
        # Os botões na tela de game over já têm essa informação
    
    def run(self, game):
        """
        Executa o loop principal da tela do jogo.
        
        Args:
            game: Instância de GameState
            
        Returns:
            dict: Resultado da execução do jogo
        """
        self.running = True
        
        while self.running:
            # Processa eventos
            if not self.handle_events(game):
                self.running = False
            
            # Atualiza e renderiza
            self.update(game)
        
        # Retorna ao menu principal
        return {"action": "back_to_menu"}