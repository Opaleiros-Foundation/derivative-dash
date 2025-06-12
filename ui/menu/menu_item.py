import pygame
from config import *

class MenuItem:
    def __init__(self, text, action, pos, font, color=BLACK, hover_color=BLUE, active=True):
        self.text = text
        self.action = action
        self.pos = pos
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.active = active
        self.is_hovered = False
        self.render_text()
        
    def render_text(self):
        self.text_surface = self.font.render(self.text, True, self.hover_color if self.is_hovered else self.color)
        self.rect = self.text_surface.get_rect(center=self.pos)
        
    def update(self, mouse_pos):
        if self.active:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
            self.render_text()
            
    def draw(self, screen):
        if self.active:
            screen.blit(self.text_surface, self.rect)
            
    def trigger(self):
        if self.active:
            return self.action()
        return None