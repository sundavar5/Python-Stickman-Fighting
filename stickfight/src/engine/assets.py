import pygame
import os

class AssetManager:
    """
    Manages loading and caching of game assets (images, sounds, fonts).
    """
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.base_path = "assets"

    def load_image(self, name, filename, scale=1.0):
        """Loads an image from the disk."""
        path = os.path.join(self.base_path, filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            if scale != 1.0:
                width = int(image.get_width() * scale)
                height = int(image.get_height() * scale)
                image = pygame.transform.scale(image, (width, height))
            self.images[name] = image
            return image
        except Exception as e:
            print(f"Error loading image {filename}: {e}")
            # Return a placeholder surface (magenta square)
            surf = pygame.Surface((32, 32))
            surf.fill((255, 0, 255))
            self.images[name] = surf
            return surf

    def get_image(self, name):
        """Returns a cached image."""
        return self.images.get(name)

    def load_sound(self, name, filename):
        """Loads a sound from the disk."""
        path = os.path.join(self.base_path, filename)
        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound
            return sound
        except Exception as e:
            print(f"Error loading sound {filename}: {e}")
            return None

    def play_sound(self, name):
        """Plays a cached sound."""
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def load_font(self, name, filename, size):
        """Loads a font."""
        # Using system font fallback for now if file not found
        try:
            if filename:
                 path = os.path.join(self.base_path, filename)
                 font = pygame.font.Font(path, size)
            else:
                 font = pygame.font.Font(None, size)
            self.fonts[name] = font
            return font
        except Exception as e:
            print(f"Error loading font {filename}: {e}")
            font = pygame.font.Font(None, size)
            self.fonts[name] = font
            return font

    def get_font(self, name):
        return self.fonts.get(name)
