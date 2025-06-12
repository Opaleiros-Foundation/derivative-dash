import pygame
from ui.menu.main_menu import Menu

def run_menu(screen):
    """
    Interface function to run the menu.
    This maintains compatibility with the existing code.
    
    Args:
        screen: Pygame display surface
        
    Returns:
        Menu result dictionary
    """
    menu = Menu(screen)
    return menu.run()