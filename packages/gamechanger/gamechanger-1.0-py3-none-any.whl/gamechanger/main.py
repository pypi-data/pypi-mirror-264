# main.py

import pygame

# AssetManager class
class AssetManager:
    def __init__(self):
        self.assets = {}

    def load_asset(self, asset_name, asset_path):
        # Load image or sound using Pygame
        if asset_path.endswith('.png'):
            asset = pygame.image.load(asset_path)
        elif asset_path.endswith('.wav'):
            asset = pygame.mixer.Sound(asset_path)
        else:
            raise ValueError("Unsupported asset type")
        self.assets[asset_name] = asset

    def get_asset(self, asset_name):
        return self.assets.get(asset_name)

# UIElement class
class UIElement:
    def __init__(self, x, y, asset=None):
        self.x = x
        self.y = y
        self.asset = asset

    def draw(self, screen):
        # Override this method in subclasses to draw the element
        pass

# Button class
class Button(UIElement):
    def __init__(self, x, y, width, height, text, callback, font_size=30, color=(255, 255, 255)):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont(None, font_size)
        self.color = color

    def draw(self, screen):
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, button_rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2,
                                   self.y + (self.height - text_surface.get_height()) // 2))

    def on_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x < event.pos[0] < self.x + self.width and self.y < event.pos[1] < self.y + self.height:
                self.callback()

# Image class
class Image(UIElement):
    def __init__(self, x, y, asset_name, asset_manager):
        asset = asset_manager.get_asset(asset_name)
        super().__init__(x, y, asset)

    def draw(self, screen):
        screen.blit(self.asset, (self.x, self.y))

# GameWindow class
class GameWindow:
    def __init__(self, title, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.elements = []
        self.running = True

    def add_element(self, element):
        self.elements.append(element)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for element in self.elements:
                    if hasattr(element, 'on_click'):
                        element.on_click(event)

            self.screen.fill((0, 0, 0))
            for element in self.elements:
                element.draw(self.screen)

            pygame.display.flip()

        pygame.quit()