import os
import sys

# Ensure the src directory is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from engine.game import Game

def main():
    print("Stickfight Game Starting...")
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
