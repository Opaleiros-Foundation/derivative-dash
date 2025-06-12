import pygame
import sys
import math
from config import *
from ui.menu.menu_item import MenuItem
from ui.menu.tutorial import TutorialMenu
import os

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = None
        
        # Fontes
        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 36)
        self.info_font = pygame.font.SysFont("Arial", 20)
        
        # Inicializa menu items
        self.create_menu_items()
        
        # Animação de ondas
        self.time = 0
        
        # Carro na curva
        self.car_pos = 0  # posição do carro na curva (índice)
        self.car_speed = 2  # velocidade do carro
        
        # Cria um triangulo simples para representar o carro
        self.car_width = 20
        self.car_height = 12
        self.car_color = (255, 0, 100)  # Rosa
        
    def create_menu_items(self):
        # Posições centralizadas
        center_x = WIDTH // 2
        start_y = HEIGHT // 2 - 20
        spacing = 60
        
        self.menu_items = [
            MenuItem("Iniciar Jogo", self.start_game, (center_x, start_y), self.menu_font),
            MenuItem("Dificuldade: Normal", self.toggle_difficulty, (center_x, start_y + spacing), self.menu_font),
            MenuItem("Tutorial", self.show_tutorial, (center_x, start_y + spacing * 2), self.menu_font),
            MenuItem("Sair", self.exit_game, (center_x, start_y + spacing * 3), self.menu_font)
        ]
        
        # Dificuldade atual
        self.difficulty = 2  # 1=Fácil, 2=Normal, 3=Difícil
        
    def toggle_difficulty(self):
        difficulties = ["Fácil", "Normal", "Difícil"]
        self.difficulty = (self.difficulty % 3) + 1
        self.menu_items[1].text = f"Dificuldade: {difficulties[self.difficulty-1]}"
        self.menu_items[1].render_text()
        return None
        
    def start_game(self):
        return {"action": "start_game", "difficulty": self.difficulty}
        
    def show_tutorial(self):
        return {"action": "tutorial"}
        
    def exit_game(self):
        pygame.quit()
        sys.exit()
        
    def draw_background(self):
        # Gradiente de fundo
        for y in range(HEIGHT):
            color_val = int(180 + 75 * y / HEIGHT)
            pygame.draw.line(self.screen, (color_val, color_val, color_val), (0, y), (WIDTH, y))
            
        # Grade de fundo
        grid_color = (220, 220, 220)
        grid_spacing = 50
        for x in range(0, WIDTH, grid_spacing):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, grid_spacing):
            pygame.draw.line(self.screen, grid_color, (0, y), (WIDTH, y), 1)
            
        # Desenha curva animada
        self.time += 0.02
        curve_points = []
        for x in range(0, WIDTH, 5):
            # Soma de ondas senoidais com diferentes frequências
            y = HEIGHT // 2 + 50 * math.sin(x/100 + self.time) + 30 * math.sin(x/50 - self.time*1.5)
            curve_points.append((x, y))
            
        if len(curve_points) > 1:
            pygame.draw.lines(self.screen, GREEN, False, curve_points, 3)
            
        # Desenha pontos na curva para simular derivadas
        for i in range(0, WIDTH, 200):
            if i < len(curve_points):
                x, y = curve_points[i]
                pygame.draw.circle(self.screen, RED, (x, y), 8)
                
                # Linha tangente (derivada)
                if i > 0 and i < len(curve_points) - 1:
                    x_prev, y_prev = curve_points[i-1]
                    x_next, y_next = curve_points[i+1]
                    dx = (x_next - x_prev) / 2
                    dy = (y_next - y_prev) / 2
                    
                    # Normaliza a direção para desenhar uma linha tangente
                    length = math.sqrt(dx**2 + dy**2)
                    if length > 0:
                        dx = dx / length * 50
                        dy = dy / length * 50
                        
                    pygame.draw.line(self.screen, ORANGE, (x - dx, y - dy), (x + dx, y + dy), 2)
                    
        # Desenha o carro seguindo a curva
        self.draw_car_on_curve(curve_points)
    
    def draw_title(self):
        # Título do jogo com sombra
        title_shadow = self.title_font.render("DERIVATIVE DASH", True, (50, 50, 50))
        title_text = self.title_font.render("DERIVATIVE DASH", True, BLUE)
        
        shadow_rect = title_shadow.get_rect(center=(WIDTH//2 + 3, 100 + 3))
        text_rect = title_text.get_rect(center=(WIDTH//2, 100))
        
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_text, text_rect)
        
        # Subtítulo
        subtitle = self.info_font.render("Um jogo para aprender sobre derivadas", True, (80, 80, 80))
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 145))
        self.screen.blit(subtitle, subtitle_rect)
        
    def draw_footer(self):
        # Instruções
        instructions = self.info_font.render("Use o mouse para selecionar opções", True, (80, 80, 80))
        instructions_rect = instructions.get_rect(center=(WIDTH//2, HEIGHT - 50))
        self.screen.blit(instructions, instructions_rect)
    
    def draw_car_on_curve(self, curve_points):
        """Desenha um carro seguindo a curva animada"""
        if len(curve_points) < 2:
            return
            
        # Atualiza a posição do carro
        self.car_pos += self.car_speed
        
        # Reinicia a posição quando chega ao fim
        if self.car_pos >= len(curve_points):
            self.car_pos = 0
            
        # Certifica que a posição é válida
        car_index = int(self.car_pos) % len(curve_points)
        
        # Obtém a posição atual do carro
        car_x, car_y = curve_points[car_index]
        
        # Calcula a direção do carro (tangente da curva)
        next_index = (car_index + 1) % len(curve_points)
        prev_index = (car_index - 1) % len(curve_points)
        
        x_prev, y_prev = curve_points[prev_index]
        x_next, y_next = curve_points[next_index]
        
        dx = (x_next - x_prev) / 2
        dy = (y_next - y_prev) / 2
        
        # Calcula o ângulo de rotação
        angle = math.degrees(math.atan2(dy, dx))
        
        # Desenha o carro (triângulo rotacionado)
        # Pontos do triângulo
        car_points = [
            (car_x + self.car_width/2, car_y),
            (car_x - self.car_width/2, car_y - self.car_height/2),
            (car_x - self.car_width/2, car_y + self.car_height/2)
        ]
        
        # Rotaciona os pontos
        rotated_points = []
        for px, py in car_points:
            # Translada para a origem
            tx, ty = px - car_x, py - car_y
            # Rotaciona
            rx = tx * math.cos(math.radians(angle)) - ty * math.sin(math.radians(angle))
            ry = tx * math.sin(math.radians(angle)) + ty * math.cos(math.radians(angle))
            # Translada de volta
            rotated_points.append((rx + car_x, ry + car_y))
            
        # Desenha o carro
        pygame.draw.polygon(self.screen, self.car_color, rotated_points)
        
    def run_tutorial(self):
        """Mostra a tela de tutorial"""
        tutorial = TutorialMenu(self.screen, self.clock)
        tutorial.run()
    
    def run(self):
        """Loop principal do menu"""
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.menu_items:
                        if item.is_hovered:
                            result = item.trigger()
                            if result:
                                if result["action"] == "start_game":
                                    return result
                                elif result["action"] == "tutorial":
                                    self.run_tutorial()
            
            # Atualiza itens do menu
            for item in self.menu_items:
                item.update(mouse_pos)
            
            # Renderiza
            self.draw_background()
            self.draw_title()
            
            # Desenha itens do menu
            for item in self.menu_items:
                item.draw(self.screen)
                
            self.draw_footer()
            
            pygame.display.flip()
            self.clock.tick(60)