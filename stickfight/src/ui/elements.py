import pygame

class UIElement:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = True

    def update(self):
        pass

    def draw(self, surface):
        pass

class ProgressBar(UIElement):
    """
    A bar representing a value (HP, Mana, etc.)
    """
    def __init__(self, x, y, width, height, color, max_value, current_value=None):
        super().__init__(x, y, width, height)
        self.color = color
        self.bg_color = (50, 50, 50)
        self.max_value = max_value
        self.current_value = current_value if current_value is not None else max_value

    def update_value(self, current, maximum=None):
        self.current_value = current
        if maximum:
            self.max_value = maximum

    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)

        # Calculate fill width
        ratio = 0
        if self.max_value > 0:
            ratio = self.current_value / self.max_value
        fill_width = int(self.rect.width * ratio)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)

        # Draw fill
        pygame.draw.rect(surface, self.color, fill_rect)

        # Draw border
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)

class Button(UIElement):
    """
    A clickable button.
    """
    def __init__(self, x, y, width, height, text, font, action_callback):
        super().__init__(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action_callback
        self.color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self.text_color = (255, 255, 255)
        self.is_hovered = False

    def update(self, mouse_pos, mouse_click):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered and mouse_click:
            self.action()

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
