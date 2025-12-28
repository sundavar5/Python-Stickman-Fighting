import os
import sys

# Ensure we can import from the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.engine import Game

if __name__ == "__main__":
    game = Game()
    game.run()
