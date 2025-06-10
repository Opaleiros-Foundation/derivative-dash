import pygame
import random
import math
from renderer import create_car_surface
from functions import FUNCTIONS

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
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
        self.speed = 2.0
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

        # Cria checkpoints alternando entre primeira e segunda derivadas
        spacing = self.TRACK_LENGTH / (self.TOTAL_CHECKPOINTS + 1)
        self.checkpoints = []
        for i in range(self.TOTAL_CHECKPOINTS):
            checkpoint_x = self.FUNC_RANGE[0] + (i+1) * spacing
            # Alterna entre primeira e segunda derivada
            deriv_type = "first" if i % 2 == 0 else "second"
            self.checkpoints.append({"x": checkpoint_x, "type": deriv_type})
        
        self.next_checkpoint = self.checkpoints[0]
        self.waiting_at_checkpoint = False

    def check_answer(self):
        try:
            user_value = float(self.input_text)
            
            if self.next_checkpoint["type"] == "first":
                real_value = self.df(self.next_checkpoint["x"])
                error = abs(user_value - real_value)
                threshold = 0.5  # Tolerância para primeira derivada
            else:
                real_value = self.d2f(self.next_checkpoint["x"])
                error = abs(user_value - real_value)
                threshold = 0.1  # Tolerância mais estrita para segunda derivada

            if error < threshold:
                self.message = "✓ Correto! Continue!"
                self.speed = 2.0
                self.score += 100 if self.next_checkpoint["type"] == "first" else 150  # Bônus para segunda derivada
                self.waiting_at_checkpoint = False
                self.input_mode = False
                self.checkpoints_passed += 1

                if self.checkpoints_passed < self.TOTAL_CHECKPOINTS:
                    self.next_checkpoint = self.checkpoints[self.checkpoints_passed]
                else:
                    self.next_checkpoint = {"x": self.FUNC_RANGE[1], "type": "none"}
            else:
                self.message = f"✗ Errado! Valor correto: {real_value:.2f}"
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
            self.camera_y = car_y - 300  # HEIGHT//2

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
                    self.message = f"🏁 VITÓRIA! Pontuação: {self.score}"
                else:
                    self.message = "Fim da pista! Você não completou todos os checkpoints!"
                self.game_over = True