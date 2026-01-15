import pygame

class InputManager:
    """
    Handles keyboard and mouse input.
    """
    def __init__(self):
        self.keys = {}
        self.prev_keys = {}
        self.mouse_buttons = {}
        self.prev_mouse_buttons = {}
        self.mouse_pos = (0, 0)
        self.quit_requested = False

    def update(self):
        """
        Updates the input state.
        """
        # Save previous state
        # In some pygame versions, key.get_pressed() returns a tuple or a wrapper that might not have .copy()
        # It's safer to just store it.
        self.prev_keys = self.keys
        self.prev_mouse_buttons = self.mouse_buttons

        # Get current state
        self.keys = pygame.key.get_pressed()
        self.mouse_buttons = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_requested = True

    def is_key_down(self, key_code):
        """Returns True if the key is currently pressed."""
        return self.keys[key_code] if key_code < len(self.keys) else False

    def is_key_just_pressed(self, key_code):
        """Returns True if the key was just pressed this frame."""
        pressed = self.keys[key_code] if key_code < len(self.keys) else False
        prev_pressed = self.prev_keys[key_code] if key_code < len(self.prev_keys) else False
        return pressed and not prev_pressed

    def is_key_just_released(self, key_code):
        """Returns True if the key was just released this frame."""
        pressed = self.keys[key_code] if key_code < len(self.keys) else False
        prev_pressed = self.prev_keys[key_code] if key_code < len(self.prev_keys) else False
        return not pressed and prev_pressed

    def is_mouse_down(self, button_index):
        """Returns True if the mouse button is pressed. 0=Left, 1=Middle, 2=Right."""
        if 0 <= button_index < len(self.mouse_buttons):
            return self.mouse_buttons[button_index]
        return False

    def is_mouse_just_pressed(self, button_index):
        """Returns True if the mouse button was just pressed this frame."""
        if 0 <= button_index < len(self.mouse_buttons):
            return self.mouse_buttons[button_index] and not self.prev_mouse_buttons[button_index]
        return False
