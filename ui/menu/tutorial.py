import pygame
import sys
from config import *

class TutorialMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 36)
        self.info_font = pygame.font.SysFont("Arial", 20)
        
        # Slides de tutorial
        self.tutorial_slides = [
            {
                "title": "Bem-vindo ao Derivative Dash!",
                "content": [
                    "Neste jogo, você vai testar seus conhecimentos de cálculo",
                    "dirigindo um carro ao longo de curvas matemáticas.",
                ]
            },
            {
                "title": "Como Jogar",
                "content": [
                    "- O carro se move automaticamente ao longo da função",
                    "- Nos checkpoints, você precisa calcular as derivadas",
                    "- Pontos verdes = primeira derivada (f')",
                    "- Pontos roxos = segunda derivada (f'')",
                    "- Responda corretamente para continuar"
                ]
            },
            {
                "title": "Dicas",
                "content": [
                    "- Observe o formato da função para estimar derivadas",
                    "- A primeira derivada é a inclinação da curva",
                    "- A segunda derivada indica concavidade",
                    "- Valores positivos: curva para cima",
                    "- Valores negativos: curva para baixo"
                ]
            }
        ]
    
    def run(self):
        """Executa o tutorial"""
        tutorial_running = True
        current_slide = 0
        
        while tutorial_running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        tutorial_running = False
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                        current_slide = min(current_slide + 1, len(self.tutorial_slides) - 1)
                    elif event.key == pygame.K_LEFT:
                        current_slide = max(current_slide - 1, 0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Área para voltar
                    if HEIGHT - 80 <= mouse_pos[1] <= HEIGHT - 30:
                        if 100 <= mouse_pos[0] <= 200:  # Botão Voltar
                            tutorial_running = False
                        elif WIDTH - 200 <= mouse_pos[0] <= WIDTH - 100:  # Botão Próximo/Anterior
                            if current_slide < len(self.tutorial_slides) - 1:
                                current_slide += 1
                            else:
                                tutorial_running = False
            
            # Desenha fundo
            self.screen.fill(WHITE)
            
            # Desenha conteúdo do slide atual
            slide = self.tutorial_slides[current_slide]
            
            # Título
            title_text = self.title_font.render(slide["title"], True, BLUE)
            title_rect = title_text.get_rect(center=(WIDTH//2, 100))
            self.screen.blit(title_text, title_rect)
            
            # Conteúdo
            for i, line in enumerate(slide["content"]):
                content_text = self.menu_font.render(line, True, BLACK)
                content_rect = content_text.get_rect(center=(WIDTH//2, 200 + i * 50))
                self.screen.blit(content_text, content_rect)
            
            # Navegação
            back_button = self.menu_font.render("Voltar", True, RED)
            back_rect = back_button.get_rect(center=(150, HEIGHT - 50))
            self.screen.blit(back_button, back_rect)
            
            if current_slide < len(self.tutorial_slides) - 1:
                next_text = "Próximo"
            else:
                next_text = "Finalizar"
                
            next_button = self.menu_font.render(next_text, True, GREEN)
            next_rect = next_button.get_rect(center=(WIDTH - 150, HEIGHT - 50))
            self.screen.blit(next_button, next_rect)
            
            # Indicador de slide
            slide_indicator = self.info_font.render(f"Slide {current_slide + 1}/{len(self.tutorial_slides)}", True, GRAY)
            indicator_rect = slide_indicator.get_rect(center=(WIDTH//2, HEIGHT - 50))
            self.screen.blit(slide_indicator, indicator_rect)
            
            pygame.display.flip()
            self.clock.tick(60)