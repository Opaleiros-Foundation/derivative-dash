import pygame
import random
import math
from ui.renderer import create_car_surface
from functions import FUNCTIONS
from utils.function_generator import get_functions

class GameState:
    def __init__(self, difficulty=2):
        """
        Inicializa o estado do jogo.
        
        Args:
            difficulty (int): Nível de dificuldade (1=Fácil, 2=Normal, 3=Difícil)
        """
        self.difficulty = difficulty
        self.reset()

    def reset(self):
        """Reinicia o estado do jogo"""
        # Configuração baseada na dificuldade
        self._configure_difficulty()
        
        # Seleção aleatória de função
        self.current_func = random.choice(FUNCTIONS)
        self.f = self.current_func["f"]
        self.df = self.current_func["df"]
        self.d2f = self.current_func["d2f"]
        self.FUNC_RANGE = self.current_func["range"]
        self.TOTAL_CHECKPOINTS = self.current_func["checkpoints"]
        self.TRACK_LENGTH = self.FUNC_RANGE[1] - self.FUNC_RANGE[0]

        # Estado do carro e câmera
        self.car_x = self.FUNC_RANGE[0] + 50
        self.camera_x = 0
        self.camera_y = self.f(self.car_x) - 300  # HEIGHT//2
        # Velocidade definida baseada na dificuldade em _configure_difficulty()
        self.max_speed = 8.0
        
        # Estado do jogo
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
        # Informações para explicação de erro
        self.error_info = None
        self.error_tip = ""

        # Cria checkpoints alternando entre primeira e segunda derivadas
        spacing = self.TRACK_LENGTH / (self.TOTAL_CHECKPOINTS + 1)
        self.checkpoints = []
        for i in range(self.TOTAL_CHECKPOINTS):
            checkpoint_x = self.FUNC_RANGE[0] + (i+1) * spacing
            # Alterna entre primeira e segunda derivada
            # No modo fácil, mais checkpoints de primeira derivada
            if self.difficulty == 1:
                deriv_type = "first" if i % 3 != 2 else "second"
            else:
                deriv_type = "first" if i % 2 == 0 else "second"
            self.checkpoints.append({"x": checkpoint_x, "type": deriv_type})
        
        self.next_checkpoint = self.checkpoints[0]
        self.waiting_at_checkpoint = False

    def _configure_difficulty(self):
        """Configura os parâmetros do jogo baseados na dificuldade"""
        if self.difficulty == 1:  # Fácil
            self.speed = 1.5
            self.error_threshold_first = 0.8   # Tolerância maior
            self.error_threshold_second = 0.2  # Tolerância maior
            self.time_bonus = 1.5              # Mais tempo
        elif self.difficulty == 2:  # Normal
            self.speed = 2.0
            self.error_threshold_first = 0.5
            self.error_threshold_second = 0.1
            self.time_bonus = 1.0
        else:  # Difícil
            self.speed = 2.5
            self.error_threshold_first = 0.3   # Tolerância menor
            self.error_threshold_second = 0.08  # Tolerância menor
            self.time_bonus = 0.8              # Menos tempo

    def check_answer(self):
        try:
            user_value = float(self.input_text)
            
            if self.next_checkpoint["type"] == "first":
                real_value = self.df(self.next_checkpoint["x"])
                error = abs(user_value - real_value)
                threshold = self.error_threshold_first
                points = 100  # Pontos para primeira derivada
            else:
                real_value = self.d2f(self.next_checkpoint["x"])
                error = abs(user_value - real_value)
                threshold = self.error_threshold_second
                points = 150  # Pontos para segunda derivada (bônus)

            if error < threshold:
                self.message = "✓ Correto! Continue!"
                self.speed = max(1.5, self.speed)  # Mantém velocidade mínima
                
                # Bônus baseado na dificuldade
                difficulty_bonus = 1.0
                if self.difficulty == 3:  # Difícil
                    difficulty_bonus = 1.5
                
                self.score += int(points * difficulty_bonus)
                
                self.waiting_at_checkpoint = False
                self.input_mode = False
                self.checkpoints_passed += 1

                if self.checkpoints_passed < self.TOTAL_CHECKPOINTS:
                    self.next_checkpoint = self.checkpoints[self.checkpoints_passed]
                else:
                    self.next_checkpoint = {"x": self.FUNC_RANGE[1], "type": "none"}
            else:
                self.message = f"✗ Errado! Valor correto: {real_value:.2f}"
                self.error_info = {
                    "user_value": user_value,
                    "real_value": real_value,
                    "x_value": self.next_checkpoint["x"],
                    "deriv_type": self.next_checkpoint["type"]
                }
                # Adicionar dica de cálculo baseada no tipo de derivada
                if self.next_checkpoint["type"] == "first":
                    self.error_tip = "Lembre-se: a primeira derivada representa a inclinação da reta tangente."
                else:
                    self.error_tip = "Lembre-se: a segunda derivada indica a concavidade da função."
                self.speed = 0
                self.game_over = True
                self.crashed = True
                self.car_surface = create_car_surface((200, 50, 50))  # RED
            self.input_text = ''
            self.message_time = pygame.time.get_ticks()
        except ValueError:
            self.message = "Digite um número válido!"
            self.message_time = pygame.time.get_ticks()

    def update(self):
        if not self.game_over and not self.waiting_at_checkpoint:
            self.car_x += self.speed
            car_y = self.f(self.car_x)
            self.camera_x = max(0, self.car_x - 333)  # WIDTH//3
            
            # Limite para a posição vertical da câmera
            # Garantir que a câmera não suba tanto que o carro fique escondido atrás do header
            max_camera_y = car_y - 200  # Valor menor significa que a câmera fica mais baixa
            self.camera_y = min(max_camera_y, car_y - 300)  # HEIGHT//2

            if self.car_x >= self.next_checkpoint["x"] - 10 and not self.input_mode:
                self.car_x = self.next_checkpoint["x"]
                self.speed = 0
                self.waiting_at_checkpoint = True
                self.input_mode = True
                if self.next_checkpoint["type"] == "first":
                    self.message = f"Qual a derivada f' em x ≈ {int(self.next_checkpoint['x'])}?"
                else:
                    self.message = f"Qual a segunda derivada f'' em x ≈ {int(self.next_checkpoint['x'])}?"
                self.message_time = pygame.time.get_ticks()

            if self.car_x >= self.FUNC_RANGE[1] - 50:
                self.car_x = self.FUNC_RANGE[1] - 50
                self.speed = 0
                if self.checkpoints_passed == self.TOTAL_CHECKPOINTS:
                    self.victory = True
                    
                    # Bônus por vitória baseado na dificuldade
                    difficulty_bonus = 100 * self.difficulty
                    self.score += difficulty_bonus
                    
                    self.message = f"🏁 VITÓRIA! Pontuação: {self.score}"
                else:
                    self.message = "Fim da pista! Você não completou todos os checkpoints!"
                self.game_over = True